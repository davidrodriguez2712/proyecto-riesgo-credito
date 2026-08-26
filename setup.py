from pathlib import Path
import sys
import os
import json


CURRENT_DIRECTORY = Path.cwd()

## Creación de carpetas
Path('./artifacts').mkdir(exist_ok= True, parents= True)
Path('./artifacts/eda').mkdir(exist_ok= True, parents= True)
Path('./artifacts/feature_engineering').mkdir(exist_ok= True, parents= True)
Path('./artifacts/training_model').mkdir(exist_ok= True, parents= True)
Path('./artifacts/model_evaluation').mkdir(exist_ok= True, parents= True)
Path('./artifacts/monitoring').mkdir(exist_ok= True, parents= True)
#Path('./artifacts/metadata').mkdir(exist_ok= True, parents= True)
Path('./artifacts/eda/tables').mkdir(exist_ok= True, parents= True)
Path('./artifacts/eda/figures').mkdir(exist_ok= True, parents= True)
Path('./data').mkdir(exist_ok= True, parents= True)
Path('./data/raw').mkdir(exist_ok= True, parents= True)
Path('./data/external').mkdir(exist_ok= True, parents= True)
Path('./data/interim').mkdir(exist_ok= True, parents= True)
Path('./data/processed').mkdir(exist_ok= True, parents= True)
Path('./backend').mkdir(exist_ok= True, parents= True)
Path('./frontend').mkdir(exist_ok= True, parents= True)
Path('./notebooks').mkdir(exist_ok= True, parents= True)

## Creación de archivos
Path('./params.yaml').touch(exist_ok= True)
Path('./README.md').touch(exist_ok= True)
Path('./.gitignore').touch(exist_ok= True)
Path('./.env').touch(exist_ok= True)

Path('./backend/Dockerfile').touch(exist_ok= True)
Path('./backend/requirements.txt').touch(exist_ok= True)

Path('./frontend/Dockerfile').touch(exist_ok= True)
Path('./frontend/requirements.txt').touch(exist_ok= True)

notebook = {
    "cells": [],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 5
}

with open("./notebooks/01_eda.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

with open("./notebooks/02_feature_engineering.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

with open("./notebooks/03_training_model.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

with open("./notebooks/04_model_evaluation.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

with open("./notebooks/05_monitoring.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)

#print(CURRENT_DIRECTORY)














