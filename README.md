# Mininet Manager

MininetManager is an extension of Mininet.
MininetManager allows us to modify some files under /home but not effect other hosts.
Besides, it saves changes of files in the project directory.
Therfore, we can load the topology with the changes of files.


## How does it work?

MininetManager create a project under `$MNM_HOME`. If `$MNM_HOME` is not set, then `/var/mnm` will be used.
MininetManager passes arguments to `mn` and creates topology. After the topology has been created, MininetManager overlay mounts the directory according to mount.json. Mount point for each host can be specified here, the default mount point is directory `/home`.


## Example

`$ sudo ./mnm --project=myproject --custom=./custom.py --topo=mytopo --mntpath=mount.json`

```
*** Creating network
*** Adding controller
*** Adding hosts:
hh1 hh2
*** Adding switches:
s1
*** Adding links:
(hh1, s1) (hh2, s1)
*** Configuring hosts
hh1 hh2
*** Starting controller
c0
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet> hh1 touch /home/<username>/<somefiles>
```

`/home/<username>/<somefiles>` only appears in the hh1 host!

## Usage

`$ sudo ./mnm --project=<project_name> [-l] [--custom=<custom_file>] [--mntpath=<mount_point_file>]`

* --project
  * project name
* -l
  * load project. If this flag is set, then mininet arguements and custom file will be loaded from the project.
* --custom
  * path to the custom file. The custom file will be copied to the project.
* --mntpath
  * a json file specifies mount points for each host
  * the default mount point is set to `/home`