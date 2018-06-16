# Based on Ryu project load_module_utils

import os
import sys
import six
import inspect
import importlib
import project
import namespace_utils as ns
from mininet.topo import ( SingleSwitchTopo, LinearTopo,
                           SingleSwitchReversedTopo, MinimalTopo )
from mininet.topolib import TreeTopo, TorusTopo
from mininet.util import buildTopo

def load_source(name, pathname):
    """
    This function provides the backward compatibility for 'imp.load_source'
    in Python 2.

    :param name: Name used to create or access a module object.
    :param pathname: Path pointing to the source file.
    :return: Loaded and initialized module.
    """
    if six.PY2:
        import imp
        return imp.load_source(name, pathname)
    else:
        loader = importlib.machinery.SourceFileLoader(name, pathname)
        return loader.load_module(name)


def chop_py_suffix(p):
    for suf in ['.py', '.pyc', '.pyo']:
        if p.endswith(suf):
            return p[:-len(suf)]
    return p

def _import_module_file(path):
    abspath = os.path.abspath(path)
    # Backup original sys.path before appending path to file
    original_path = list(sys.path)
    sys.path.append(os.path.dirname(abspath))
    modname = chop_py_suffix(os.path.basename(abspath))
    try:
        return load_source(modname, abspath)
    finally:
        # Restore original sys.path
        sys.path = original_path

def import_module(modname):
    if os.path.exists(modname):
        try:
            # Try to import module since 'modname' is a valid path to a file
            # e.g.) modname = './path/to/module/name.py'
            return _import_module_file(modname)
        except SyntaxError:
            # The file didn't parse as valid Python code, try
            # importing module assuming 'modname' is a Python module name
            # e.g.) modname = 'path.to.module.name'
            return importlib.import_module(modname)
    else:
        # Import module assuming 'modname' is a Python module name
        # e.g.) modname = 'path.to.module.name'
        return importlib.import_module(modname)


def load_topo_hosts():
    # FIXME: default_topos should get from 'mn' in mininet project 
    TOPODEF = 'minimal'
    TOPOS = { 'minimal': MinimalTopo,
            'linear': LinearTopo,
            'reversed': SingleSwitchReversedTopo,
            'single': SingleSwitchTopo,
            'tree': TreeTopo,
            'torus': TorusTopo }
    default_topos = TOPOS.keys()

    # load mn args
    args = project.read_args()

    # get target topo
    target = TOPODEF
    for x in args:
        index = x.find('topo=')
        if index is not -1:
            target = x[index+5:]
            break
    
    if not project.custom_path:
        raise Exception('project has not been initialized!!')

    try:
        mod = import_module(project.custom_path)
        custom_topo = dict(inspect.getmembers(mod))['topos']
        TOPOS.update(custom_topo)
    except:
        # This happens when the custom file does not be provided. Use default topology.
        pass
    
    # Try to build topology and get hosts list
    try:
        topo = buildTopo( TOPOS, target )
    except:
        raise Exception('{} topology is unavailable!'.format(target))
    return topo.hosts(sort=True)
