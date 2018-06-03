# https://stackoverflow.com/questions/30127569/start-multiprocessing-process-in-namespace

from ctypes import cdll
libc = cdll.LoadLibrary('libc.so.6')
_setns = libc.setns

import os

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
