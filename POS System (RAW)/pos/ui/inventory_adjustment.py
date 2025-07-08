
import tkinter as tk
from tkinter import ttk, messagebox
from pos.db.database import get_session
from pos.db.models import Produk, InventoryAdjustment
import datetime

class InventoryAdjustmentScreen:
    def __init__(self, root, current_user):
        self.root = root
        self.root.title("Penyesuaian Stok")
        self.user = current_user
        self.session = get_session()
        self.build_ui()
        self.load_products()

    def build_ui(self):
        self.tree = ttk.Treeview(self.root, columns=("Nama", "Stok"), show="headings")
        self.tree.heading("Nama", text="Nama Produk")
        self.tree.heading("Stok", text="Stok Saat Ini")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.adjust_frame = tk.Frame(self.root)
        self.adjust_frame.pack(pady=5)

        tk.Label(self.adjust_frame, text="ID Produk").grid(row=0, column=0)
        self.id_entry = tk.Entry(self.adjust_frame, width=5)
        self.id_entry.grid(row=0, column=1)

        tk.Label(self.adjust_frame, text="Perubahan (+/-)").grid(row=0, column=2)
        self.qty_entry = tk.Entry(self.adjust_frame, width=5)
        self.qty_entry.grid(row=0, column=3)

        tk.Label(self.adjust_frame, text="Alasan").grid(row=0, column=4)
        self.reason_entry = tk.Entry(self.adjust_frame, width=20)
        self.reason_entry.grid(row=0, column=5)

        self.adjust_btn = tk.Button(self.adjust_frame, text="Simpan", command=self.apply_adjustment)
        self.adjust_btn.grid(row=0, column=6, padx=10)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        products = self.session.query(Produk).filter(Produk.is_active == True).all()
        for p in products:
            self.tree.insert("", tk.END, values=(p.name, p.stock_quantity))

    def apply_adjustment(self):
        try:
            product_id = int(self.id_entry.get())
            change = int(self.qty_entry.get())
            reason = self.reason_entry.get().strip()
            if not reason:
                raise ValueError("Alasan wajib diisi")

            produk = self.session.query(Produk).get(product_id)
            if not produk:
                raise ValueError("Produk tidak ditemukan")

            produk.stock_quantity += change
            self.session.add(InventoryAdjustment(
                product_id=product_id,
                adjusted_by=self.user.username,
                change=change,
                reason=reason,
                timestamp=datetime.datetime.utcnow()
            ))
            self.session.commit()
            messagebox.showinfo("Berhasil", "Stok berhasil diperbarui")
            self.load_products()
        except Exception as e:
            messagebox.showerror("Gagal", str(e))
