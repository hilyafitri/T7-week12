# Nama  : Hilya Fitri
# NIM   : F1D02310009
# Kelas : C

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 4))
        super().__init__(self.figure)
    
    def plot_bar_chart(self, data):
        self.figure.clear()

        ax = self.figure.add_subplot(111)

        sales = data.groupby('Product line')['Sales'].sum()

        ax.bar(sales.index, sales.values)
        ax.set_title('Total Penjualan per Product Line')
        ax.set_xlabel('Product Line')
        ax.set_ylabel('Total Sales')

        ax.tick_params(axis='x', rotation=20)

        self.figure.subplots_adjust(bottom=0.3)

        self.figure.tight_layout()

        self.draw()

    def plot_pie_chart(self, data):
        self.figure.clear()

        ax = self.figure.add_subplot(111)

        payment = data['Payment'].value_counts()

        ax.pie(payment.values,
               labels=payment.index,
               autopct='%1.1f%%')

        ax.set_title('Metode Pembayaran')

        self.draw()