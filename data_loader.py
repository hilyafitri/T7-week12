# Nama  : Hilya Fitri
# NIM   : F1D02310009
# Kelas : C

import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.file_path)

        self.df.columns = self.df.columns.str.strip()

        print(self.df.columns)

        return self.df

    def get_summary(self):
        total_transaksi = len(self.df)
        
        total_pendapatan = self.df['Sales'].sum()

        rata_rating = self.df['Rating'].mean()

        return {
            'total_transaksi': total_transaksi,
            'total_pendapatan': total_pendapatan,
            'rata_rating': rata_rating
        }
