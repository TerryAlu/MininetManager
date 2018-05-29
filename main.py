import os
import sys
import inspect
import subprocess

from mininet.util import ensureRoot

## add lib from ./lib
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/lib')
#print sys.path
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
#print mn_cmd

'''
mnm_home = MNM_HOME_DEF
print mnm_home

'''

# TODO: save arguments
# print sys.argv

def gen_upperdir(route, hosts):
    for host in hosts:
        project.create_dir(route + "/" + host)
    
    return

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--file',
                       default='topo.py',
                       help='input mininet python script name')
    parser.add_argument('--project',
                       default='Project1',
                       help='input project name')
    parser.add_argument('--host',
                       default='h1',
                       help='input host name')
    args = parser.parse_args()

    # get host name
    host_names = args.host.split(",")

    # generate mnm workspace for first use
    project.create_dir(MNM_HOME_DEF)

    # generate project directory
    project_dir = MNM_HOME_DEF + "/" + args.project
    project.create_dir(project_dir)

    # generate upperdir for each host
    gen_upperdir(project_dir, host_names)

    ensureRoot()

    # test find host pid
    for host in host_names:
        print host + "-pid: " + ns.find_node_pid(host)

    print os.path.abspath('topo.py')
    print lm.load_topos("topo.py")
