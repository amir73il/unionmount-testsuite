#
# Class of object containing current test configuration
#

__copyright__ = """
Copyright (C) 2014 Red Hat, Inc. All Rights Reserved.
Written by David Howells (dhowells@redhat.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public Licence version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public Licence for more details.

You should have received a copy of the GNU General Public Licence
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import os

class config:
    def __init__(self, progname):
        self.__progname = progname
        self.__testing_overlayfs = False
        self.__testing_snapshot = False
        self.__testing_none = False
        self.__base_mntroot = os.getenv('UNIONMOUNT_BASEDIR')
        self.__lower_mntroot = os.getenv('UNIONMOUNT_LOWERDIR')
        self.__union_mntroot = os.getenv('UNIONMOUNT_MNTPOINT')
        print("Environment variables:")
        if self.__base_mntroot:
            print("UNIONMOUNT_BASEDIR=" + self.__base_mntroot)
        if self.__lower_mntroot:
            print("UNIONMOUNT_LOWERDIR=" + self.__lower_mntroot)
        if self.__union_mntroot:
            print("UNIONMOUNT_MNTPOINT=" + self.__union_mntroot)
        print()
        if self.__base_mntroot and not self.__lower_mntroot:
            # Empty UNIONMOUNT_LOWERDIR with non-empty UNIONMOUNT_BASEDIR imply --samefs
            # unless user requests maxfs=<N>
            self.__maxfs = -1
        else:
            self.__maxfs = 0
        self.__verbose = False
        self.__verify = False
        self.__squashfs = False
        self.__metacopy = False
        self.__nested = False
        self.__xino = False
        self.__mntopts = ""
        self.__fusefs = False
        self.__fstype = "overlay"
        self.__fsname = "overlay"

    def progname(self):
        return self.__progname

    def testing_none(self):
        return self.__testing_none
    def testing_overlayfs(self):
        return self.__testing_overlayfs
    def testing_snapshot(self):
        return self.__testing_snapshot

    def set_testing_none(self):
        self.__testing_none = True

    def set_testing_overlayfs(self):
        self.__testing_overlayfs = True

    def set_testing_snapshot(self):
        self.__testing_snapshot = True
        self.__maxfs = -1

    # base dir is used only for --ov --samefs, in which case:
    # BASEDIR/l is lowermost layer
    # BASEDIR/0/u is the first layer above it, which starts as upper layer
    # and may later be rotated to lower layers.
    # BASEDIR/m is the union mount point.
    # user provided UNIONMOUNT_BASEDIR should already be mounted.
    def should_use_base(self):
        return self.__base_mntroot or self.is_samefs() or self.testing_snapshot()
    def should_mount_base(self):
        return not self.__base_mntroot and self.should_use_base()
    def base_mntroot(self):
        return self.__base_mntroot or "/base"
    def env_base_mntroot(self):
        return self.__base_mntroot
    # lower dir is mounted ro for --ov (without --samefs) ...
    def should_mount_lower_ro(self):
        return self.testing_overlayfs() and not self.is_samefs() and not self.__lower_mntroot
    # ... and mounted rw for --no
    # user provided UNIONMOUNT_LOWERDIR should already be mounted.
    def should_mount_lower_rw(self):
        return self.testing_none() and not self.__lower_mntroot
    def should_mount_lower(self):
        return self.should_mount_lower_ro() or self.should_mount_lower_rw()
    # lowermost layer is either at UNIONMOUNT_LOWERDIR, /lower or BASEDIR/l
    def lower_mntroot(self):
        if self.__lower_mntroot:
            return self.__lower_mntroot
        if self.should_use_base():
            return self.base_mntroot() + "/l"
        return self.old_lower_mntroot()
    def old_lower_mntroot(self):
        return self.__lower_mntroot or "/lower"
    def env_lower_mntroot(self):
        return self.__lower_mntroot
    # upper dir is mounted for --ov (without --samefs)
    def should_mount_upper(self):
        return self.testing_overlayfs() and not self.is_samefs()  and not self.__base_mntroot
    # layers (0..N) above lowermost are either at /upper/N or at BASEDIR/N
    def upper_mntroot(self):
        if self.should_use_base():
            return self.base_mntroot()
        return self.old_upper_mntroot()
    def old_upper_mntroot(self):
        return self.__base_mntroot or "/upper"
    # union mount point is either at /mnt or at BASEDIR/m
    def union_mntroot(self):
        if self.__union_mntroot:
            return self.__union_mntroot
        if self.should_use_base():
            return self.base_mntroot() + "/m"
        return self.old_union_mntroot()
    def old_union_mntroot(self):
        return self.__union_mntroot or "/mnt"
    def env_union_mntroot(self):
        return self.__union_mntroot
    def snapshot_mntroot(self):
        return self.base_mntroot() + "/s"
    def backup_mntroot(self):
        return self.base_mntroot() + "/b"
    def lowerdir(self):
        return self.lower_mntroot() + "/a"
    def lowerimg(self):
        return self.lower_mntroot() + "/a.img"
    def testdir(self):
        return self.union_mntroot() + "/a"

    def set_verbose(self, to=True):
        self.__verbose = to
    def is_verbose(self):
        return self.__verbose
    def set_verify(self, to=True):
        self.__verify = to
    def is_verify(self):
        return self.__verify
    def set_maxfs(self, to):
        self.__maxfs = to
    def maxfs(self):
        return self.__maxfs
    def is_samefs(self):
        return self.__maxfs < 0
    def set_squashfs(self, to=True):
        self.__squashfs = to
    def is_squashfs(self):
        return self.__squashfs
    def set_xino(self, to=True):
        self.__xino = to
    def is_xino(self):
        return self.__xino
    def set_metacopy(self, to=True):
        self.__metacopy = to
    def is_metacopy(self):
        return self.__metacopy
    def set_nested(self, to=True):
        self.__nested = to
    def is_nested(self):
        return self.__nested

    def add_mntopt(self, opt):
        self.__mntopts += "," + opt
    def set_mntopts(self, opts):
        self.__mntopts = opts
    def mntopts(self):
        return self.__mntopts

    def fsname(self):
        return self.__fsname
    def fstype(self):
        return self.__fstype
    def set_fusefs(self, to):
        self.__fusefs = True
        self.__fsname = to
        self.__fstype = "fuse." + to
    def is_fusefs(self):
        return self.__fusefs
