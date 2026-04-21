import tkinter as tk
from tkinter import ttk, messagebox
import articles

class ArticlesTab:
    def __init__(self, parent, printer):
        self.printer = printer
        self.frame = ttk.Frame(parent)
        
        # Configuration pour que le tableau s'étire avec la fenêtre
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # --- Section Saisie ---
        input_frame = ttk.Frame(self.frame, padding="10")
        input_frame.grid(row=0, column=0, sticky="ew")

        tk.Label(input_frame, text="Code Barre:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_code = tk.Entry(input_frame)
        self.ent_code.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Nom:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_nom = tk.Entry(input_frame)
        self.ent_nom.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Prix:").grid(row=0, column=4, padx=5, pady=5)
        self.ent_prix = tk.Entry(input_frame)
        self.ent_prix.grid(row=0, column=5, padx=5, pady=5)

        # --- Section Boutons ---
        button_frame = ttk.Frame(self.frame, padding="5")
        button_frame.grid(row=1, column=0, sticky="ew")

        tk.Button(button_frame, text="Enregistrer", bg="#4CAF50", fg="white",
                  command=self.save).grid(row=0, column=0, padx=5)

        tk.Button(button_frame, text="Supprimer", bg="#f44336", fg="white",
                  command=self.delete).grid(row=0, column=1, padx=5)

        tk.Button(button_frame, text="Imprimer Code", bg="#2196F3", fg="white",
                  command=self.print_barcode).grid(row=0, column=2, padx=5)

        tk.Button(button_frame, text="Vider champs", 
                  command=self.clear_inputs).grid(row=0, column=3, padx=5)

        # --- Tableau avec Scrollbar ---
        tree_frame = ttk.Frame(self.frame)
        tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("code", "nom", "prix"), show='headings')
        
        # Ajout d'une barre de défilement pour les longs inventaires
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in ("code", "nom", "prix"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Événement : clic sur un article pour le charger dans les champs
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.clear_inputs()
            self.ent_code.insert(0, str(item[0]))
            self.ent_nom.insert(0, str(item[1]))
            self.ent_prix.insert(0, str(item[2]))

    def save(self):
        code = self.ent_code.get().strip()
        nom = self.ent_nom.get().strip()
        prix_str = self.ent_prix.get().strip().replace(',', '.')

        # Sécurité : vérifier que rien n'est vide
        if not code or not nom or not prix_str:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")
            return

        # Sécurité : s'assurer que le prix est un format valide pour la base de données
        try:
            prix = float(prix_str)
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre valide.")
            return

        articles.upsert_article(code, nom, prix)
        self.refresh()
        self.clear_inputs()

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Veuillez sélectionner un article à supprimer.")
            return

        # Sécurité : demander confirmation avant destruction en DB
        if not messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet article ?"):
            return

        code = self.tree.item(selected[0])['values'][0]
        articles.delete_article(code)
        self.refresh()
        self.clear_inputs()

    def print_barcode(self):
        if not self.printer.is_ready():
            messagebox.showerror("Erreur", "Imprimante non connectée")
            return
        
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.printer.print_barcode(item[1], item[0])
        else:
            code = self.ent_code.get().strip()
            nom = self.ent_nom.get().strip()
            if code and nom:
                self.printer.print_barcode(nom, code)
            else:
                messagebox.showwarning("Attention", "Sélectionnez un article ou remplissez le code et le nom.")

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in articles.get_all_articles():
            self.tree.insert("", "end", values=row)

    def clear_inputs(self):
        self.ent_code.delete(0, tk.END)
        self.ent_nom.delete(0, tk.END)
        self.ent_prix.delete(0, tk.END)