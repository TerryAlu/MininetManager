import os
import sys
import inspect
import subprocess
import argparse

from mininet.util import ensureRoot

#print sys.path
import lib.namespace_utils as ns
import lib.load_module_utils as lm
import lib.project as project

## const. variable
MN_CMD = 'mn'

## global variables
mn_cmd = list(sys.argv)
mn_cmd[0] = MN_CMD
#print mn_cmd

# TODO: save arguments
# print sys.argv

def gen_upperdir(route, hosts):
    for host in hosts:
        project.create_dir(route + "/" + host)
    
    return

def check_args(args):
    if not args.project:
        print '--project argument can not be empty'
        return False
    return True


if __name__ == '__main__':

    ensureRoot()

    parser = argparse.ArgumentParser()
    parser.add_argument('--project',
                       help='input project name')
    args = parser.parse_args()

    if not check_args(args):
        sys.exit(1)

    # try to create mnm home dir
    project.init_project(args)
    print project.read_args()

    ns.overlay_mount('h1', 'home')

