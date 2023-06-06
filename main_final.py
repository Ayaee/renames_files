import tkinter as tk
import pathlib as pl
import lucidity
import shutil

from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle
from conf import templates


def rename_files(my_tab_view, selected_tab, name, accepted):
    """
    Fonction servant à réaliser les différentes manières de renommer les fichiers voulu
    copy = copie les fichiers dans un nouveau dossier en les renommant (possibilité d'effacer ou nom l'ancien dossier après vérification)
    rename = renomme les fichiers directement dans le même dossier

    :param choice : Choix effectué par l'utilisateur sur la manière de renommer
    :param rename : Nouveau nom donné au fichier
    :return: Les fichiers renommer selon la méthode choisit
    """
    folder_source = my_tab_view.folder_source
    folder_copy = my_tab_view.folder_copy

    folder_existing_not_empty = check_existing_not_empty(folder_source)

    if folder_existing_not_empty:
        for img in folder_source.iterdir():
            frame, extension = get_data_template(img)

            if selected_tab == "Copy":
                rename_path = (folder_copy / f"{name}.{frame}.{extension}")

                try:
                    shutil.copy2(img, rename_path)

                except FileNotFoundError:
                    raise RenameFailure(
                        f"Le dossier {folder_copy} dans lequel vous voulez copier les fichiers n'a pas été trouvé")

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu permettre de copier {rename_path}: {exc}")

                if accepted:
                    file_existing = check_existing(rename_path)

                    if file_existing:
                        img.unlink()

                    if not list(folder_source.iterdir()):
                        folder_source.rmdir()
                    else:
                        continue

                else:
                    continue

            elif selected_tab == "Rename":
                rename_path = (folder_source / f"{name}.{frame}.{extension}")

                try:
                    img.rename(rename_path)

                except FileExistsError:
                    raise RenameFailure(f"Le fichier renommé {rename_path} existe déjà")

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu renommer le fichier {img}: {exc}")

            else:
                raise RenameFailure("Erreur dans la procedure de renommage")


def get_data_template(img):
    """
    Fonction servant à créer le template à partir de la variable du pattern créer dans la 'conf.py' puis à récupérer la frame et l'extension du fichier

    :param img : Fichier traité qui est en train de se faire renommer
    :return: La frame et l'extension du fichier traité, ou raise une erreur si le template n'est pas en adéquation avec les templates créer
    """
    try:
        template_data = lucidity.parse(str(img), templates.templates)
        template_data = dict(template_data[0])
        frame = template_data['frame']
        extension = template_data['extension']

        return frame, extension

    except lucidity.error.ParseError:
        raise RenameFailure(
            f"Le fichier {img} ne correspond à aucun templates donné dans le fichier 'templates.py' veuillez le rajouter")


def check_existing_not_empty(folder_source):
    """
    Fonction permettant de vérifier si le dossier choisit par l'utilisateur est bien existant, est bien un dossier et non un fichier et contient bien des fichiers pour être renommés

    :param folder: Dossier contenant les fichiers à renommer
    :return: True si le dossier est existant n'est pas un fichier et contient bien des fichiers, sinon raise une erreur selon la situation
    """
    if folder_source.exists() and not folder_source.is_file():
        if not list(folder_source.iterdir()):

            raise RenameFailure(f"Erreur: Le dossier {folder_source} dans lequel vous cherchez est vide.")

        else:
            return True

    else:
        raise RenameFailure(
            f"Erreur: Le dossier {folder_source} dans lequel les fichiers devraient être n'a pas été trouvé. ")


def check_existing(file):
    """
    Fonction vérifiant que le fichier renommé soit bien existant dans le nouveau dossier

    :param file: Fichier qui est en train d'être copié et renommé
    :return: True si le fichier est bien existant, sinon raise une erreur pour indiquer que le fichier n'a pas été correctement copié
    """
    file_path = pl.Path(file)

    if not file_path.is_file():

        raise RenameFailure(f"Erreur: Le fichier {file} ne semble pas avoir été correctement copier dans le dossier")

    else:
        return True


class RenameFailure(Exception):
    pass


##############
##    UI    ##
##############

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
        browse_button = tk.Button(parent, text="Choose the original folder containing the files",
                                  command=self.get_browse_folder)
        browse_button.pack(pady=10, padx=10)

    def get_browse_folder(self):
        str_folder_source = filedialog.askdirectory()
        self.folder_source = pl.Path(str_folder_source).resolve()
        print("Selected folder copy:", self.folder_source)
        return self.folder_source

    def create_copy_tab(self):
        copy_frame = self.tab2

        # Create a button to select the folder copy
        browse_button_copy = tk.Button(copy_frame, text="Choose the folder in which the files will be copied and renamed",
                                       command=self.get_browse_folder_copy)
        browse_button_copy.pack(pady=10, padx=10)

        # Create a checkbox
        self.checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(copy_frame, text="Delete original folder",
                                  variable=self.checkbox_var)
        checkbox.pack(pady=10)

    def get_browse_folder_copy(self):
        str_folder_copy = filedialog.askdirectory()
        self.folder_copy = pl.Path(str_folder_copy).resolve()
        print("Selected folder copy:", self.folder_copy)
        return self.folder_copy

    def get_selected_tab(self):
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        return tab_text


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sequence Renamer")
        self.geometry("750x400")

        style = ThemedStyle(self)
        style.set_theme("black")

        # Create a container frame
        container = tk.Frame(self)
        container.pack(padx=20, pady=20)

        # Create a label
        label = tk.Label(container,
                         text="Write the new name you want to assign to the files")
        label.pack(pady=10)

        # Create an entry for capturing user's name
        self.name_entry = tk.Entry(
            container)  # Utilisation de self pour rendre la variable accessible à toute la classe
        self.name_entry.pack(pady=10)

        # Create a label
        label = tk.Label(container,
                         text="Do you want to rename the original files or save them and rename a copy of the files?")
        label.pack(pady=10)

        # Create MyTabView
        self.tab_view = MyTabView(container)
        self.tab_view.pack()

        self.button = tk.Button(self, text="Execute", command=self.button_callback)
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
        rename_files(self.tab_view, selected_tab, name, accepted)


app = App()
app.mainloop()
