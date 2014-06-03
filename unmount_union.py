from settings import *
from tool_box import *

def unmount_union():
    system("umount " + union_mntroot)
    check_not_tainted()

    if testing_overlayfs:
        system("umount " + upper_mntroot)
        check_not_tainted()

    system("umount " + lower_mntroot)
    check_not_tainted()
