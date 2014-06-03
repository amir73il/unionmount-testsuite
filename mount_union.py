from settings import *
from tool_box import *

def mount_union():
    if testing_unionmount:
        system("/root/util-linux-union/mount/mount -i -t tmpfs upper_layer " +
               union_mntroot + " -o union")
        os.sync()

        upper_fs = get_dev_id(testdir)
        if lower_fs == upper_fs:
            raise RuntimeError("Upper (" + upper_fs + " and lower (" + lower_fs +
                               ") shouldn't be the same")

    else:
        system("mount -t tmpfs upper_layer " + upper_mntroot)
        upperdir = upper_mntroot + "/upper"
        workdir = upper_mntroot + "/work"
        os.mkdir(upperdir)
        os.mkdir(workdir)
        system("mount -t overlayfs overlayfs " + union_mntroot +
               " -olowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
        
