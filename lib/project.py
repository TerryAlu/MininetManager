import os

## const. variable
MNM_ENV_NAME = 'MNM_HOME'
MNM_HOME_DEF = '/var/run/mnm'

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
