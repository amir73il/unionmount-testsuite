#
# Create and set up a lower layer for the test scripts to use
#
from settings import *
from tool_box import *
import os, shutil

def set_up():
    os.sync()

    # Discard anything already mounted on the mountpoint to avoid contamination
    # as unionmount tries to collect all the mounts located there into the
    # union.
    if testing_unionmount:
        while system("umount " + union_mntroot):
            pass

    # Create a lower layer to union over
    system("mount -t tmpfs lower_layer " + lower_mntroot)

    # Systemd has weird ideas about things
    system("mount --make-private " + lower_mntroot)

    #
    # Create a few test files we can use in the lower layer
    #
    os.mkdir(lowerdir)

    for i in range(100, 130):
        # Under the test directory, we create a bunch of regular files
        # containing data called foo100 to foo129:
        fd = open(lowerdir + "/foo" + str(i), "w")
        fd.write(":xxx:yyy:zzz")
        del fd

        # Then we create a bunch of direct symlinks to those files
        os.symlink("../a/foo" + str(i), lowerdir + "/direct_sym" + str(i))

        # Then we create a bunch of indirect symlinks to those files
        os.symlink("direct_sym" + str(i), lowerdir + "/indirect_sym" + str(i))

        # Then we create a bunch symlinks that don't point to extant files
        os.symlink("no_foo" + str(i), lowerdir + "/pointless" + str(i))

        # We create a bunch of directories, each with an empty file
        os.mkdir(lowerdir + "/dir" + str(i))
        fd = open(lowerdir + "/dir" + str(i) + "/a", "w")
        del fd

        # And add direct and indirect symlinks to those
        os.symlink("../a/dir" + str(i), lowerdir + "/direct_dir_sym" + str(i))
        os.symlink("direct_dir_sym" + str(i), lowerdir + "/indirect_dir_sym" + str(i))

        # And a bunch of empty directories
        os.mkdir(lowerdir + "/empty" + str(i))

        # Everything above is then owned by the bin user
        for f in [ "foo", "direct_sym", "indirect_sym", "pointless" ]:
            os.lchown(lowerdir + "/" + f + str(i), 1, 1)

        # Create some root-owned regular files also
        fd = open(lowerdir + "/roofile" + str(i), "w")
        fd.write(":xxx:yyy:zzz")
        del fd

    # The mount has to be read-only for us to make use of it
    system("mount -o remount,ro " + lower_mntroot)
