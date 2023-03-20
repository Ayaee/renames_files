import os
import pathlib as pl
import shutil

import lucidity

import conf


def transfer_img():
    img_template = lucidity.Template("rename", conf.rename_pattern, anchor=lucidity.Template.ANCHOR_END)

    name = input("Quel sera le nouveau nom de vos différentes frames ?\n")  # masterlayer.0230.exr

    for img in conf.root_img_before.iterdir():

        img = str(img)
        template_data = img_template.parse(img)
        frame = template_data['frame']

        rename = (conf.root_img_after / f"{name}.{frame}.exr")

        shutil.copy2(img, rename)


if __name__ == '__main__':
    print(transfer_img())
