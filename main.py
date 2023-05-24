import pathlib as pl
import lucidity
import shutil

from conf import conf, templates


def function_choice():
    """
    Fonction principale servant à demander à l'utilisateur s'il veut renommer ou copier les fichiers, ainsi que le nom qu'il souhaitera leur donner
    La fonction appelle ensuite celle qui servira à réaliser le renommage

    :return: Le choix de l'utilisateur pour la procédure et le nouveau nom
    """
    choice = input("Voulez vous directement 'rename' vos fichier dans le dossier existant ou alors les 'copy' dans un nouveau dossier pour les renommer ?\n"
                   "Écrivez 'rename' ou 'copy' selon votre choix\n")

    list_choice = ["copy", "rename"]

    if choice not in list_choice:
        raise RenameFailure(f"Erreur: Le nom saisie ne correspond à aucun choix donné. Nom saisie : '{choice}'")

    else:
        rename = input("Quel sera le nouveau nom de vos différentes frames ?\n")

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    rename_files(choice, rename)


def rename_files(choice, rename):
    """
    Fonction servant à réaliser les différentes manières de renommer les fichiers voulu
    copy = copie les fichiers dans un nouveau dossier en les renommant (possibilité d'effacer ou nom l'ancien dossier après vérification)
    rename = renomme les fichiers directement dans le même dossier

    :param choice : Choix effectué par l'utilisateur sur la manière de renommer
    :param rename : Nouveau nom donné au fichier
    :return: Les fichiers renommer selon la méthode choisit
    """
    folder_existing_not_empty = check_existing_not_empty(conf.root_img_before)
    delete = function_delete(choice)

    if folder_existing_not_empty:
        for img in conf.root_img_before.iterdir():
            frame, extension = get_data_template(img)

            if choice == "copy":
                rename_path = (conf.root_img_after / f"{rename}.{frame}.{extension}")

                try:
                    shutil.copy2(img, rename_path)

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu permettre de copier {rename_path}: {exc}")

                if delete == "yes":
                    file_existing = check_existing(rename_path)

                    if file_existing:
                        img.unlink()

                    if not list(conf.root_img_before.iterdir()):
                        conf.root_img_before.rmdir()
                    else:
                        continue

                else:
                    continue

            elif choice == "rename":
                rename_path = (conf.root_img_before / f"{rename}.{frame}.{extension}")

                try:
                    img.rename(rename_path)

                except FileExistsError:
                    raise RenameFailure(f"Le fichier renommé {rename_path} existe déjà")

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu renommer le fichier {img}: {exc}")

            else:
                raise RenameFailure("Erreur dans la procedure de renommage")


def function_delete(choice):
    """
    Fonction servant à demander à l'utilisateur si préfère supprimer ou non l'ancien dossier
    (Seulement quand celui-ci à choisie l'option 'copy')

    :param choice: Choix effectué par l'utilisateur sur la manière de renommer
    :return: Le choix effectué par l'utilisateur pour savoir s'il désire supprimer l'ancien dossier
    """
    if choice == "copy":
        delete = input("Voulez vous supprimer l'ancien dossier ?\n"
                       "Écrivez 'yes' ou 'no' selon votre choix\n")

        list_delete = ["yes", "no"]

        if delete not in list_delete:
            raise RenameFailure(f"Erreur: Le mot saisie ne correspond à aucun des deux choix donnés. Nom saisie : '{delete}'")

        return delete


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
        raise RenameFailure(f"Le fichier {img} ne correspond à aucun templates donné dans le fichier 'templates.py' veuillez le rajouter")


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


if __name__ == '__main__':
    print(function_choice())
