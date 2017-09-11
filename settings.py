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

class config:
    def __init__(self, progname):
        self.__progname = progname
        self.__testing_unionmount = False
        self.__testing_overlayfs = False
        self.__testing_snapshot = False
        self.__testing_none = False
        self.__base_mntroot = None
        self.__lower_mntroot = None
        self.__upper_mntroot = None
        self.__union_mntroot = None
        self.__snapshot_mntroot = None
        self.__backup_mntroot = None
        self.__verbose = False
        self.__verify = False
        self.__samefs = False
        self.__squashfs = False

    def progname(self):
        return self.__progname
        
    def testing_none(self):
        return self.__testing_none
    def testing_unionmount(self):
        return self.__testing_unionmount
    def testing_overlayfs(self):
        return self.__testing_overlayfs
    def testing_snapshot(self):
        return self.__testing_snapshot

    def set_testing_none(self):
        self.__lower_mntroot = "/lower"
        self.__union_mntroot = "/mnt"
        self.__testing_none = True

    def set_testing_unionmount(self):
        self.__lower_mntroot = "/mnt"
        self.__union_mntroot = "/mnt"
        self.__testing_unionmount = True

    def set_testing_overlayfs(self):
        self.__base_mntroot = "/base"
        self.__lower_mntroot = "/lower"
        self.__upper_mntroot = "/upper"
        self.__union_mntroot = "/mnt"
        self.__testing_overlayfs = True

    def set_testing_snapshot(self):
        self.__base_mntroot = "/base"
        self.__lower_mntroot = "/lower"
        self.__upper_mntroot = "/upper"
        self.__union_mntroot = "/mnt"
        self.__backup_mntroot = "/backup"
        self.__snapshot_mntroot = self.__backup_mntroot + "/snapshot"
        self.__testing_snapshot = True
        self.__testing_none = True
        self.__samefs = True

    def base_mntroot(self):
        return self.__base_mntroot
    def lower_mntroot(self):
        return self.__lower_mntroot
    def upper_mntroot(self):
        return self.__upper_mntroot
    def union_mntroot(self):
        return self.__union_mntroot
    def snapshot_mntroot(self):
        return self.__snapshot_mntroot
    def backup_mntroot(self):
        return self.__backup_mntroot
    def lowerdir(self):
        return self.__lower_mntroot + "/a"
    def lowerimg(self):
        return self.__lower_mntroot + "/a.img"
    def testdir(self):
        return self.__union_mntroot + "/a"

    def set_verbose(self, to=True):
        self.__verbose = to
    def is_verbose(self):
        return self.__verbose
    def set_verify(self, to=True):
        self.__verify = to
    def is_verify(self):
        return self.__verify
    def set_samefs(self, to=True):
        self.__samefs = to
    def is_samefs(self):
        return self.__samefs
    def set_squashfs(self, to=True):
        self.__squashfs = to
    def is_squashfs(self):
        return self.__squashfs
