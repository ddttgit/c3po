# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import subprocess
import shutil
import re

# -- Project construction -----------------------------------------------------

# Add C3PO sources into the PATH environment variable.
sys.path.insert(0, os.path.abspath('../../sources'))

# Get the current working directory.
current_path = os.path.dirname(os.path.abspath(__file__))

# Set temporary directory where C3PO sources will be copied.
tmp_path = current_path+"/../tmp"

# Copies C3PO sources if tmp directory does not exist.
if not os.path.isdir(tmp_path):
    shutil.copytree(current_path+"/../../sources/", tmp_path, dirs_exist_ok=True)

# Generates all the .rst files from C3PO sources.
subprocess.run(["sphinx-apidoc", "-fe", "-o", current_path, tmp_path, "--templatedir="+current_path+"/_apidoc_templates/"], capture_output=True)

# Add copied C3PO sources into the PATH environment variable.
sys.path.insert(0, os.path.abspath(tmp_path))

def scan(path, workdir):
    """
    Parameters
    ----------
    path : str
        Absolute path of the C3PO sources.
    workdir : str
        Absolute path of the documentation sources.

    Returns
    -------
    tuple(list[str], list[str])
        Returns the tuple (list_py,list_dir), with:
        - list_py : A list of absolute paths of all the Python files that C3PO sources contain (in a
          list list_py).
        - list_dir : A list of absolute paths of all the directories that C3PO sources contain (in a
          list list_dir).
    """
    list_py = []
    list_dir = []

    for name in os.listdir(path):
        path_name = path + "/" + name
        if os.path.isfile(path_name):
            if os.path.splitext(path_name)[-1] == ".py" and name != "__init__.py":
                list_py.append(path_name)
        if os.path.isdir(path_name):
            if name != "__pycache__" and name != "c3po.egg-info":
                modulepathdir = workdir+"/"+name
                if not os.path.isdir(modulepathdir):
                    os.mkdir(modulepathdir)
                list_dir.append(path_name)
                files, dirs = scan(path_name, modulepathdir)
                list_py += files
                list_dir += dirs

    return list_py, list_dir

# Scan C3PO sources.
# Saves absolute path of all the Python files that C3PO sources contain (in a list list_py).
# Saves absolute path of all the directories that C3PO sources contain (in a list list_dir).
# Reproduces the tree structure of C3PO sources into the documentation directory.
list_py, list_dir = scan(sys.path[0], current_path)

dict_class = {}

# Loops over the Python files
for file in list_py:
    # Gets the relative path of each Python file. It looks like "c3po/<path-to-file>".
    # It cuts the file extension.
    pathfile = os.path.splitext(file.replace(sys.path[0]+"/",""))[0]

    # Gets the parent directory of the file.
    pathdir = "/".join(pathfile.split("/")[:-1])

    # Tranforms the path synthax "<path>/<to>/<the>/<file>" into "<path>.<to>.<the>.<file>".
    # The new synthax corresponds to the one of .rst files created by the command "sphinx-apidoc".
    # Moves .rst file to the good location into the tree structure of the documentation.
    rst = ".".join(pathfile.split("/"))
    shutil.move(current_path+"/"+rst+".rst", pathdir+"/"+rst+".rst")

    # Scans the content of each Python files and extract the name of all the classes.
    # <file_name1> : [<class1>, <class2>, ...]
    # <file_name2> : [...]
    # ...
    with open(tmp_path+"/"+pathfile+".py", "r") as file:
        content = file.readlines()
        r = re.compile("^class ")
        newlist = list(filter(r.match, content))
        for i in range(len(newlist)):
            newlist[i] = re.search(r"\s\w+[(|:]",newlist[i]).group()[1:-1]
    dict_class[rst] = newlist

sourceInit = None
listLoadModule = []

for d in list_dir:
    # Gets the relative path of each directory. It looks like "c3po/<path-to-directory>".
    # Transforms the path synthax "<path>/<to>/<the>/<directory>" into "<path>.<to>.<the>.<directory>".
    # Moves .rst file to the good location into the tree structure of the documentation.
    pathfile = d.replace(os.path.abspath(tmp_path)+"/","")
    pathdir = current_path+"/"+"/".join(pathfile.split("/")[:-1])
    rst = ".".join(pathfile.split("/"))+".rst"
    shutil.move(current_path+"/"+rst, pathdir+"/"+rst)

    if d.split("/")[-1] == 'c3po':
        sourceInit = d

# Scans the file tmp/c3po/__init__.py
# Checks if all the modules are loaded by this file.
# If not, adds the line
# from <file_name> import <class1>, <class2>, ...
alreadyload = []
with open(sourceInit+"/__init__.py", "r") as file:
    content = file.readlines()
    for line in content:
        splitline = line.split()
        if splitline and splitline[0] == 'from':
            alreadyload.append(splitline[1])

with open(sourceInit+"/__init__.py", "a") as file:
    for key in dict_class.keys():
        add = True
        for mod in alreadyload:
            if mod in key:
                add = False
                break
        if add:
            file.write('from {} import {}\n'.format(key, ", ".join(dict_class[key])))
                    
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'C3PO documentation'
copyright = '2025, TMA-GRP4'
author = 'TMA-GRP4'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx'
]

graphviz_output_format = 'svg'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'mpi4py': ('https://mpi4py.readthedocs.io/en/stable/', None)
    }

autodoc_mock_imports = ["CATHARE2SWIG", "CATHARE3SWIG", "Access", "FlicaICoCo",
                        "trusticoco", "MEDconvert", "MEDtsetpt", "pleiades",
                        "pleiadesMPI", "Alcyone2Init", "mpi4py", "medcoupling",
                        "MEDLoader", "c3po.medcouplingCompat"]

if os.getenv("DATADIR") == None:
    autodoc_mock_imports.append("c3po.physicsDrivers.FLICA4Driver")
elif not (os.path.isfile(os.path.join(os.getenv("DATADIR"), "flica4_static.dat")) or
    os.path.isfile(os.path.join(os.getenv("DATADIR"), "flica4_transient.dat"))):

    autodoc_mock_imports.append("c3po.physicsDrivers.FLICA4Driver")

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_theme_options = {'sidebarwidth': 450}
html_static_path = ['_static']
