from tool_box import *

def mount_union(ctx):
    cfg = ctx.config()
    union_mntroot = cfg.union_mntroot()
    testdir = cfg.testdir()
    if cfg.testing_none():
        lower_mntroot = cfg.lower_mntroot()
        system("mount -o bind " + lower_mntroot + " " + union_mntroot)
        ctx.note_upper_fs(lower_mntroot, testdir, testdir)

    else:
        lower_mntroot = cfg.lower_mntroot()
        upper_mntroot = cfg.upper_mntroot()
        snapshot_mntroot = cfg.snapshot_mntroot()
        if cfg.should_mount_upper():
            system("mount " + upper_mntroot + " 2>/dev/null"
                    " || mount -t tmpfs upper_layer " + upper_mntroot)
        layer_mntroot = upper_mntroot + "/" + ctx.curr_layer()
        upperdir = layer_mntroot + "/u"
        workdir = layer_mntroot + "/w"
        nested_mntroot = upper_mntroot + "/n"
        nested_upper = upper_mntroot + "/u"
        nested_work = upper_mntroot + "/w"
        try:
            os.mkdir(layer_mntroot)
            if cfg.is_nested():
                os.mkdir(nested_mntroot)
        except OSError:
            system("rm -rf " + upper_mntroot + "/*")
            os.mkdir(layer_mntroot)
            if cfg.is_nested():
                os.mkdir(nested_mntroot)
        # Create unique fs for upper/0 if maxfs > 0
        if cfg.maxfs() > 0:
            system("mount -t tmpfs " + ctx.curr_layer() + "_layer " + layer_mntroot)
        os.mkdir(upperdir)
        os.mkdir(workdir)
        if not cfg.testing_snapshot():
            # Create pure upper file
            write_file(upperdir + "/f", "pure");
        if cfg.is_nested():
            os.mkdir(nested_upper)
            os.mkdir(nested_work)

        if cfg.testing_snapshot():
            mnt = snapshot_mntroot
            mntopt = " -oindex=on,nfs_export=on,redirect_dir=origin"
        else:
            mnt = union_mntroot
            mntopt = " -orw" + cfg.mntopts()
        if cfg.is_nested():
            nested_mntopt = mntopt
            if cfg.is_verify():
                nested_mntopt = mntopt + ",nfs_export=on"
            system("mount -t " + cfg.fstype() + " nested_layer " + nested_mntroot + nested_mntopt + ",lowerdir=" + lower_mntroot + ",upperdir=" + nested_upper + ",workdir=" + nested_work)
            lower_mntroot = nested_mntroot
            ctx.note_lower_fs(lower_mntroot)
        system("mount -t " + cfg.fstype() + " " + cfg.fsname() + " " + mnt + mntopt +
               ",lowerdir=" + lower_mntroot + ",upperdir=" + upperdir + ",workdir=" + workdir)
        if cfg.testing_snapshot():
            snapmntopt = " -onoatime,snapshot=" + snapshot_mntroot
            system("mount -t snapshot " + lower_mntroot + " " + union_mntroot + snapmntopt)
            ctx.note_upper_fs(lower_mntroot, testdir, testdir)
        else:
            # Record st_dev of merge dir and pure upper file
            ctx.note_upper_fs(upper_mntroot, testdir, union_mntroot + "/f")
        ctx.note_lower_layers(lower_mntroot)
        ctx.note_upper_layer(upperdir)
