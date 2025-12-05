# Prérequis Python

- c3po
- graphviz
- sphinx
- sphinx-rtd-theme

# Contenu du répertoire doc/

Ce répertoire contient :

- Makefile
- requirements.txt
- source/

## Le fichier Makefile

Permet de lancer la commande "make html" pour générer la documentation de C3PO.

Pour supprimer le répertoire de compilation "build", on peut lancer la commande :

```bash
make clean
```

ou

```bash
rm -r build/
```

## Le fichier requirements.txt

Contient les versions des prérequis nécessaires pour générer les documentations C3PO et ReadTheDoc.

## Le répertoire source/

Le répertoire "source/" contient :

- code\_integration.rst
    Contient le chapitre "How to use a code with C3PO".

- mainpage.rst
    Contient le chapitre "C3PO documentation".

- index.rst
    Fichier principal de la documentation. Contient la table des matières principale de la
    documentation.

- conf.py
    Script de configuration du projet Sphinx.

- \_apidoc\_templates/
    Répertoire qui contient les templates des fichiers .rst du projet Sphinx.

Les fichiers .rst sont générés automatiquement par la commande "make html" via le script de
configuration "conf.py".


