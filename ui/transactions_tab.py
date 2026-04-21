import tkinter as tk
from tkinter import ttk
import transactions
from db import get_connection
from config import TAX_RATE

class TransactionsTab:
    def __init__(self, parent, printer):
        self.printer = printer
        self.frame = ttk.Frame(parent)
        self.cart = []

        tk.Label(self.frame, text="Code Barre:").pack()
        self.entry = tk.Entry(self.frame)
        self.entry.pack()
        self.entry.bind('<Return>', self.scan)

        self.tree = ttk.Treeview(self.frame, columns=("nom", "prix"), show='headings')
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prix", text="Prix")
        self.tree.pack()

        self.lbl_ht = tk.Label(self.frame, text="Prix normal : 0.00")
        self.lbl_ht.pack()
        
        self.lbl_tva = tk.Label(self.frame, text="Taxes : 0.00")
        self.lbl_tva.pack()
        
        self.lbl_ttc = tk.Label(self.frame, text="TOTAL : 0.00")
        self.lbl_ttc.pack()

        tk.Button(self.frame, text="Payer", command=self.pay).pack()
        tk.Button(self.frame, text="Vider", command=self.clear).pack()

    def scan(self, event):
        code = self.entry.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prix FROM articles WHERE code_barre=%s", (code,))
        res = cursor.fetchone()
        conn.close()

        if res:
            self.cart.append(res)
            self.tree.insert("", "end", values=res)
            self.update_totals()

        self.entry.delete(0, 'end')

    def update_totals(self):
        total_ht = sum(float(x[1]) for x in self.cart)
        taxes = total_ht * TAX_RATE
        total_ttc = total_ht + taxes

        self.lbl_ht.config(text=f"Prix normal : {total_ht:.2f}")
        self.lbl_tva.config(text=f"Taxes : {taxes:.2f}")
        self.lbl_ttc.config(text=f"TOTAL : {total_ttc:.2f}")

    def clear(self):
        self.cart = []
        self.tree.delete(*self.tree.get_children())
        self.update_totals()

    def pay(self):
        if not self.cart: return

        total_ht = sum(float(x[1]) for x in self.cart)
        taxes = total_ht * TAX_RATE
        total_ttc = total_ht + taxes

        transactions.save_transaction(total_ttc)
        self.printer.print_ticket(self.cart, total_ht, taxes, total_ttc)
        self.clear()