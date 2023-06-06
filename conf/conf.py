import pathlib as pl


root_img_before = pl.Path(__file__).resolve(strict=True).parent.parent / "before"
root_img_after = pl.Path(__file__).resolve(strict=True).parent.parent / "after"

rename_pattern = r"{name}.{version}.{frame}.{extension}"


if __name__ == '__main__':
    print(type(root_img_before))
    print(root_img_after)