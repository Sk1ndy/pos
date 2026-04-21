import tkinter as tk
from tkinter import ttk
import articles

class ArticlesTab:
    def __init__(self, parent, printer):
        self.printer = printer
        self.frame = ttk.Frame(parent)

        # Labels et Champs de saisie
        tk.Label(self.frame, text="Code:").grid(row=0, column=0)
        self.ent_code = tk.Entry(self.frame)
        self.ent_code.grid(row=0, column=1)

        tk.Label(self.frame, text="Nom:").grid(row=0, column=2)
        self.ent_nom = tk.Entry(self.frame)
        self.ent_nom.grid(row=0, column=3)

        tk.Label(self.frame, text="Prix:").grid(row=0, column=4)
        self.ent_prix = tk.Entry(self.frame)
        self.ent_prix.grid(row=0, column=5)

        # Boutons standards
        tk.Button(self.frame, text="Enregistrer", command=self.save).grid(row=1, column=0)
        tk.Button(self.frame, text="Supprimer", command=self.delete).grid(row=1, column=1)
        tk.Button(self.frame, text="Imprimer", command=self.print_barcode).grid(row=1, column=2)

        # Tableau
        self.tree = ttk.Treeview(self.frame, columns=("code", "nom", "prix"), show='headings')
        for col in ("code", "nom", "prix"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=6)

        self.refresh()

    def save(self):
        code = self.ent_code.get()
        nom = self.ent_nom.get()
        prix = self.ent_prix.get().replace(',', '.')
        
        if code and nom and prix:
            articles.upsert_article(code, nom, float(prix))
            self.refresh()

    def delete(self):
        selected = self.tree.selection()
        if selected:
            code = self.tree.item(selected[0])['values'][0]
            articles.delete_article(code)
            self.refresh()

    def print_barcode(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.printer.print_barcode(item[1], item[0])

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in articles.get_all_articles():
            self.tree.insert("", "end", values=row)