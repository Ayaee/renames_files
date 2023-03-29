
# Rename Files

Création d'un tool permettant de pouvoir rename de plusieurs façons 'safe' 'check' et 'fast' une grande quantité de fichiers contenu dans un dossier, en gardant le versionning de frame (selon un template).


## Environment Variables

Pour que le script puisse fonctionner, il vous faudra le fichier 'conf.py, si le fichier n'est pas disponible veillez à l'ajouter

`root_img_before = pl.Path(__file__).resolve(strict=True).parent / "before"`
`root_img_after = pl.Path(__file__).resolve(strict=True).parent / "after"`

`rename_pattern = r"{name}.{version}.{frame}.exr"`

***Vérifier l'arborescence des path et le pattern utilisé et à les modifier si nécéssaire***


## FAQ

#### Le template n'est absolument pas compatible avec mes noms de fichiers

*Vérifier dans le fichier 'conf.py' le pattern utilisé pour créer le template et modifier le si besoin*


## Features

- ~~Création de la fonction 'check'~~
- ~~Création de la fonction 'rename'~~
- Script lançable depuis une icone desktop
- Création d'une UI
- UI permettant de choisir le dossier d'entrée
- UI permettant de choisir le dossier de sortie



## Feedback

Si vous voulez me faire des retours,  me donner des conseils ou des améliorations, n'hésitez pas à me contacter sur afabre@artfx.fr par mail ou pas Google Chat


## Authors

- [@abygaellefabre](https://github.com/Ayaee)

