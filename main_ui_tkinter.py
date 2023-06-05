import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


class MyTabView(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # create tabs
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Rename")
        self.notebook.add(self.tab2, text="Copy")

    def get_selected_tab(self):
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        return tab_text


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My App")
        self.geometry("900x300")

        style = ThemedStyle(self)
        style.set_theme("black")

        # Create a container frame
        container = tk.Frame(self)
        container.pack(padx=20, pady=20)

        # Create a label
        label = tk.Label(container,
                         text="Quel sera le nouveau nom de vos différentes frames ?")
        label.pack(pady=10)

        # Create an entry for capturing user's name
        self.name_entry = tk.Entry(container)  # Utilisation de self pour rendre la variable accessible à toute la classe
        self.name_entry.pack(pady=10)

        # Create a label
        label = tk.Label(container, text="Voulez vous directement 'rename' vos fichier dans le dossier existant ou alors les 'copy' dans un nouveau dossier pour les renommer ?")
        label.pack(pady=10)

        # Create MyTabView
        self.tab_view = MyTabView(container)
        self.tab_view.pack()

        # Create a checkbox
        self.checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(container, text="Voulez vous supprimer l'ancien dossier ?", variable=self.checkbox_var)
        checkbox.pack(pady=10)

        self.button = tk.Button(self, text="Get Selected Tab", command=self.button_callback)
        self.button.pack(padx=10, pady=10)

    def button_callback(self):
        selected_tab = self.tab_view.get_selected_tab()
        name = self.name_entry.get()  # Utilisation de self pour accéder à la variable name_entry
        accepted = self.checkbox_var.get()
        print("Selected tab:", selected_tab)
        print("Name:", name)
        print("Accepted:", accepted)
        return selected_tab, name, accepted


app = App()
app.mainloop()