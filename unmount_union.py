from tool_box import *

def unmount_union(ctx):
    cfg = ctx.config()
    system("umount " + cfg.union_mntroot())
    check_not_tainted()

    if cfg.should_mount_lower():
        system("umount " + cfg.lower_mntroot())
        check_not_tainted()

    if cfg.testing_overlayfs():
        # unmount individual layers with maxfs > 0
        if cfg.maxfs() > 0 or cfg.is_nested():
            try:
                system("umount " + cfg.upper_mntroot() + "/* 2>/dev/null")
            except RuntimeError:
                pass
            check_not_tainted()

    if cfg.should_mount_base():
        system("umount " + cfg.base_mntroot())
        check_not_tainted()
    elif cfg.should_mount_upper():
        system("umount " + cfg.upper_mntroot())
        check_not_tainted()
