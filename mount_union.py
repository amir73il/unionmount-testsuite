from settings import *
from tool_box import *

def mount_union(ctx):
    if testing_unionmount:
        system("/root/util-linux-union/mount/mount -i -t tmpfs upper_layer " +
               union_mntroot + " -o union")
        ctx.note_upper_fs(testdir, testdir)

        if ctx.lower_fs() == ctx.upper_fs():
            raise TestError("Upper (" + ctx.upper_fs() + " and lower (" + ctx.lower_fs() +
                            ") shouldn't be the same")

    else:
        system("mount -t tmpfs upper_layer " + upper_mntroot)
        upperdir = upper_mntroot + "/upper"
        workdir = upper_mntroot + "/work"
        os.mkdir(upperdir)
        os.mkdir(workdir)
        system("mount -t overlayfs overlayfs " + union_mntroot +
               " -olowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
        ctx.note_upper_fs(upper_mntroot, testdir)
