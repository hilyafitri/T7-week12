# Nama  : Hilya Fitri
# NIM   : F1D02310009
# Kelas : C

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import Qt

from data.data_loader import DataLoader
from charts.chart_widget import ChartWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dashboard Visualisasi Data')
        self.resize(1400, 800)

        self.loader = DataLoader('supermarket_sales.csv')
        self.df = self.loader.load_data()

        self.init_ui()

        self.load_table(self.df)
        self.update_summary()
        self.update_chart()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ===== TITLE =====
        title = QLabel('Dashboard Supermarket Sales')
        title.setAlignment(Qt.AlignCenter)
        
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #D16D9E;
            margin: 15px;
        """)


        main_layout.addWidget(title)

        # ===== SUMMARY =====
        summary_layout = QHBoxLayout()

        self.total_transaksi_label = self.create_summary_card(
            'Total Transaksi'
        )

        self.total_pendapatan_label = self.create_summary_card(
            'Total Pendapatan'
        )

        self.rating_label = self.create_summary_card(
            'Rata Rating'
        )

        summary_layout.addWidget(self.total_transaksi_label)
        summary_layout.addWidget(self.total_pendapatan_label)
        summary_layout.addWidget(self.rating_label)

        main_layout.addLayout(summary_layout)

        # ===== FILTER =====
        filter_layout = QHBoxLayout()

        self.branch_filter = QComboBox()
        self.branch_filter.addItem('Semua Branch')

        branches = self.df['Branch'].unique()

        for branch in branches:
            self.branch_filter.addItem(branch)

        self.branch_filter.currentIndexChanged.connect(
            self.filter_data
        )

        self.chart_selector = QComboBox()

        self.chart_selector.addItems([
            'Bar Chart',
            'Pie Chart'
        ])

        self.chart_selector.currentIndexChanged.connect(
            self.update_chart
        )

        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_data)

        export_button = QPushButton('Export PNG')
        export_button.clicked.connect(self.export_chart)

        filter_layout.addWidget(QLabel('Filter Branch:'))
        filter_layout.addWidget(self.branch_filter)

        filter_layout.addSpacing(30)

        filter_layout.addWidget(QLabel('Pilih Chart:'))
        filter_layout.addWidget(self.chart_selector)

        filter_layout.addStretch()

        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(export_button)

        main_layout.addLayout(filter_layout)

        # ===== CONTENT =====
        content_layout = QHBoxLayout()

        # ===== TABLE =====
        self.table = QTableWidget()

        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        content_layout.addWidget(self.table, 3)

        # ===== CHART =====
        chart_container = QFrame()
        chart_layout = QVBoxLayout()

        self.chart_widget = ChartWidget()

        chart_layout.addWidget(self.chart_widget)

        chart_container.setLayout(chart_layout)

        content_layout.addWidget(chart_container, 2)

        main_layout.addLayout(content_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFF8F0;
                color: #5C3A47;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLabel {
                color: #5C3A47;
            }

            QTableWidget {
                background-color: white;
                border: 2px solid #F8C8DC;
                gridline-color: #FADADD;
                selection-background-color: #F8C8DC;
                color: #5C3A47;
            }

            QHeaderView::section {
                background-color: #F8C8DC;
                color: #5C3A47;
                padding: 5px;
                border: none;
                font-weight: bold;
            }

            QPushButton {
                background-color: #F8C8DC;
                color: #5C3A47;
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #F4B6C2;
            }

            QComboBox {
                background-color: white;
                border: 2px solid #F8C8DC;
                border-radius: 6px;
                padding: 5px;
                color: #5C3A47;
            }
        """)

        self.setLayout(main_layout)

    def create_summary_card(self, title):
        label = QLabel()

        label.setAlignment(Qt.AlignCenter)

        
        label.setStyleSheet("""
            background-color: #F8C8DC;
            color: #5C3A47;
            border-radius: 15px;
            padding: 20px;
            font-size: 16px;
            font-weight: bold;
        """)

        label.setText(title)

        return label

    def load_table(self, data):
        self.table.clear()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))

        self.table.setHorizontalHeaderLabels(data.columns)

        for row in range(len(data)):
            for col in range(len(data.columns)):
                value = str(data.iloc[row, col])

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(value)
                )

        self.table.resizeColumnsToContents()

    def update_summary(self):
        summary = self.loader.get_summary()

        self.total_transaksi_label.setText(
            f"Total Transaksi\n{summary['total_transaksi']}"
        )

        self.total_pendapatan_label.setText(
            f"Total Pendapatan\n${summary['total_pendapatan']:.2f}"
        )

        self.rating_label.setText(
            f"Rata Rating\n{summary['rata_rating']:.2f}"
        )

    def filter_data(self):
        selected_branch = self.branch_filter.currentText()

        if selected_branch == 'Semua Branch':
            filtered_df = self.df
        else:
            filtered_df = self.df[
                self.df['Branch'] == selected_branch
            ]

        self.filtered_df = filtered_df

        self.load_table(filtered_df)
        self.update_chart()

    def update_chart(self):
        chart_type = self.chart_selector.currentText()

        data = getattr(self, 'filtered_df', self.df)

        if chart_type == 'Bar Chart':
            self.chart_widget.plot_bar_chart(data)
        else:
            self.chart_widget.plot_pie_chart(data)

    def refresh_data(self):
        self.df = self.loader.load_data()

        self.load_table(self.df)
        self.update_summary()
        self.update_chart()

        QMessageBox.information(
            self,
            'Refresh',
            'Data berhasil direfresh!'
        )

    def export_chart(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            'Save Chart',
            '',
            'PNG Files (*.png)'
        )

        if file_name:
            self.chart_widget.figure.savefig(file_name)

            QMessageBox.information(
                self,
                'Export Success',
                'Chart berhasil disimpan!'
            )
