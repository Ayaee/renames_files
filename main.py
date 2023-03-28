import pathlib as pl
import lucidity
import shutil


import conf


def function_choice():
    choice = input("Comment voulez vous renomer vos fichier ? (Ecrivez votre choix\n"
          "En faisant un  'save', en copiant les fichiers renommer dans un nouveau dossier et en conservant l'ancien ?\n"
          "En faisant un 'check', en copiant les fichiers renommer dans un nouveau dossier et si le fichier est bien existant supprimer l'ancien, puis l'ancien dossier ?\n"
          "En faisant un 'rename', en reonommant les fichiers directement dans le même dossier et écrasant les ancien ?\n")
    print(choice)

    list_choice = ["save", "check", "rename"]

    if choice not in list_choice:
        raise RenameFailure(f"Erreur: Le nom saisie ne correspond à aucun choix donné. Nom saisie : '{choice}'")

    else:
        rename = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr

    rename_files(choice, rename)


def rename_files(choice, rename):

    img_template = lucidity.Template("rename_template", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    print("Je suis la")

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    folder_existing_not_empty = check_existing_not_empty(conf.root_img_before)

    if folder_existing_not_empty:
        for img in conf.root_img_before.iterdir():
            template_data = img_template.parse(str(img))
            frame = template_data['frame']

            rename_path = (conf.root_img_after / f"{rename}.{frame}.exr")
            print(choice)

            if choice == "save" or choice == "check":
                try:
                    shutil.copy2(img, rename_path)

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu permettre de copier {rename_path}: {exc}")

                if choice == 'check':
                    file_existing = check_existing(rename_path)

                    if file_existing:
                        img.unlink()

            elif choice == "rename":
                try:
                    img.replace(rename_path)
                    # img.rename(rename_path)

                except FileExistsError as exc:
                    raise RenameFailure(f"Le fichier renommé {rename_path} existe déjà")

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu renommer le fichier {img}: {exc}")

            else:
                raise RenameFailure("Erreur")


def check_existing_not_empty(folder):
    """
    Fonction permettant de vérifier si le dossier choisit par l'utilisateur est bien existant, est bien un dossier et non un fichier et contient bien des fichiers pour être renommés

    :param folder: Dossier contenant les fichiers à renommer
    :return: True si le dossier est existant n'est pas un fichier et contient bien des fichiers, sinon raise une erreur selon la situation
    """
    if folder.exists() and not folder.is_file():
        if not list(folder.iterdir()):

            raise RenameFailure("Erreur: Le dossier dans lequel vous cherchez est vide.")

        else:
            return True

    else:
        raise RenameFailure(f"Erreur: Le dossier dans lequel les fichiers sont n'a pas été trouvé. {folder}")


def check_existing(file):
    file_path = pl.Path(file)

    if not file_path.is_file():

        raise RenameFailure(f"Erreur: Le fichier {file} ne semble pas avoir été correctement copier dans le dossier")

    else:
        return True


class RenameFailure(Exception):
    pass


if __name__ == '__main__':
    print(function_choice())

    # folder = conf.root_img_before
    # print(empty(folder))

    # file = "D:/TD5/Code_Externe/renames_files/after/test.0662.exr"
    # print(check_existing(file))
