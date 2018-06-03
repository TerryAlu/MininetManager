import os
import sys
import inspect
import subprocess
import argparse

from mininet.util import ensureRoot

## add lib from ./lib
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/lib')
#print sys.path
import namespace_utils as ns
import load_module_utils as lm
import project 
from project import MNM_ENV_NAME
from project import MNM_HOME_DEF

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
    '''
    Check whether the key args exist
    '''

    if not args.project or not args.custom or not args.topo:
        print '--project, --custom and --topo argument can not be empty'
        return False

    if not os.path.isfile(args.custom):
        print 'custom file', args.custom, 'can not be found'
        return False

    return True


if __name__ == '__main__':

    ensureRoot()

    parser = argparse.ArgumentParser()
    parser.add_argument('--custom',
                       help='input mininet python script name')
    parser.add_argument('--project',
                       help='input project name')
    parser.add_argument('--topo',
                       help='input topology name')
    args = parser.parse_args()

    # if not check_args(args):
        # sys.exit(1)

    # try to create mnm home dir
    mnm_home_dir = os.environ.get(MNM_ENV_NAME, MNM_HOME_DEF)
    project.create_dir(MNM_HOME_DEF)

    ## XXX: just for testing
    work_dir = '/tmp/work'
    upper_dir = '/tmp/upper'
    target_dir = '/home' # lower & mount point
    
    # remove and create work & upper dir
    try:
        subprocess.call('rm -rf {}'.format(work_dir))
    except:
        pass
    project.create_dir(work_dir)

    try:
        subprocess.call('rm -rf {}'.format(upper_dir))
    except:
        pass
    project.create_dir(upper_dir)

    # enter h1 mount namespace
    h1_pid = ns.find_node_pid('h1')
    try:
        ns.setns_pid(h1_pid)
    except:
        print 'You need to start a mininet topology with a node named h1. eg. sudo mn'
        sys.exit(1)

    print 'h1 pid: {}'.format(h1_pid)
    print 'mount -t overlay overlay -o lowerdir={},upperdir={},workdir={} {}'.format(target_dir, upper_dir, work_dir, target_dir)

    # overlay mount
    subprocess.call('mount -t overlay overlay -o lowerdir={},upperdir={},workdir={} {}'.format(target_dir, upper_dir, work_dir, target_dir), shell=True)

    print 'Done'
    print '============================\n'
    print 'You can check it work with the following commands.\n'
    print '\t1. sudo nsenter -t {} -n -m'.format(h1_pid)
    print '\t2. findmnt\n'
    print '{} is mounted by overlayfs\n'.format(target_dir)


    # generate project directory
    # project_dir = MNM_HOME_DEF + "/" + args.project
    # project.create_dir(project_dir)

    # generate upperdir for each host
    # gen_upperdir(project_dir, host_names)


    # test find host pid
    # for host in host_names:
        # print host + "-pid: " + ns.find_node_pid(host)

    # print os.path.abspath('topo.py')
    # print lm.load_topos("topo.py")
