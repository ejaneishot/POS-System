
import tkinter as tk
from tkinter import messagebox
from pos.db.database import get_session
from pos.db.models import Produk, Transaksi, DetailTransaksi
import datetime

class FastSellApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Sell")
        self.session = get_session()
        self.cart = {}
        self.build_ui()
        self.load_products()

    def build_ui(self):
        self.product_frame = tk.Frame(self.root)
        self.product_frame.pack(pady=10)

        self.cart_frame = tk.Frame(self.root)
        self.cart_frame.pack(pady=10)

        self.cart_listbox = tk.Listbox(self.cart_frame, width=50)
        self.cart_listbox.pack()

        self.total_label = tk.Label(self.cart_frame, text="Total: Rp 0")
        self.total_label.pack()

        self.checkout_button = tk.Button(self.cart_frame, text="Bayar Tunai", command=self.checkout)
        self.checkout_button.pack(pady=10)

    def load_products(self):
        products = self.session.query(Produk).filter_by(is_active=True).order_by(Produk.updated_at.desc()).limit(9).all()
        for idx, product in enumerate(products):
            btn = tk.Button(self.product_frame, text=f"{product.name}
Rp{product.price:.0f}",
                            width=20, height=4,
                            command=lambda p=product: self.add_to_cart(p))
            btn.grid(row=idx // 3, column=idx % 3, padx=5, pady=5)

    def add_to_cart(self, product):
        if product.product_id in self.cart:
            self.cart[product.product_id]["quantity"] += 1
        else:
            self.cart[product.product_id] = {
                "name": product.name,
                "price": product.price,
                "quantity": 1
            }
        self.update_cart()

    def update_cart(self):
        self.cart_listbox.delete(0, tk.END)
        total = 0
        for item in self.cart.values():
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            self.cart_listbox.insert(tk.END, f"{item['name']} x{item['quantity']} = Rp{subtotal:.0f}")
        self.total_label.config(text=f"Total: Rp {total:.0f}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Kosong", "Keranjang kosong!")
            return
        total = sum(item["price"] * item["quantity"] for item in self.cart.values())
        transaksi = Transaksi(timestamp=datetime.datetime.utcnow(), total_amount=total, payment_method="Tunai")
        self.session.add(transaksi)
        self.session.commit()

        for product_id, item in self.cart.items():
            detail = DetailTransaksi(
                transaction_id=transaksi.transaction_id,
                product_id=product_id,
                quantity=item["quantity"],
                unit_price=item["price"],
                subtotal=item["price"] * item["quantity"]
            )
            self.session.add(detail)
            # Reduce stock
            produk = self.session.query(Produk).get(product_id)
            if produk:
                produk.stock_quantity -= item["quantity"]
        self.session.commit()

        messagebox.showinfo("Sukses", "Transaksi berhasil disimpan!")
        self.cart.clear()
        self.update_cart()
