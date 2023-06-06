import customtkinter as ctk
import pathlib as pl
import lucidity
import shutil

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
    Fonction servant à créer le template à partir de la variable du pattern créer dans la 'old_conf.py' puis à récupérer la frame et l'extension du fichier

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

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Rename")
        self.add("Copy")

        # add widgets on tabs
        self.select_folder_source_rename = ctk.CTkButton(master=self.tab("Rename"),
                                                  text="Choose the original folder containing the files",
                                                  command=self.get_folder_source_rename,
                                                  fg_color="#2D8664",
                                                  hover_color="#194D2A")
        self.select_folder_source_rename.place(relx=0.5, rely=0.3, anchor="center")


        self.select_folder_source_copy = ctk.CTkButton(master=self.tab("Copy"),
                                                       text="Choose the original folder containing the files",
                                                       command=self.get_folder_source_copy,
                                                       fg_color="#2D8664",
                                                       hover_color="#194D2A")
        self.select_folder_source_copy.place(relx=0.5, rely=0.3, anchor="center")

        self.select_folder_copy = ctk.CTkButton(master=self.tab("Copy"),
                                                text="Choose the folder in which the files will be copied and renamed",
                                                command=self.get_folder_copy,
                                                fg_color="#2D8664",
                                                hover_color="#194D2A")
        self.select_folder_copy.place(relx=0.5, rely=0.5, anchor="center")

        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(master=self.tab("Copy"),
                                        text="Delete original folder",
                                        variable=self.checkbox_var,
                                        fg_color="#2D8664",
                                        hover_color="#194D2A")
        self.checkbox.place(relx=0.5, rely=0.7, anchor="center")

    def get_folder_source_rename(self):
        str_folder_source = ctk.filedialog.askdirectory()
        self.folder_source = pl.Path(str_folder_source).resolve()
        self.folder_copy = pl.Path(str_folder_source).resolve()
        print("Selected folder source:", self.folder_source)
        return self.folder_source, self.folder_copy

    def get_folder_source_copy(self):
        str_folder_source = ctk.filedialog.askdirectory()
        self.folder_source = pl.Path(str_folder_source).resolve()
        print("Selected folder source:", self.folder_source)
        return self.folder_source

    def get_folder_copy(self):
        str_folder_copy = ctk.filedialog.askdirectory()
        self.folder_copy = pl.Path(str_folder_copy).resolve()
        print("Selected folder copy:", self.folder_copy)
        return self.folder_copy

    def get_checkbox_value(self):
        return self.checkbox_var.get()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sequence Renamer")
        self.geometry("700x570")

        ctk.set_appearance_mode("dark")
        #ctk.set_default_color_theme("green")

        self.label = ctk.CTkLabel(master=self,
                                  text="Write the new name you want to assign to the files")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.name_entry = ctk.CTkEntry(master=self)
        self.name_entry.place(relx=0.5, rely=0.17, anchor="center")

        self.label_top = ctk.CTkLabel(master=self,
                                      text="Do you want to rename the original files or save them and rename a copy of the files")
        self.label_top.place(relx=0.5, rely=0.31, anchor="center")

        self.tab_view = MyTabView(master=self,
                                  segmented_button_selected_color="#2D8664",
                                  segmented_button_selected_hover_color="#194D2A")
        self.tab_view.place(relheight=0.4, relwidth=0.8, relx=0.5, rely=0.55, anchor="center")

        self.button = ctk.CTkButton(self,
                                    text="Execute",
                                    command=self.button_callback,
                                    fg_color="#2D8664",
                                    hover_color="#194D2A")
        self.button.place(relx=0.5, rely=0.82, anchor="center")

    def button_callback(self):
        name = self.name_entry.get()
        selected_tab = self.tab_view.get()
        accepted = self.tab_view.get_checkbox_value()
        print("Name:", name)
        print("Selected tab:", selected_tab)
        print("Accepted:", accepted)
        if self.tab_view.folder_copy is None:
            rename_files(self.tab_view, selected_tab, name, accepted)
        else:
            rename_files(self.tab_view, selected_tab, name, accepted)


app = App()
app.mainloop()
