# Project Overview:

This application, designed to be executed on the CLI, manages CRUD function for a pop up cafe business to log and track customer orders and information. Data is persisted using MySQL and Adminer. 

## How to run: 

miniprojectfinal.py is the main file. Once in the correct directory:

### 1. Ensure docker is installed and running by typing the following command into the terminal:

$ docker -v 

### 2. Run the following command inside the directory

$ docker-compose up -d 

### 3. Activate the virtual environment

Windows:
$ source venv/Scripts/activate

MacOS/Unix:
$ source venv/bin/activate

### 4. Install the requirements:

pip3 install -r requirements.txt

### 5. Run the Unit tests:

py -m pytest test_app_functions.py

### 5. Run the app and follow terminal instructions:

uncomment lines 1569-1572

Windows:
$ py miniprojectfinal.py

MacOS/Unix:
$ python3 miniprojectfinal.py
