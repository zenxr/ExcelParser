# Excel Parser

Brady Howard asked for this, I'm not providing maintenance on it. Bug him if he spreads the app around and it isn't stable anymore!

### Application structure

* `config.py` - configuration file; has FilePath, and etc.
* `Pipfile` and `Pipfile.lock` - Used by pipenv to sandbox this application. All dependencies are stored only in the pipenv, so different users don't have to bother with managing package versions, configuration, and etc.
* `README.md` - the file responsible for showing the currently displayed text.
* `__init__.py` - app's root file; almost all code logic occurs here.
* `./templates` - (mostly) html template files

## Config.py

Configuration of the application is done in this file. Specifies where to look for the excel file.

* `ExcelFilePath` - relative path to the excile file. ("./" means current directory)
* `SheetToParse` - the excel sheet to parse. Change it if the sheet name changes. Could configure the application to use all sheets later if need arises
* `ColumnNamesToSearch` - Each column added here should be a present column in the sheet. A search field is generated for each column.
* `PageTitle` - set the window title if  you'd like, because why not (mostly because I didn't have a good name)
* `OpenBrowser` - set to True or False if you want the default web browser to automatically launch to the server.

## Requirements and Installation

This is made in Python3.7. It uses pipenv, which handles resolving dependencies and ensures this application is sandboxed in its own environment.

**Software Requirements**
* Grab Python3.7 (and pip, though it may come with python3.7)
* Grab *pipenv* via `pip3 install pipenv` if its not already installed. (try pipenv in terminal/cmd)

**Installation**
* Clone the repository
* Open shell/CMD inside of the cloned repository folder (where __init__.py lives)
* `pipenv install --dev` will install all of the packages needed.

Congratulations, installation complete!
## Running

Make sure to set up the configuration file as needed. 

Specifically, the `ExcelFilePath` variable *must* be set correctly. Default: "./Files/micro .xlsx" (suggest leaving the default, place your file there with that name)

* `pipenv run python __init__.py`

This will start a web server on `127.0.0.1:5000`, open it in a web browser. (I've automated that, but without making the code asyncronous you'll probably have to refresh once it opens.)

You can access it via any device on the same network as you, so long as you know your LAN IP (`ipconfig -all` in Windows CMD; `ifconfig` on most Linux distros, I don't know OSX's command). If you choose to do so, you could leave this running and port forward on your router to this address; but there's no built in security or proper infrastructure.

## Architecture

* `Flask` - web framework used
* `pandas` - module used for parsing excel data
* `bootstrap` - handles website styling and supplies prebuilt classes. Resides in `./static/css` and `./static/js`

# Contributing

Cody Stephenson July 20th, 2019. I don't really plan on maintaining this. Feel free to grab it and modify.
