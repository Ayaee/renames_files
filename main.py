import pathlib as pl
import lucidity
import shutil


import conf


def function_choice():
    """
    Fonction principale servant à demander à l'utilisateur la manière dont il veut réaliser son renommage de fichiers ainsi que le nom qu'il désirera donner
    La fonction appelle ensuite celle qui servira à réaliser le renommage

    :return: Le choix de l'utilisateur pour la procédure et le nouveau nom
    """
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

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    rename_files(choice, rename)


def rename_files(choice, rename):
    """
    Fonction servant à réaliser les différentes manière de renommer les fichiers voulu, trois manière existantes
    save = copie les fichiers dans un nouveau dossier en les renommant et garde l'ancien dossier avec les anciens fichiers
    check = copie les fichiers dans un nouveau dossier en les renommant si le fichier est bien transféré et renommer supprimer l'ancien fichier et si l'ancien dossier est finalement vide le supprime également
    rename = renomme les fichiers directement dans le même dossier

    :param choice: Choix effectué par l'utilisateur sur la manière de renommer
    :param rename: Nouveau nom donné au fichiers
    :return: Le résultat d'une des trois méthode du renommage
    """
    folder_existing_not_empty = check_existing_not_empty(conf.root_img_before)

    if folder_existing_not_empty:
        for img in conf.root_img_before.iterdir():
            frame, extension = get_data_pattern(img)


            if choice == "save" or choice == "check":
                rename_path = (conf.root_img_after / f"{rename}.{frame}.{extension}")

                try:
                    shutil.copy2(img, rename_path)

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu permettre de copier {rename_path}: {exc}")

                if choice == 'check':
                    file_existing = check_existing(rename_path)

                    if file_existing:
                        img.unlink()

                    if not list(conf.root_img_before.iterdir()):
                        conf.root_img_before.rmdir()
                    else:
                        continue

            elif choice == "rename":
                rename_path = (conf.root_img_before / f"{rename}.{frame}.{extension}")

                try:
                    img.rename(rename_path)

                except FileExistsError as exc:
                    raise RenameFailure(f"Le fichier renommé {rename_path} existe déjà")

                except Exception as exc:
                    raise RenameFailure(f"Une erreur n'a pas pu renommer le fichier {img}: {exc}")

            else:
                raise RenameFailure("Erreur dans la procedure de renommage")


def get_data_pattern(img):
    """
    Fonction servant à créer le template à partir de la variable du pattern créer dans la 'conf.py' puis à récupérer la frame et l'extension du fichier

    :param img: Fichier traité qui est en train de se faire renommer
    :return: La frame et l'extension du fichier traité, ou raise une  erreur si le template n'est pas en adéquation avec le pattern créer
    """
    img_template = lucidity.Template("rename_template", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    try:
        template_data = img_template.parse(str(img))
        frame = template_data['frame']
        extension = template_data['extension']

        return frame, extension

    except lucidity.error.ParseError as exc:
        raise RenameFailure(f"Le fichier {img} ne correspond pas au template pattern donné dans le fichier 'conf.py' veuillez le modifier")


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
