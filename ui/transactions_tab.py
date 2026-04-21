import tkinter as tk
from tkinter import ttk, messagebox
import transactions
from config import TAX_RATE
from db import get_connection

class TransactionsTab:
    def __init__(self, parent, printer):
        self.printer = printer
        self.frame = ttk.Frame(parent)
        
        # Grille principale (2 colonnes)
        self.frame.columnconfigure(0, weight=3) # Zone liste (plus large)
        self.frame.columnconfigure(1, weight=1) # Zone paiement
        self.frame.rowconfigure(0, weight=1)

        self.cart = []
        self.tva_rate = 0.20 # TVA à 20%

        # --- Zone Gauche : Scan et Panier ---
        left_frame = ttk.Frame(self.frame, padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.columnconfigure(1, weight=1)
        left_frame.rowconfigure(1, weight=1)

        ttk.Label(left_frame, text="Code Barre:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.entry = tk.Entry(left_frame, font=("Arial", 14))
        self.entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.entry.bind('<Return>', self.scan)
        self.entry.focus() # Place le curseur directement ici

        # Tableau des articles
        self.tree = ttk.Treeview(left_frame, columns=("nom", "prix"), show='headings')
        self.tree.heading("nom", text="Article")
        self.tree.heading("prix", text="Prix TTC")
        self.tree.column("nom", width=250)
        self.tree.column("prix", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        scrollbar.grid(row=1, column=2, sticky="ns", pady=10)

        # --- Zone Droite : Totaux et Actions ---
        right_frame = ttk.Frame(self.frame, padding="10", relief="ridge")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(right_frame, text="RÉSUMÉ", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        self.lbl_ht = tk.Label(right_frame, text="Sous-total HT : 0.00$", font=("Arial", 11))
        self.lbl_ht.pack(anchor="w", pady=2)

        self.lbl_tva = tk.Label(right_frame, text="TVA (20%) : 0.00$", font=("Arial", 11))
        self.lbl_tva.pack(anchor="w", pady=2)

        self.lbl_ttc = tk.Label(right_frame, text="TOTAL TTC : 0.00$", font=("Arial", 16, "bold"), fg="blue")
        self.lbl_ttc.pack(anchor="w", pady=15)

        # Boutons d'action
        tk.Button(right_frame, text="Payer & Imprimer", bg="#4CAF50", fg="white", 
                  font=("Arial", 12, "bold"), height=2, command=self.pay).pack(fill="x", pady=5)
        
        tk.Button(right_frame, text="Retirer l'article", bg="#FF9800", fg="white", 
                  command=self.remove_item).pack(fill="x", pady=5)
        
        tk.Button(right_frame, text="Annuler la vente", bg="#F44336", fg="white", 
                  command=self.clear_cart).pack(fill="x", pady=5)

    def scan(self, event):
        code = self.entry.get().strip()
        if not code: return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prix FROM articles WHERE code_barre=%s", (code,))
        res = cursor.fetchone()
        conn.close()

        if res:
            self.cart.append(res)
            self.tree.insert("", "end", values=(res[0], f"{res[1]:.2f}$"))
            self.update_totals()
        else:
            messagebox.showwarning("Inconnu", "Code barre non reconnu.")

        self.entry.delete(0, 'end')

    def update_totals(self):
        total_ttc = sum(float(x[1]) for x in self.cart)
        total_ht = total_ttc / (1 + self.tva_rate)
        tva = total_ttc - total_ht

        self.lbl_ht.config(text=f"Sous-total HT : {total_ht:.2f}$")
        self.lbl_tva.config(text=f"TVA (20%) : {tva:.2f}$")
        self.lbl_ttc.config(text=f"TOTAL TTC : {total_ttc:.2f}$")

    def remove_item(self):
        selected = self.tree.selection()
        if not selected: return
        
        # Trouver l'index de l'élément cliqué et le retirer
        index = self.tree.index(selected[0])
        self.cart.pop(index)
        self.tree.delete(selected[0])
        self.update_totals()

    def clear_cart(self):
        if not self.cart: return
        if messagebox.askyesno("Annuler", "Vider le panier actuel ?"):
            self.cart.clear()
            self.tree.delete(*self.tree.get_children())
            self.update_totals()

    def pay(self):
        if not self.cart: return

        total_ht = sum(float(x[1]) for x in self.cart)
        taxes = total_ht * TAX_RATE
        total_ttc = total_ht + taxes

        # Sauvegarde en BDD du prix final
        transactions.save_transaction(total_ttc)

        # Impression avec les nouvelles informations
        self.printer.print_ticket(self.cart, total_ht, taxes, total_ttc)

        self.cart.clear()
        self.tree.delete(*self.tree.get_children())
        self.update_totals()
        self.entry.focus()