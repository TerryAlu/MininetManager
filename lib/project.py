import os

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
