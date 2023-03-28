import shutil
<<<<<<< Updated upstream
import sys
=======
import pathlib as pl
>>>>>>> Stashed changes

import lucidity

import conf


def copy_and_save(rename):
    """
    Fonction servant à renommer les fichiers dans 'before' pour les copier intégralement dans 'after'.
    Cette fonction ne supprime pas le dossier 'before' et garde les deux dossiers.

    :param rename: Nom choisit par l'utilisateur pour renommer les fichiers
    :return: La totalité des fichiers dans 'before' renommée comme désirée dans 'after'
    """
    # rename = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr
    img_template = lucidity.Template("rename", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    folder_existing_not_empty = check_existing_not_empty(conf.root_img_before)

    if folder_existing_not_empty:
        for img in conf.root_img_before.iterdir():
            template_data = img_template.parse(str(img))
            frame = template_data['frame']

            rename_path = (conf.root_img_after / f"{rename}.{frame}.exr")

            try:
                shutil.copy2(img, rename_path)

            except Exception as exc:
                raise RenameFailure(f"Une erreur n'a pas pu permettre de copier {rename_path}: {exc}")


def copy_and_check(rename):
    """
    Fonction servant à renommer les fichiers dans 'before' pour les copier intégralement dans 'after'.
    Cette fonction supprime les fichiers copiés un par un et le dossier 'before' à la fin.

    :param rename: Nom choisit par l'utilisateur pour renommer les fichiers
    :return: La totalité des fichiers dans 'before' renommée comme désirée dans 'after' et suppression des anciens fichiers et du dossier 'before'
    """
    img_template = lucidity.Template("rename", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    folder_existing_not_empty = check_existing_not_empty(conf.root_img_before)

    if folder_existing_not_empty:
        for img in conf.root_img_before.iterdir():
            template_data = img_template.parse(str(img))
            frame = template_data['frame']

            rename_path = (conf.root_img_after / f"{rename}.{frame}.exr")

            try:
                shutil.copy2(img, rename_path)

            except Exception as exc:
                raise RenameFailure(f"Une erreur n'a pas pu permettre de copier {rename_path}: {exc}")

            file_existing = check_existing(rename_path)

            if file_existing:
                img.unlink()


def rename_and_crush(rename):
    """
    Fonction servant à renommer les fichiers dans 'before'.
    Cette fonction renommer l'intégralité des fichiers et écraser l'ancien nom.

    :param rename:
    :return:
    """
    img_template = lucidity.Template("rename", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    folder_existing_not_empty = check_existing_not_empty(conf.root_img_before)

    if folder_existing_not_empty:
        for img in conf.root_img_before.iterdir():
            template_data = img_template.parse(str(img))
            frame = template_data['frame']

            rename_path = (conf.root_img_after / f"{rename}.{frame}.exr")

            try:
                img.replace(rename_path)
                # img.rename(rename_path)

            except FileExistsError as exc:
                raise RenameFailure(f"Le fichier renommé {rename_path} existe déjà")

            except Exception as exc:
                raise RenameFailure(f"Une erreur n'a pas pu renommer le fichier {img}: {exc}")

            continue



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
    rename = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr
    # print(copy_and_save(rename))
    # print(copy_and_check(rename))
    print((rename_and_crush(rename)))

    # folder = conf.root_img_before
    # print(empty(folder))

    # file = "D:/TD5/Code_Externe/renames_files/after/test.0662.exr"
    # print(check_existing(file))
