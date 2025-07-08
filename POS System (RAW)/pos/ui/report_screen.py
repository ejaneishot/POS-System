
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from pos.db.database import get_session
from pos.db.models import Produk, Transaksi, DetailTransaksi

class ReportScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Laporan Penjualan & Stok")
        self.session = get_session()
        self.build_ui()
        self.load_reports()

    def build_ui(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill='both')

        self.daily_sales_tab = tk.Frame(self.tabs)
        self.top_products_tab = tk.Frame(self.tabs)
        self.low_stock_tab = tk.Frame(self.tabs)

        self.tabs.add(self.daily_sales_tab, text="Ringkasan Harian")
        self.tabs.add(self.top_products_tab, text="Top Produk")
        self.tabs.add(self.low_stock_tab, text="Stok Rendah")

        self.sales_text = tk.Text(self.daily_sales_tab, wrap="word")
        self.sales_text.pack(expand=1, fill='both', padx=10, pady=10)

        self.top_text = tk.Text(self.top_products_tab, wrap="word")
        self.top_text.pack(expand=1, fill='both', padx=10, pady=10)

        self.low_stock_text = tk.Text(self.low_stock_tab, wrap="word")
        self.low_stock_text.pack(expand=1, fill='both', padx=10, pady=10)

    def load_reports(self):
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        transactions = self.session.query(Transaksi).filter(
            Transaksi.timestamp >= today,
            Transaksi.timestamp < tomorrow
        ).all()

        total_sales = sum(t.total_amount for t in transactions)
        num_transactions = len(transactions)

        self.sales_text.insert(tk.END, f"Tanggal: {today}\n")
        self.sales_text.insert(tk.END, f"Total Transaksi: {num_transactions}\n")
        self.sales_text.insert(tk.END, f"Total Penjualan: Rp {total_sales:.0f}\n")

        # Top products by quantity sold today
        top_query = (
            self.session.query(DetailTransaksi.product_id, Produk.name, Produk.category,
                               Produk.price, tk.func.sum(DetailTransaksi.quantity).label("qty"))
            .join(Produk, Produk.product_id == DetailTransaksi.product_id)
            .join(Transaksi, Transaksi.transaction_id == DetailTransaksi.transaction_id)
            .filter(Transaksi.timestamp >= today, Transaksi.timestamp < tomorrow)
            .group_by(DetailTransaksi.product_id)
            .order_by(tk.func.sum(DetailTransaksi.quantity).desc())
            .limit(5)
        )

        self.top_text.insert(tk.END, "Top 5 Produk Terjual Hari Ini:\n")
        for pid, name, cat, price, qty in top_query:
            self.top_text.insert(tk.END, f"{name} ({cat}) - {qty} pcs\n")

        # Low stock warning
        low_stock_items = self.session.query(Produk).filter(Produk.stock_quantity <= 10).all()
        self.low_stock_text.insert(tk.END, "Produk dengan Stok Rendah (<= 10):\n")
        for p in low_stock_items:
            self.low_stock_text.insert(tk.END, f"{p.name} - Stok: {p.stock_quantity}\n")
