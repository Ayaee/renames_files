import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle


class MyTabView(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.checkbox_var = None
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # create tabs
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Rename")
        self.notebook.add(self.tab2, text="Copy")

        # Create browse button in both tabs
        self.create_browse_button(self.tab1)
        self.create_browse_button(self.tab2)

        # Create checkbox in the "Copy" tab
        self.create_copy_tab()

    def create_browse_button(self, parent):
        browse_button = tk.Button(parent, text="Choisir le dossier qui contient les fichiers à renommer",
                                  command=self.get_browse_folder)
        browse_button.pack(pady=10, padx=10)

    def get_browse_folder(self):
        folder_path = filedialog.askdirectory()
        print(type(folder_path))
        return folder_path

    def create_copy_tab(self):
        copy_frame = self.tab2

        # Create a button to select the folder copy
        browse_button_copy = tk.Button(copy_frame, text="Choisir le dossier où copier et renommer les fichers",
                                       command=self.get_browse_folder_copy)
        browse_button_copy.pack(pady=10)

        # Create a checkbox
        self.checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(copy_frame, text="Voulez vous supprimer l'ancien dossier ?",
                                  variable=self.checkbox_var)
        checkbox.pack(pady=10)

    def get_browse_folder_copy(self):
        folder_path_copy = filedialog.askdirectory()
        print("Selected folder copy:", folder_path_copy)
        return folder_path_copy

    def get_selected_tab(self):
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        return tab_text


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My App")
        self.geometry("850x400")

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

        self.button = tk.Button(self, text="Valider", command=self.button_callback)
        self.button.pack(padx=10, pady=10)

        # Initialize selected_folder attribute
        self.selected_folder = None

    def button_callback(self):
        selected_tab = self.tab_view.get_selected_tab()
        name = self.name_entry.get()  # Utilisation de self pour accéder à la variable name_entry
        accepted = self.tab_view.checkbox_var.get()  # Utilisation de la variable de la tab view
        print("Selected tab:", selected_tab)
        print("Name:", name)
        print("Accepted:", accepted)
        return selected_tab, name, accepted


app = App()
app.mainloop()