import os
import pathlib as pl
import shutil
import sys

import lucidity

import conf


def copy_before_save(rename):
    """
    Fonction servant à renommer les fichiers dans 'before' pour les copier intégralement dans 'after'.
    Cette fonction ne supprime pas le dossier 'before' et garde les deux dossiers.

    :return: La totalité des fichiers dans 'before' renommée comme désirée dans 'after'
    """
    # rename = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr
    img_template = lucidity.Template("rename", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    if rename.strip() == "":
        raise RenameFailure(f"Erreur: Le nom saisie est vide et ne contient aucun caractères. Nom saisie : '{rename}'")

    folder_existing = existing(conf.root_img_before)

    if folder_existing:
        for img in conf.root_img_before.iterdir():
            img = str(img)
            template_data = img_template.parse(img)
            frame = template_data['frame']

            rename_path = (conf.root_img_after / f"{rename}.{frame}.exr")

            shutil.copy2(img, rename_path)


def existing(folder):

    if folder.exists():

        return True

    else:
        raise RenameFailure(f"Erreur: Le dossier dans lequel les fichiers sont n'a pas été trouvé. {folder}")


def empty(folder):
    
    pass


class RenameFailure(Exception):
    pass


if __name__ == '__main__':
    # rename = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr
    # print(copy_before_save(rename))

    folder = conf.root_img_before
    print(empty(folder))
