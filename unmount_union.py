from tool_box import *

def unmount_union(ctx):
    cfg = ctx.config()
    system("umount " + cfg.union_mntroot())
    check_not_tainted()

    if cfg.testing_snapshot():
        system("umount " + cfg.snapshot_mntroot())
        check_not_tainted()

    if cfg.testing_overlayfs() or cfg.testing_snapshot():
        if cfg.is_samefs():
            system("umount " + cfg.base_mntroot())
            check_not_tainted()
        # unmount individual layers with maxfs > 0
        if cfg.maxfs() > 0:
            try:
                system("umount " + cfg.upper_mntroot() + "/* 2>/dev/null")
            except RuntimeError:
                pass
        check_not_tainted()
        system("umount " + cfg.upper_mntroot())
        check_not_tainted()

    system("umount " + cfg.lower_mntroot())
    check_not_tainted()
