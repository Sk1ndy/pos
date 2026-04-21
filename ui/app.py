import tkinter as tk
from tkinter import ttk
from printer import Printer
from ui.articles_tab import ArticlesTab
from ui.transactions_tab import TransactionsTab

class App:
    def __init__(self, root):
        self.printer = Printer()

        notebook = ttk.Notebook(root)

        self.articles = ArticlesTab(notebook, self.printer)
        self.transactions = TransactionsTab(notebook, self.printer)

        notebook.add(self.articles.frame, text="Articles")
        notebook.add(self.transactions.frame, text="Transactions")

        notebook.pack(expand=1, fill="both")