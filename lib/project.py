import os
import sys
from shutil import copyfile

## const. variable
MNM_ENV_NAME = 'MNM_HOME'
MNM_HOME_DEF = '/var/mnm'

mnm_home_dir = os.environ.get(MNM_ENV_NAME, MNM_HOME_DEF)

def exist_dir(dir_path):
    return os.path.exists(dir_path)

def exist_file(file_path):
    return os.path.isfile(file_path)

# create directory if not exist
def create_dir(dir_path, ignore_exist=True):
    try:
        os.makedirs(dir_path)
    except:
        if ignore_exist:
            return
        raise Exception(dir_path+' has been existed!')

def create_mnm_home():
    create_dir(mnm_home_dir)

def create_project_dir():
    global project_path
    try:
        create_dir(project_path, False)
    except Exception as err:
        print err
        # sys.exit(1)

# create upper and work directory for /<target_name> in virtual host
def create_target_dir(host_name, target_name):
    global project_path
    host_path = project_path+'/'+host_name
    upper_path = host_path+'/'+target_name
    work_path = host_path+'/'+target_name+'_work'
    create_dir(host_path)
    create_dir(upper_path)
    create_dir(work_path)
    return (upper_path, work_path)

# convert args list to string and write to the file
def write_args(args):
    global args_path
    with open(args_path, 'w') as argsfile:
        str_args = ' '.join(args)
        argsfile.write(str_args)

def read_args():
    global args_path
    with open(args_path, 'r') as argsfile:
        return argsfile.read().split()

def copy_custom(path):
    global custom_path
    copyfile(path, custom_path)

# call this after getting project name
def init_project(args):
    global project_path
    project_path = mnm_home_dir+'/'+args.project
    global args_path
    args_path = project_path+'/args'
    # custom path is fixed in the project
    global custom_path
    custom_path = project_path+'/custom.py'

    create_mnm_home()
    if not args.l:
        create_project_dir()
