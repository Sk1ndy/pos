import tkinter as tk
from tkinter import ttk
import transactions
from db import get_connection

class TransactionsTab:
    def __init__(self, parent, printer):
        self.printer = printer
        self.frame = ttk.Frame(parent)

        self.cart = []

        self.entry = tk.Entry(self.frame)
        self.entry.pack()
        self.entry.bind('<Return>', self.scan)

        self.tree = ttk.Treeview(self.frame,
                                 columns=("nom", "prix"),
                                 show='headings')

        self.tree.heading("nom", text="Nom")
        self.tree.heading("prix", text="Prix")
        self.tree.pack()

        self.total_label = tk.Label(self.frame, text="0.00$")
        self.total_label.pack()

        tk.Button(self.frame, text="Payer",
                  command=self.pay).pack()

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
            self.update_total()

        self.entry.delete(0, 'end')

    def update_total(self):
        total = sum(x[1] for x in self.cart)
        self.total_label.config(text=f"{total:.2f}$")

    def pay(self):
        if not self.cart:
            return

        total = sum(x[1] for x in self.cart)

        transactions.save_transaction(total)

        self.printer.print_ticket(self.cart, total)

        self.cart = []
        self.tree.delete(*self.tree.get_children())
        self.update_total()