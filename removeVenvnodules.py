import os
import shutil

def delete_directories(path):
    for root, dirs, files in os.walk(path):
        if 'venv' in dirs:
            shutil.rmtree(os.path.join(root, 'venv'))
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
        if 'node_modules' in dirs:
            shutil.rmtree(os.path.join(root, 'node_modules'))

delete_directories('.')