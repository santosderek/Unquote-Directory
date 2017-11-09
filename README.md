# Unquote-Directory
Unquote a directory of filenames with url encoding.

***

***Example:*** %5bThis%20is%20a%20title%5d.txt -> [This is a title].txt

### How to install:

*** Repository developed in Python 3.6.x ***

*Copy repository from github:*

    git clone https://github.com/santosderek/Unquote-Directory/

*Move into repository*

    cd Unquote-Directory

*Install Python Package*

    python3 setup.py install

*Congrats, it's installed! Now you can proceed bellow*

***

### How to use:
#### Following commands can be used:
***Base command:***

    unquote [path/to/directory]

***Help page***

*View the help page*

    unquote --help

***Unquote Through All Sub-Directories***

    unquote -r [path/to/directory] | OR | unquote --recursion [path/to/directory]
