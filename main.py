import os
import pathlib as pl
import shutil
import sys

import lucidity

import conf


def rename_copy_before_save():
    """
    Fonction servant à renommer les fichiers dans 'before' pour les copier intégralement dans 'after'.
    Cette fonction ne supprime pas le dossier 'before' et garde les deux dossiers.

    :return: La totalité des fichiers dans 'before' renommée comme désirée dans 'after'
    """
    img_template = lucidity.Template("rename", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    name = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr

    if name.strip() == "":
        sys.exit("Erreur: Le nom saisie est vide et ne contient aucun caractère")

    for img in conf.root_img_before.iterdir():
        img = str(img)
        template_data = img_template.parse(img)
        frame = template_data['frame']

        rename = (conf.root_img_after / f"{name}.{frame}.exr")

        shutil.copy2(img, rename)


def RenameFailure(Exception):
    pass


if __name__ == '__main__':
    print(rename_copy_before_save())
