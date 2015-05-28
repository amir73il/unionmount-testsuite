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
        self.__testing_none = False
        self.__lower_mntroot = None
        self.__upper_mntroot = None
        self.__union_mntroot = None
        self.__verbose = False

    def progname(self):
        return self.__progname
        
    def testing_none(self):
        return self.__testing_none
    def testing_unionmount(self):
        return self.__testing_unionmount
    def testing_overlayfs(self):
        return self.__testing_overlayfs

    def set_testing_none(self):
        self.__lower_mntroot = "/lower"
        self.__union_mntroot = "/mnt"
        self.__testing_none = True

    def set_testing_unionmount(self):
        self.__lower_mntroot = "/mnt"
        self.__union_mntroot = "/mnt"
        self.__testing_unionmount = True

    def set_testing_overlayfs(self):
        self.__lower_mntroot = "/lower"
        self.__upper_mntroot = "/upper"
        self.__union_mntroot = "/mnt"
        self.__testing_overlayfs = True

    def lower_mntroot(self):
        return self.__lower_mntroot
    def upper_mntroot(self):
        return self.__upper_mntroot
    def union_mntroot(self):
        return self.__union_mntroot
    def lowerdir(self):
        return self.__lower_mntroot + "/a"
    def testdir(self):
        return self.__union_mntroot + "/a"

    def set_verbose(self, to=True):
        self.__verbose = to
    def is_verbose(self, to=True):
        return self.__verbose
