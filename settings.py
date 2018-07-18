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
        self.__testing_overlayfs = False
        self.__testing_none = False
        self.__base_mntroot = None
        self.__lower_mntroot = None
        self.__upper_mntroot = None
        self.__union_mntroot = None
        self.__verbose = False
        self.__verify = False
        self.__maxfs = 0
        self.__squashfs = False
        self.__xino = False
        self.__mntopts = ""
        self.__fs = "overlay"

    def progname(self):
        return self.__progname

    def testing_none(self):
        return self.__testing_none
    def testing_overlayfs(self):
        return self.__testing_overlayfs

    def set_testing_none(self):
        self.__lower_mntroot = "/lower"
        self.__union_mntroot = "/mnt"
        self.__testing_none = True

    def set_testing_overlayfs(self):
        self.__base_mntroot = "/base"
        self.__lower_mntroot = "/lower"
        self.__upper_mntroot = "/upper"
        self.__union_mntroot = "/mnt"
        self.__testing_overlayfs = True

    def base_mntroot(self):
        return self.__base_mntroot
    def lower_mntroot(self):
        return self.__lower_mntroot
    def upper_mntroot(self):
        return self.__upper_mntroot
    def union_mntroot(self):
        return self.__union_mntroot
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

    def add_mntopt(self, opt):
        self.__mntopts += "," + opt
    def set_mntopts(self, opts):
        self.__mntopts = opts
    def mntopts(self):
        return self.__mntopts

    def fs(self):
        return self.__fs
    def set_fs(self, to):
        self.__fs = to
