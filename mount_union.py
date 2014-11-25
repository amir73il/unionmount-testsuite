from tool_box import *

def mount_union(ctx):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    testdir = cfg.testdir()
    if cfg.testing_none():
        lower_mntroot = cfg.lower_mntroot()
        system("mount -o remount,rw " + lower_mntroot)
        system("mount -o bind " + lower_mntroot + " " + union_mntroot)
        ctx.note_upper_fs(lower_mntroot, testdir)

    elif cfg.testing_unionmount():
        system("/root/util-linux-union/mount/mount -i -t tmpfs upper_layer " +
               union_mntroot + " -o union")
        ctx.note_upper_fs(testdir, testdir)

        if ctx.lower_fs() == ctx.upper_fs():
            raise TestError("Upper (" + ctx.upper_fs() + " and lower (" + ctx.lower_fs() +
                            ") shouldn't be the same")

    else:
        lower_mntroot = cfg.lower_mntroot()
        upper_mntroot = cfg.upper_mntroot()
        system("mount -t tmpfs upper_layer " + upper_mntroot)
        upperdir = upper_mntroot + "/upper"
        workdir = upper_mntroot + "/work"
        os.mkdir(upperdir)
        os.mkdir(workdir)
        system("mount -t overlay overlay " + union_mntroot +
               " -olowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
        ctx.note_upper_fs(upper_mntroot, testdir)
