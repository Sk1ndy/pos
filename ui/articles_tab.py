import tkinter as tk
from tkinter import ttk, messagebox
import articles

class ArticlesTab:
    def __init__(self, parent, printer):
        self.printer = printer

        self.frame = ttk.Frame(parent)

        self.ent_code = tk.Entry(self.frame)
        self.ent_nom = tk.Entry(self.frame)
        self.ent_prix = tk.Entry(self.frame)

        self.ent_code.grid(row=0, column=1)
        self.ent_nom.grid(row=0, column=3)
        self.ent_prix.grid(row=0, column=5)

        tk.Button(self.frame, text="Save",
                  command=self.save).grid(row=1, column=0)

        tk.Button(self.frame, text="Delete",
                  command=self.delete).grid(row=1, column=1)

        tk.Button(self.frame, text="Print",
                  command=self.print_barcode).grid(row=1, column=2)

        self.tree = ttk.Treeview(self.frame,
                                 columns=("code", "nom", "prix"),
                                 show='headings')

        for col in ("code", "nom", "prix"):
            self.tree.heading(col, text=col)

        self.tree.grid(row=2, column=0, columnspan=6)

        self.refresh()

    def save(self):
        articles.upsert_article(
            self.ent_code.get(),
            self.ent_nom.get(),
            self.ent_prix.get()
        )
        self.refresh()

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            return

        code = self.tree.item(selected)['values'][0]
        articles.delete_article(code)
        self.refresh()

    def print_barcode(self):
        if not self.printer.is_ready():
            messagebox.showerror("Erreur", "Imprimante non connectée")
            return

        self.printer.print_barcode(
            self.ent_nom.get(),
            self.ent_code.get()
        )

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in articles.get_all_articles():
            self.tree.insert("", "end", values=row)