import os
import sys
import inspect
import subprocess

from mininet.util import ensureRoot

## add lib from ./lib
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/lib')
print sys.path
import namespace_utils as ns
import load_module_utils as lm
import project 

## const. variable
MNM_ENV_NAME = 'MNM_HOME'
MN_CMD = 'mn'
MNM_HOME_DEF = '/var/run/mnm'

## global variables
mn_cmd = list(sys.argv)
mn_cmd[0] = MN_CMD
# print mn_cmd

print ns.find_node_pid('h1')

mnm_home = MNM_HOME_DEF
print mnm_home

ensureRoot()

print 'try to create mnm home'
project.create_dir(mnm_home)

# print os.path.abspath('../custom.py')
# print lm.load_topos("../custom.py")

# print os.environ['HOME']
# print os.environ.get(MNM_ENV_NAME, None)

# TODO: save arguments
# print sys.argv


