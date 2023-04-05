import lucidity


templates = [
lucidity.Template('exr', '{name}.{version}.{frame}.{extension}', anchor=lucidity.Template.ANCHOR_END),
    lucidity.Template('ass', '{name}.{frame}.{extension}', anchor=lucidity.Template.ANCHOR_END)
    ]