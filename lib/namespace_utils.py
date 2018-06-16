# https://stackoverflow.com/questions/30127569/start-multiprocessing-process-in-namespace
from ctypes import cdll
libc = cdll.LoadLibrary('libc.so.6')
_setns = libc.setns

import os
import project
import subprocess as sp

def setns(fd, nstype=0):
    if hasattr(fd, 'fileno'):
        fd = fd.fileno()

    _setns(fd, nstype)

def get_netns_path(pid):
    assert pid
    return '/proc/%d/ns/mnt' % pid

def setns_pid(pid):
    with open(get_netns_path(pid)) as fd:
        setns(fd)

def setns_default():
    with open(get_netns_path(1)) as fd:
        setns(fd)

# find pid whose /proc/<pid>/cmdline contains string of cmdline
def find_pid(cmdline):
    assert cmdline
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
	if cmdline in open(os.path.join('/proc', pid, 'cmdline'), 'rb').read():
		return int(pid)
    return None

def find_node_pid(node_name):
    assert node_name
    return find_pid('mininet:'+node_name)

def default_hostdict():
    '''
    Return {hostname: pid} dictionary created by single, tree... topology.
    Default hosts are named h1, h2... etc.
    '''
    host_dict = {}
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            cmdline = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            index = cmdline.find('mininet:h')
            if index is not -1:
                host_dict[cmdline[index+8:].rstrip('\x00')] = int(pid)
        except:
            pass
    return host_dict

def custom_hostdict(hostlist):
    host_dict = {}
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            cmdline = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            for x in hostlist:
                index = cmdline.find('mininet:'+x)
                if index is not -1:
                    host_dict[x] = int(pid)
                    break
        except:
            pass
    return host_dict

# FIXME: Only support the directory in root directory currently. eg. /home, /etc
# /home/someuser this will be supported in the future.
def overlay_mount(hosts, target_name):
    '''
    Create the target overlay structure in project directory and overlay mount all hosts' target directory.

    @param hosts        Hosts info. in dictionary format. {host_name: host_pid}
    @param target_name  Directory name in root. eg. /home, /etc
    '''

    for host, pid in hosts.iteritems():
        try:
            # Create overlay structure in project directory
            upper_path, work_path = project.create_target_dir(host, target_name)
            target_dir = '/'+target_name

            # Try to overlay mount all hosts' target directory
            setns_pid(pid)
            sp.call('mount -t overlay overlay -o lowerdir={},upperdir={},workdir={} {}'.format(target_dir, upper_path, work_path, target_dir), shell=True)
        except Exception, e:
            print e.message
            sys.exit(1)
