import tkinter as tk
from pos.ui.login_screen import LoginScreen
from pos.ui.fast_sell import FastSellApp
from pos.ui.report_screen import ReportScreen
from pos.ui.inventory_adjustment import InventoryAdjustmentScreen

def start_app(user):
    root = tk.Tk()
    root.geometry("600x600")

    if user.role == "kasir":
        app = FastSellApp(root)
    elif user.role in ["admin", "kepala", "kepala unit"]:
        root.title(f"Dashboard - {user.role.capitalize()}")
        tk.Label(root, text=f"Selamat datang, {user.username} ({user.role})", font=('Arial', 14)).pack(pady=20)
        tk.Button(root, text="Buka Laporan", command=lambda: open_report()).pack(pady=10)

        if user.role == "admin":
            tk.Button(root, text="Penyesuaian Stok", command=lambda: open_inventory_adjustment(user)).pack(pady=10)
    else:
        tk.Label(root, text="Peran tidak dikenal.").pack()

    root.mainloop()

def open_report():
    report_root = tk.Toplevel()
    report_root.geometry("600x400")
    ReportScreen(report_root)

def open_inventory_adjustment(user):
    adj_root = tk.Toplevel()
    adj_root.geometry("700x400")
    InventoryAdjustmentScreen(adj_root, current_user=user)

if __name__ == "__main__":
    login_root = tk.Tk()
    login_root.geometry("300x200")
    LoginScreen(login_root, on_login_success=start_app)
    login_root.mainloop()
