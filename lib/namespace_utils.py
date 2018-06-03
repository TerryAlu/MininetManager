# https://stackoverflow.com/questions/30127569/start-multiprocessing-process-in-namespace
from ctypes import cdll
libc = cdll.LoadLibrary('libc.so.6')
_setns = libc.setns

import os
import project

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

# FIXME: Only support the directory in root directory currently. eg. /home, /etc
# /home/someuser this will be supported in the future.
def overlay_mount(host_name, target_name):
    project.create_target_dir(host_name, target_name)
    
    '''
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
    '''
