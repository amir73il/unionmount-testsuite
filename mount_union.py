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
        if cfg.is_samefs():
            base_mntroot = cfg.base_mntroot()
            system("mount -o remount,rw " + base_mntroot)
            try:
                os.mkdir(base_mntroot + upper_mntroot)
            except OSError:
                pass
            system("mount -o bind " + base_mntroot + upper_mntroot + " " + upper_mntroot)
        else:
            system("mount " + upper_mntroot + " 2>/dev/null"
                    " || mount -t tmpfs upper_layer " + upper_mntroot)
        upperdir = upper_mntroot + "/" + ctx.curr_layer()
        workdir = upper_mntroot + "/work" + ctx.curr_layer()
        try:
            os.mkdir(upperdir)
            os.mkdir(workdir)
        except OSError:
            system("rm -rf " + upper_mntroot + "/*")
            os.mkdir(upperdir)
            os.mkdir(workdir)
        system("mount -t overlay overlay " + "/share" +
               " -olowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
        system("exportfs -va")
        system("mount -t nfs localhost:/share " + union_mntroot)
        ctx.note_upper_fs(upper_mntroot, testdir)
        ctx.note_lower_layers(lower_mntroot)
        ctx.note_upper_layer(upperdir)
