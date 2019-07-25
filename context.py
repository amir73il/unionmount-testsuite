#
# Class of object containing current test state
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

from tool_box import *
from remount_union import remount_union
import sys, os, errno
from stat import *
from enum import IntEnum

# None value is for lower
class upper(IntEnum):
    META=1
    DATA=2

class inode:
    def __init__(self, filetype, symlink_val=None, symlink_to=None):
        assert(filetype != None)
        assert(filetype != "s" or symlink_val)
        self.__filetype = filetype
        self.__symlink_val = symlink_val
        self.__symlink_to = symlink_to

    def filetype(self):
        return self.__filetype

    def sym_val(self):
        return self.__symlink_val

    def sym_target(self):
        return self.__symlink_to

class dentry:
    def __init__(self, name, inode=None, root=False, layer=None, on_upper=None):
        self.__name = name
        self.__parent = None
        self.created(inode, layer, on_upper)

    # By default created objects are pure upper
    def created(self, inode, layer, on_upper=upper.DATA):
        self.__i = inode
        self.__failed_create = False
        self.__children = dict()
        self.__is_dir = inode and inode.filetype() == "d"
        self.__layer = layer
        self.__upper = on_upper
        self.__rename_exdev = not on_upper

    def failed_to_create(self):
        if self.__i == None:
            self.__failed_create = True

    def clear(self):
        assert(self.__i != None)
        self.__i = None
        self.__children = dict()

    def name(self):
        return self.__name

    def filename(self):
        if self.__parent == None:
            return ""
        return self.__parent.filename() + "/" + self.__name

    def inode(self):
        return self.__i

    def filetype(self):
        if self.__i:
            return self.__i.filetype()
        return None

    def is_negative(self):
        return self.__i == None

    def parent(self):
        return self.__parent

    def add_child(self, child):
        assert(child != None)
        if self.is_dir():
            self.__children[child.__name] = child
        child.__parent = self
        return child

    def look_up_child(self, name):
        if self.is_dir() and name in self.__children:
            return self.__children[name]
        return self.add_child(dentry(name, None))

    def children(self):
        return self.__children.values()

    def unlink_child(self, child):
        assert(self.is_dir())
        assert(self.__children[child.__name] == child)
        del self.__children[child.__name]
        child.__parent = None

    def unlink(self):
        if self.parent():
            self.parent().unlink_child(self)

    def did_create_fail(self):
        return self.__failed_create

    def copied_up(self, layer, copy_up=upper.META):
        if not self.__upper or layer != self.__layer or self.__upper < copy_up:
            self.__layer = layer
            self.__upper = copy_up

    def replace_with(self, src):
        old_parent = src.parent()
        new_parent = self.parent()
        miss = dentry(src.__name, None, layer = src.__layer, on_upper = src.__upper)
        old_parent.unlink_child(src)
        old_parent.add_child(miss)
        src.__name = self.__name
        new_parent.unlink_child(self)
        new_parent.add_child(src)

    def on_upper(self, layer):
        if self.__layer != layer:
            return None
        return self.__upper

    def data_on_upper(self, layer):
        return self.__layer == layer and self.__upper == upper.DATA

    def layer(self):
        if self.__upper:
            return "upper/" + str(self.__layer)
        return "lower"

    def is_dir(self):
        return self.__is_dir

    def is_reg(self):
        return self.__i.filetype() == "r"

    def is_sym(self):
        return self.__i and self.__i.filetype() == "s"

    def sym_val(self):
        return self.__i.sym_val()

    def sym_target(self):
        return self.__i.sym_target()

    def is_neg_or_sym_to_neg(self):
        if self.is_negative():
            return True
        return self.is_sym() and self.sym_target().is_neg_or_sym_to_neg()

    def is_reg_or_sym_to_reg(self):
        if self.__i.filetype() == "r":
            return True
        if not self.is_sym():
            return False
        if self.sym_target().is_negative():
            return False
        return self.sym_target().is_reg_or_sym_to_reg()

    def is_dir_or_sym_to_dir(self):
        if self.__i.filetype() == "d":
            return True
        if not self.is_sym():
            return False
        if self.sym_target().is_negative():
            return False
        return self.sym_target().is_dir_or_sym_to_dir()

    def get_exdev_on_rename(self):
        return self.__rename_exdev

###############################################################################
#
# The main test context
#
###############################################################################
class test_context:
    def __init__(self, cfg, termslash=False, direct_mode=False, recycle=False, max_layers=0, run_as=0):
        self.__cfg = cfg
        self.__root = dentry("/", inode("d"), root=True)
        self.__cwd = None
        self.__filenr = 99
        self.__layers_nr = 0
        self.__max_layers = max_layers
        self.__lower_layers = None
        self.__lower_fs = None
        self.__upper_layer = None
        self.__upper_fs = None
        self.__upper_dir_fs = None
        self.__verbose = cfg.is_verbose()
        self.__direct_mode = direct_mode
        self.__skip_layer_test = cfg.testing_none()
        self.__same_dev = cfg.is_fusefs() or cfg.is_samefs() or cfg.is_xino()
        self.__termslash = ""
        self.__recycle = recycle
        if termslash:
            self.__termslash = "/"
        self.__run_as = run_as

    def config(self):
        return self.__cfg

    def direct_mode(self):
        return self.__direct_mode

    def is_verbose(self):
        return self.__verbose

    def as_bin(self):
        if self.__run_as != 0:
            return self.__run_as
        return 1

    def verbose(self, *args):
        if self.__verbose:
            for i in args:
                sys.stdout.write(str(i))

    def verbosef(self, formatstr, *args):
        if self.__verbose:
            sys.stdout.write(formatstr.format(*args))

    def output(self, *args):
        for i in args:
            sys.stdout.write(str(i))

    def outputf(self, formatstr, *args):
        sys.stdout.write(formatstr.format(*args))

    def error(self, *args):
        sys.stderr.write(program_name + ": ")
        for i in args:
            sys.stderr.write(str(i))
        sys.exit(1)

    def errorf(self, formatstr, *args):
        error(formatstr.format(*args))

    def lstat_file(self, path):
        if path.endswith("/"):
            path = path[:len(path) - 1]
        self.verbose("os.lstat(", path, ")\n")
        return os.lstat(path)

    def is_whiteout(self, path):
        st = self.lstat_file(path)
        return S_ISCHR(st.st_mode) and st.st_rdev == 0

    def get_dev_id(self, path):
        return self.lstat_file(path).st_dev

    def get_file_ino(self, path):
        return self.lstat_file(path).st_ino

    def get_file_size(self, path):
        return self.lstat_file(path).st_size

    def get_file_blocks(self, path):
        return self.lstat_file(path).st_blocks

    def get_file_atime(self, path):
        return self.lstat_file(path).st_atime

    def get_file_mtime(self, path):
        return self.lstat_file(path).st_mtime

    # Save device ID for lower fs
    def note_lower_fs(self, path):
        self.__lower_fs = self.get_dev_id(path)

    def lower_fs(self):
        return self.__lower_fs

    # Save device IDs for upper fs
    def note_upper_fs(self, filepath, dirpath):
        self.__upper_fs = self.get_dev_id(filepath)
        if dirpath == filepath:
            self.__upper_dir_fs = self.__upper_fs
        else:
            self.__upper_dir_fs = self.get_dev_id(dirpath)

    def note_upper_layer(self, path):
        self.__upper_layer = path

    def note_lower_layers(self, lowerlayers):
        self.__lower_layers = lowerlayers

    def lower_layers(self):
        return self.__lower_layers

    def upper_layer(self):
        return self.__upper_layer

    def layers_nr(self):
        return self.__layers_nr

    def have_more_layers(self):
        return self.__layers_nr < self.__max_layers

    def have_more_fs(self):
        # /upper is same fs as /lower if maxfs < 0
        # /upper/N are all same fs (/upper) if maxfs == 0
        # /upper/N where N < maxfs are unique fs
        # /upper/N where N >= maxfs are same fs (/upper)
        return self.__layers_nr < self.config().maxfs()

    def curr_layer(self):
        return str(self.__layers_nr)

    def next_layer(self):
        if not self.have_more_layers():
            return self.curr_layer()
        self.__layers_nr += 1
        return str(self.__layers_nr)

    def upper_fs(self):
        return self.__upper_fs

    def upper_dir_fs(self):
        return self.__upper_dir_fs

    def skip_layer_test(self):
        return self.__skip_layer_test

    def same_dev(self):
        return self.__same_dev

    # Display the banner beginning the test
    def begin_test(self, source, nr, name):
        ix = source.rfind("/")
        if ix >= 0:
            source = source[ix + 1:]
        msg="TEST " + source + ":" + str(nr) + ": " + name + "\n"
        self.output(msg)
        if self.is_verbose():
            write_kmsg(msg);
        self.__filenr += 1

    # Increment the test fileset number
    def incr_filenr(self):
        self.__filenr += 1

    # Get path relative to basedir
    # Returns None if basedir is not a prefix of path
    def rel_path(self, path, basedir):
        l = len(basedir)
        if len(path) < l or path[:l] != basedir:
            return None
        return path[l:]

    # Get upper path from union path
    def upper_path(self, path):
        relpath = self.rel_path(path, self.config().union_mntroot())
        if relpath is None:
            raise TestError(path + ": not on union mount")
        return self.__upper_layer + relpath

    # Get various filenames
    def gen_filename(self, name):
        return "{:s}/{:s}{:d}".format(self.config().testdir(), name, self.__filenr)
    def no_file(self):
        return self.gen_filename("no_foo")
    def pointless(self):
        return self.gen_filename("pointless")
    def reg_file(self):
        return self.gen_filename("foo")
    def direct_sym(self):
        return self.gen_filename("direct_sym")
    def indirect_sym(self):
        return self.gen_filename("indirect_sym")
    def no_dir(self):
        return self.gen_filename("no_dir")
    def empty_dir(self):
        return self.gen_filename("empty")
    def non_empty_dir(self):
        return self.gen_filename("dir")
    def direct_dir_sym(self):
        return self.gen_filename("direct_dir_sym")
    def indirect_dir_sym(self):
        return self.gen_filename("indirect_dir_sym")
    def rootfile(self):
        # Hack for impermissible test that should be run as root
        if self.__run_as != 0:
            self.verbosef("os.seteuid(0)")
            os.seteuid(0)
            self.verbosef("os.setegid(0)")
            os.setegid(0)
            self.__run_as = 0
        return self.gen_filename("rootfile")

    # Get various symlink contents
    def gen_symlink_val(self, filename):
        (parent, dentry) = self.pathwalk(filename + str(self.__filenr), no_follow=True)
        assert(dentry.is_sym())
        return dentry.sym_val()
    def pointless_val(self):
        return self.gen_symlink_val("pointless")
    def direct_sym_val(self):
        return self.gen_symlink_val("direct_sym")
    def indirect_sym_val(self):
        return self.gen_symlink_val("indirect_sym")
    def direct_dir_sym_val(self):
        return self.gen_symlink_val("direct_dir_sym")
    def indirect_dir_sym_val(self):
        return self.gen_symlink_val("indirect_dir_sym")

    # Determine whether there should be a terminal slash
    def termslash(self):
        return self.__termslash

    ###########################################################################
    #
    # File state cache
    #
    ###########################################################################
    # Walk over a symlink
    def pathwalk_symlink(self, cursor, symlink, remnant_filename, args):
        if symlink in args["symlinks"]:
            if remnant_filename == "":
                fake_dentry = dentry(symlink.name())
                fake_dentry.failed_to_create()
                return (cursor, fake_dentry)
            raise TestError(args["orig_filename"] + ": Recursive symlink")
        args["symlinks"].add(symlink)
        content = symlink.sym_val()
        if content.startswith("/"):
            cursor = self.__root
        return self.pathwalk_one(cursor, content + remnant_filename, args)

    # Walk over the last component of a path
    def pathwalk_last(self, cursor, filename, args):
        name = filename
        if name == ".":
            return (cursor.parent(), cursor)
        if name == "..":
            return (cursor.parent().parent(), cursor.parent())

        to = cursor.look_up_child(name)
        if to.is_negative():
            pass
        elif to.is_sym() and not args["no_follow"]:
            return self.pathwalk_symlink(cursor, to, "", args)
        return (cursor, to)

    # Walk over an intermediate component of a path
    def pathwalk_one(self, cursor, filename, args):
        filename = filename.lstrip("/")
        slash = filename.find("/")
        if slash == -1:
            # The tail gets treated differently for nofollow purposes
            args["parent"] = cursor
            return self.pathwalk_last(cursor, filename, args)

        name = filename[:slash]
        if name == ".":
            return self.pathwalk_one(cursor, filename[slash:], args)
        if name == "..":
            return self.pathwalk_one(cursor.parent(), filename[slash:], args)

        to = cursor.look_up_child(name)
        if to.is_sym():
            return self.pathwalk_symlink(cursor, to, filename[slash:], args)
        if to.is_dir():
            return self.pathwalk_one(to, filename[slash:], args)
        if to.is_negative():
            if not args["missing_ok"]:
                raise TestError(to.filename() + ": Missing intermediate path component")

        # Running awkward tests requires that we tell the kernel to walk
        # non-directories and directories that don't exist.
        return self.pathwalk_one(to, filename[slash:], args)

    # Walk over a path.  Returns a tuple of (parent, target).
    def pathwalk(self, filename, **args):
        assert(filename)
        if self.direct_mode():
            cursor = dentry(filename)
            return (cursor, cursor)
        args["symlinks"] = set()
        args["orig_filename"] = filename
        if "no_follow" not in args:
            args["no_follow"] = False
        if "dir_fd" not in args:
            args["dir_fd"] = None
        if "missing_ok" not in args:
            args["missing_ok"] = False
        if filename.startswith("/"):
            cursor = self.__root
        elif args["dir_fd"] != None:
            cursor = args["dir_fd"]
        else:
            cursor = self.__cwd
        return self.pathwalk_one(cursor, filename.rstrip("/"), args)

    # Record a file's type ("r", "s", "d", None) and symlink target record
    def record_file(self, filename, filetype, symlink_val=None, symlink_to=None, layer=None, on_upper=None):
        if filetype == None:
            i = None
        else:
            i = inode(filetype, symlink_val, symlink_to)
        (parent, dentry) = self.pathwalk(filename, missing_ok=True)
        dentry.created(i, layer, on_upper)
        return dentry

    # Change base directory
    def set_cwd(self, filename):
        (parent, target) = self.pathwalk(filename)
        self.__cwd = target

    # Recursively delete a tree
    def rmtree_aux(self, cursor):
        f = cursor.filename()
        if cursor.is_dir():
            for i in cursor.children():
                self.rmtree_aux(i)
            self.verbosef("os.rmdir({:s})\n", f)
            os.rmdir(f)
            try:
                self.verbosef("os.rmdir({:s})\n", f)
                os.rmdir(f)
            except FileNotFoundError:
                pass
        elif not cursor.is_negative():
            self.verbosef("os.unlink({:s})\n", f)
            os.unlink(f)
            try:
                self.verbosef("os.unlink({:s})\n", f)
                os.unlink(f)
            except FileNotFoundError:
                pass

    def rmtree(self, filename):
        self.output("- rmtree ", filename, "\n")
        self.check_layer(filename)
        (parent, target) = self.pathwalk(filename)
        self.rmtree_aux(target)
        parent.unlink_child(target)
        self.check_layer(filename)

    # Check that ino has not changed due to copy up or mount cycle
    def check_dev_ino(self, filename, dentry, dev, ino, layer, recycle):
        # Skip the persistent ino check for directory if lower and upper are not using same st_dev
        if not self.same_dev() and dentry.is_dir() and recycle:
            return
        # Skip the check if upper was rotated to lower
        if layer != self.layers_nr():
            return
        # Compare st_dev/st_ino before copy up / mount cycle to current st_dev/st_ino
        ino2 = self.get_file_ino(filename)
        dev2 = self.get_dev_id(filename)
        if ino != ino2 or (dev != dev2 and not recycle):
            if dev2 != self.upper_dir_fs() and dev2 != self.upper_fs():
                raise TestError(filename + ": inode number changed on copy up, but not on upper/union layer")
            if self.config().is_verify():
                raise TestError(filename + ": inode number/layer changed on copy up (got " +
                                str(dev2) + ":" + str(ino2) + ", was " +
                                str(dev) + ":" + str(ino) + ")")

    # Check that file/data was/not copied up as expected
    def check_copy_up(self, filename, dentry, layer, blocks):
        upper_path = self.upper_path(filename)
        try:
            upper_blocks = self.get_file_blocks(upper_path)
        except (FileNotFoundError, NotADirectoryError):
            if dentry.on_upper(layer):
                raise TestError(upper_path + ": Upper file is missing")
            return

        if not dentry.on_upper(layer):
            # Directory could have been copied up recursively and we didn't mark it's dentry on_upper
            if dentry.is_dir() or self.is_whiteout(upper_path):
                return
            raise TestError(upper_path + ": Upper file unexpectedly found")

        if not dentry.is_reg():
            return

        # Metacopy should have st_blocks coming from lowerdata, so upper blocks
        # should be zero. This check may give false positives with metacopy=on
        # and upper file whose st_blocks > 0 when xattrs are not stored in inode
        if self.config().is_metacopy() and not dentry.data_on_upper(layer):
            if upper_blocks != 0:
                raise TestError(upper_path +
                        ": Metacopy file blocks non-zero (" +
                        str(upper_blocks) + ")")
        # Wanted to compare upper_blocks to block, but that test fails sometimes
        # on xfs because st_blocks can be observed larger than actual blocks for
        # a brief time after copy up, because of delalloc blocks on the inode
        # beyond EOF due to speculative preallocation. And sometimes the value
        # of st_blocks from first stat() did not match the value from second stat()
        elif bool(upper_blocks) != bool(blocks):
            raise TestError(upper_path +
                    ": Upper file blocks missmatch (" +
                    str(upper_blocks) + " != " + str(blocks) + ")")


    ###########################################################################
    #
    # Layer check operation
    #
    ###########################################################################
    def check_layer(self, filename, dir_fd=None, symlinks=set()):
        if self.direct_mode():
            return
        (parent, dentry) = self.pathwalk(filename, no_follow=True, dir_fd=dir_fd,
                                         missing_ok=True)
        name = dentry.filename()
        try:
            dev = self.get_dev_id(name)
            blocks = self.get_file_blocks(name)
        except (FileNotFoundError, NotADirectoryError):
            if not dentry.is_negative():
                raise TestError(name + ": File is missing")
            return

        if dentry.is_negative():
            raise TestError(name + ": File unexpectedly found")

        #self.output("- check_layer ", dentry.filename(), " -", dentry.layer(), " # ", dev, "\n")
        if self.skip_layer_test():
            return

        layer = self.layers_nr()
        if self.config().is_verify():
            self.check_copy_up(name, dentry, layer, blocks)

        if dentry.is_dir():
            # Directory inodes are always on overlay st_dev
            if dev != self.upper_dir_fs():
                raise TestError(name + ": Directory not on union layer")
        elif self.same_dev():
            # With samefs or xino setup, files are on overlay st_dev if st_ino is
            # constant on copy up and on real st_dev if st_ino is not constant.
            # --verify verifies constant st_ino, so it implies overlay st_dev check.
            # Without --verify, we allow for both options.
            if dev == self.upper_dir_fs():
                pass
            elif self.config().is_verify() or self.config().is_fusefs():
                raise TestError(name + ": File not on union layer")
            elif dev != self.upper_fs():
                raise TestError(name + ": File not on lower/upper layer")
        else:
            # With non samefs setup, files are on pseudo or upper st_dev if st_ino
            # is constant on copy up and on lower or upper st_dev otherwise.
            # --verify verifies constant st_ino, so it implies pseudo st_dev check.
            # Without --verify we allow for both options.
            if dev == self.upper_dir_fs():
                raise TestError(name + ": File unexpectedly on union layer")
            elif dev == self.upper_fs():
                # Only pure upper may have upper fs st_dev
                if not dentry.data_on_upper(layer):
                    raise TestError(name + ": File unexpectedly on upper layer")
            elif self.config().is_verify():
                if dev == self.lower_fs():
                    # With non samefs constant inode, overlayfs returns pseudo st_dev
                    # or upper layer st_dev, but never the lower layer st_dev
                    raise TestError(name + ": File unexpectedly on lower layer")
            else:
                # Whether or not dentry.on_upper(), st_dev could be from
                # lower layer or pseudo st_dev, in case upper has origin,
                # so there is nothing left for us to check here.
                # TODO: record lower_file_fs() after clean mount on a sample
                # lower file and check here that dev == self.lower_file_fs()
                pass

        if dentry.is_sym() and dentry not in symlinks:
            symlinks.add(dentry)
            self.check_layer(dentry.sym_val(), dir_fd=parent, symlinks=symlinks)

    ###########################################################################
    #
    # Open a file operation
    #
    ###########################################################################
    def open_file(self, filename, **args):
        filename = filename.replace("//", "/")
        self.check_layer(filename)

        line = ""
        flags = 0
        rd = False
        wr = False

        if "ro" in args:
            line += " -r"
            rd = True
        elif "rw" in args:
            line += " -r -w"
            rd = True
            wr = True
        elif "wo" in args:
            line += " -w"
            wr = True
        elif "app" in args:
            wr = True
        else:
            raise RuntimeError("One or both of -r and -w must be supplied to open_file")

        if "app" in args:
            flags |= os.O_APPEND
            line += " -a"
            wr = True

        layer = self.layers_nr()
        copy_up = None
        if rd and wr:
            flags |= os.O_RDWR
            copy_up = upper.DATA
        elif rd:
            flags |= os.O_RDONLY
        else:
            flags |= os.O_WRONLY
            copy_up = upper.DATA

        create = False
        if "dir" in args:
            line += " -d"
            flags |= os.O_DIRECTORY
        if "crt" in args:
            line += " -c"
            flags |= os.O_CREAT
            create = True
        if "ex" in args:
            line += " -e"
            flags |= os.O_EXCL
        if "tr" in args:
            line += " -t"
            flags |= os.O_TRUNC
            copy_up = upper.DATA

        mode = 0
        if "mode" in args:
            mode = args["mode"]
            line += " -m " + str(mode)

        if "read" in args:
            line += " -R " + args["read"]

        if "write" in args:
            line += " -W " + args["write"]

        if "err" not in args:
            args["err"] = None
        want_error = args["err"]

        missing_ok = (want_error==errno.ENOENT) or create
        (parent, dentry) = self.pathwalk(filename, missing_ok=missing_ok)

        # Determine the error we might expect.  This is complicated by the fact
        # that we have to automatically change the error if we expect a failure
        # due to a path with a terminal slash.
        #
        # Further, it's possible to get EXDEV on renaming a directory that
        # mirrors an underlying directory.
        #
        if dentry.get_exdev_on_rename() and "xerr" in args and not self.__skip_layer_test:
            args["err"] = args["xerr"]

        if filename.endswith("/"):
            if not dentry.is_negative():
                if create:
                    args["err"] = errno.EISDIR
                elif dentry.is_dir_or_sym_to_dir():
                    pass
                else:
                    args["err"] = errno.ENOTDIR
            elif dentry.is_negative():
                if create:
                    args["err"] = errno.EISDIR
                elif dentry.did_create_fail():
                    args["err"] = errno.ENOENT

        if self.__run_as != 0:
            args["as_bin"] = self.__run_as
        if "as_bin" in args:
            line += " -B"

        want_error = args["err"]
        if want_error:
            line += " -E " + errno.errorcode[want_error]

        self.output(" ./run --open-file ", filename, line, "\n")

        # Open the file
        try:
            if "as_bin" in args and self.__run_as != args["as_bin"]:
                self.verbosef("os.seteuid({:d})", args["as_bin"])
                os.seteuid(args["as_bin"])
                self.verbosef("os.setegid({:d})", args["as_bin"])
                os.setegid(args["as_bin"])
            self.verbosef("os.open({:s},{:x},{:o})\n", filename, flags, mode)
            fd = os.open(filename, flags, mode)
            if "as_bin" in args and self.__run_as != args["as_bin"]:
                self.verbosef("os.seteuid({:d})", self.__run_as)
                os.seteuid(self.__run_as)
                self.verbosef("os.setegid({:d})", self.__run_as)
                os.setegid(self.__run_as)
            if want_error:
                raise TestError(filename + ": Expected error (" +
                                os.strerror(want_error) + ") was not produced")
            if not self.direct_mode():
                if dentry.is_negative():
                    if not create:
                        raise TestError(filename + ": File was created without O_CREAT")
                    dentry.created(inode("f"), layer)
                else:
                    if copy_up:
                        dentry.copied_up(layer, copy_up)
        except OSError as oe:
            if "as_bin" in args and self.__run_as != args["as_bin"]:
                self.verbosef("os.seteuid({:d})", self.__run_as)
                os.seteuid(self.__run_as)
                self.verbosef("os.setegid({:d})", self.__run_as)
                os.setegid(self.__run_as)
            actual = os.strerror(oe.errno)
            if not want_error:
                raise TestError(filename + ": Unexpected error: " + actual)
            wanted = os.strerror(want_error)
            if want_error != oe.errno:
                raise TestError(filename + ": Unexpected error (expecting " +
                                wanted + "): " + actual)
            fd = None
            if create:
                dentry.failed_to_create()

        self.check_layer(filename)

        # Write the data to it, if any
        if fd != None and "write" in args:
            data = args["write"].encode()
            self.verbose("os.write(", fd, ",", data, ")\n");
            res = os.write(fd, data)
            l = len(data)
            if res != l:
                raise TestError(filename + ": File write length incorrect (" +
                                str(res) + " != " + str(l) + ")")

        # Read the contents back from it and compare if requested
        if fd != None and "read" in args:
            data = args["read"].encode()
            l = len(data)
            self.verbose("os.fstat(", fd, ")\n");
            st = os.fstat(fd)
            if st.st_size != l:
                raise TestError(filename + ": File size wrong (got " +
                                str(st.st_size) + ", want " + str(l) + ")")

            self.verbose("os.lseek(", fd, ",0,0)\n");
            os.lseek(fd, 0, os.SEEK_SET)

            self.verbose("os.read(", fd, ",", l, ")\n");
            content = os.read(fd, l)
            if len(content) != l:
                raise TestError(filename + ": File read length incorrect (" +
                                str(len(content)) + " != " + str(l) + ")")

            if content != data:
                raise TestError(filename + ": File contents differ (expected '" +
                                data.decode() + "', got '" + content.decode() + "')")

        if fd != None:
            self.verbose("os.close(", fd, ")\n");
            os.close(fd)
        self.check_layer(filename)

    # Open a directory
    def open_dir(self, filename, **args):
        self.open_file(filename, dir=1, **args)

    ###########################################################################
    #
    # Determine the error that should be produced for a single-filename
    # function that doesn't create the file where the filename has an incorrect
    # slash appended.
    #
    # Pass to vfs_op_prelude() with guess=guess1_error
    #
    ###########################################################################
    def guess1_error(self, dentry, has_ts, dentry2, has_ts2):
        if not has_ts:
            return None
        if dentry.is_negative():
            return errno.ENOENT
        if dentry.is_sym():
            return errno.ENOTDIR
        if dentry.is_reg_or_sym_to_reg():
            return errno.ENOTDIR
        return None

    ###########################################################################
    #
    # Determine the error that should be produced for a single-filename
    # function that doesn't create the file where the filename has an incorrect
    # slash appended.
    #
    # Pass to vfs_op_prelude() with guess=guess1_error_create
    #
    ###########################################################################
    def guess1_error_create(self, dentry, has_ts, dentry2, has_ts2):
        if not has_ts:
            return None
        if not dentry.is_negative():
            if dentry.is_sym():
                return errno.ENOTDIR
            elif dentry.is_reg_or_sym_to_reg():
                return errno.EISDIR
        elif dentry.is_negative():
            return errno.EISDIR
        return None

    ###########################################################################
    #
    # VFS Operation common bits
    #
    ###########################################################################
    def vfs_op_prelude(self, line, filename, args, filename2=None,
                       no_follow=True,
                       guess=None,
                       create=False):
        line = line.replace("//", "/")
        if "follow" in args:
            no_follow = False
        if "no_follow" in args:
            no_follow = True
        if "err" not in args:
            args["err"] = None
        want_error = args["err"]
        missing_ok = filename2 == None and ((want_error != None) or create)

        filename = filename.replace("//", "/")
        (parent, dentry) = self.pathwalk(filename, no_follow=no_follow,
                                         missing_ok=missing_ok)
        has_ts=filename.endswith("/")

        if filename2 != None:
            filename2 = filename2.replace("//", "/")
            (parent2, dentry2) = self.pathwalk(filename2, no_follow=no_follow,
                                               missing_ok=True)
            has_ts2=filename.endswith("/")
        else:
            parent2 = None
            dentry2 = None
            has_ts2 = None

        # Determine the error we might expect.  This is complicated by the fact
        # that we have to automatically change the error if we expect a failure
        # due to a path with a terminal slash.
        #
        # Further, it's possible to get EXDEV on renaming a directory that
        # mirrors an underlying directory.
        #
        if dentry.get_exdev_on_rename() and "xerr" in args and not self.__skip_layer_test:
            args["err"] = args["xerr"]

        override = guess(dentry, has_ts, dentry2, has_ts2)
        if override:
            args["err"] = override
        want_error = args["err"]

        # Build the commandline to repeat the test
        if "follow" in args:
            line += " -L"
        elif "no_follow" in args:
            line += " -l"
        if "no_automount" in args:
            line += " -A"
        if "content" in args:
            line += " -R " + args["content"]
        if "as_bin" in args:
            line += " -B"
        else if self.__run_as != 0:
            args["as_bin"] = self.__run_as
        if want_error:
            line += " -E " + errno.errorcode[want_error]
        self.output(" ./run --", line, "\n")

        self.check_layer(filename)
        if filename2 != None:
            self.check_layer(filename)

        if "as_bin" in args:
            self.verbosef("os.setegid(1)")
            os.setegid(1)
            self.verbosef("os.seteuid(1)")
            os.seteuid(1)

        if filename2 != None:
            return (dentry, dentry2)
        else:
            return dentry

    # Determine how to handle success
    def vfs_op_success(self, filename, dentry, args, filetype="f", create=False, copy_up=None,
                       hardlink_to=None):
        if "as_bin" in args and args["as_bin"] != self.__run_as:
            self.verbosef("os.seteuid({:d})", self.__run_as)
            os.seteuid(self.__run_as)
            self.verbosef("os.setegid({:d})", self.__run_as)
            os.setegid(self.__run_as)
        want_error = args["err"]
        if want_error:
            raise TestError(filename + ": Expected error (" +
                            os.strerror(want_error) + ") was not produced")
        layer = self.layers_nr()
        if dentry.is_negative():
            if not create:
                if filetype == "d":
                    raise TestError(filename + ": Directory was created unexpectedly")
                elif filetype == "s":
                    raise TestError(filename + ": Symlink was created unexpectedly")
                else:
                    raise TestError(filename + ": File was created unexpectedly")
            if not hardlink_to:
                dentry.created(inode(filetype), layer)
            else:
                dentry.created(hardlink_to.inode(), layer, on_upper = hardlink_to.on_upper(layer))
        else:
            if copy_up:
                dentry.copied_up(layer, copy_up)
        self.check_layer(filename)

    # Determine how to handle an error
    def vfs_op_error(self, oe, filename, dentry, args, create=False):
        if self.__run_as:
            args["as_bin"] = self.__run_as
        if "as_bin" in args and not self.__run_as:
            self.verbosef("os.seteuid(0)")
            os.seteuid(0)
            self.verbosef("os.setegid(0)")
            os.setegid(0)
        actual = os.strerror(oe.errno)
        want_error = args["err"]
        if not want_error and oe.errno != errno.EXDEV:
            raise TestError(filename + ": Unexpected error: " + actual)
        if want_error != oe.errno and oe.errno == errno.EXDEV:
            raise TestError(filename + ": Unexpected error: " + actual + "; Run tests with --xdev to skip dir rename tests")
        wanted = os.strerror(want_error)
        if want_error != oe.errno and want_error != errno.ENOTEMPTY and oe.errno != errno.EEXIST:
            raise TestError(filename + ": Unexpected error (expecting " +
                            wanted + "): " + actual)
        if create:
            dentry.failed_to_create()
        self.check_layer(filename)

    ###########################################################################
    #
    # Change file mode operation
    #
    ###########################################################################
    def chmod(self, filename, mode, **args):
        line = "chmod " + filename + " 0{:o}".format(mode)
        dentry = self.vfs_op_prelude(line, filename, args, guess=self.guess1_error_create)

        try:
            self.verbosef("os.chmod({:s},0{:o})\n", filename, mode)
            os.chmod(filename, mode, follow_symlinks=("no_follow" in args))
            self.vfs_op_success(filename, dentry, args, copy_up=upper.META)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # Create hard link operation
    #
    ###########################################################################
    def link(self, filename, filename2, **args):
        # Guess the error that should be produced with terminal slashes added
        def guess_error(dentry, has_ts, dentry2, has_ts2):
            if not has_ts and not has_ts2:
                return None

            if has_ts2 and dentry.is_dir():
                if dentry2.is_negative():
                    return errno.ENOENT
                if dentry2.is_reg_or_sym_to_reg():
                    return errno.EEXIST

            if has_ts:
                if dentry.is_negative():
                    return errno.ENOENT
                if dentry.is_neg_or_sym_to_neg():
                    return errno.ENOENT
                if not dentry.is_dir():
                    return errno.ENOTDIR

            if has_ts2:
                if dentry2.is_negative():
                    return errno.EISDIR
                if dentry2.is_sym():
                    return errno.ENOTDIR
                if dentry2.is_reg_or_sym_to_reg():
                    return errno.EISDIR

            return None

        line = "link " + filename + " " + filename2
        (dentry, dentry2) = self.vfs_op_prelude(line, filename, args, filename2,
                                                guess=guess_error, create=True)
        follow_symlinks = False
        if "follow" in args:
            follow_symlinks = True
        if "no_follow" in args:
            follow_symlinks = False

        try:
            self.verbosef("os.link({:s},{:s})\n", filename, filename2)
            dev = self.get_dev_id(filename)
            ino = self.get_file_ino(filename)
            layer = self.layers_nr()
            os.link(filename, filename2, follow_symlinks=follow_symlinks)
            dentry.copied_up(layer)
            self.vfs_op_success(filename, dentry, args, copy_up=upper.META)
            self.vfs_op_success(filename2, dentry2, args, create=True, filetype=dentry.filetype(),
                                hardlink_to=dentry)
            recycle = self.__recycle
            if "recycle" in args:
                recycle = args["recycle"]
            if recycle:
                # Cycle mount after link
                remount_union(self)
            # Check that ino has not changed through copy up, link and mount cycle
            self.check_dev_ino(filename, dentry, dev, ino, layer, recycle)
            self.check_dev_ino(filename2, dentry2, dev, ino, layer, recycle)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)
            self.vfs_op_error(oe, filename2, dentry2, args, create=True)

    ###########################################################################
    #
    # Make directory operation
    #
    ###########################################################################
    def mkdir(self, filename, mode, **args):
        # Guess the error that should be produced with terminal slashes added
        def guess_error(dentry, has_ts, dentry2, has_ts2):
            return None

        line = "mkdir " + filename + " 0{:o}".format(mode)
        dentry = self.vfs_op_prelude(line, filename, args,
                                     guess=guess_error,
                                     create=True)

        try:
            self.verbosef("os.mkdir({:s},0{:o})\n", filename, mode)
            os.mkdir(filename, mode)
            self.vfs_op_success(filename, dentry, args, filetype="d", create=True)
            if "recycle" not in args:
                args["recycle"] = self.__recycle
            if args["recycle"]:
                # Cycle mount and possibly rotate upper after create directory
                remount_union(self, rotate_upper=True)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args, create=True)

    ###########################################################################
    #
    # Readlink operation
    #
    ###########################################################################
    def readlink(self, filename, **args):
        # Guess the error that should be produced with terminal slashes added
        def guess_error(dentry, has_ts, dentry2, has_ts2):
            if not has_ts:
                return None
            if dentry.is_negative():
                return errno.ENOENT
            if dentry.is_sym():
                if dentry.is_dir_or_sym_to_dir():
                    return errno.EINVAL
                if dentry.is_neg_or_sym_to_neg():
                    return errno.ENOENT
                return errno.ENOTDIR
            if dentry.is_reg_or_sym_to_reg():
                return errno.ENOTDIR
            return None

        line = "readlink " + filename
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=True,
                                     guess=guess_error)

        try:
            self.verbose("os.readlink(", filename, ")\n")
            content = os.readlink(filename)
            self.vfs_op_success(filename, dentry, args)
            if content != args["content"]:
                raise TestError(filename + ": symlink has wrong content (has '" +
                                content + "' not '" + args["content"] + "')")
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # Rename operation
    #
    ###########################################################################
    def rename(self, filename, filename2, **args):
        # Guess the error that should be produced with terminal slashes added
        def guess_error(dentry, has_ts, dentry2, has_ts2):
            if not has_ts and not has_ts2:
                return None
            if dentry.is_dir():
                return None
            if dentry.is_negative():
                return errno.ENOENT
            if dentry.is_sym() or dentry.is_reg_or_sym_to_reg():
                return errno.ENOTDIR
            if dentry2.is_negative():
                return errno.EISDIR
            if dentry2.is_sym():
                return errno.ENOTDIR
            if dentry2.is_reg_or_sym_to_reg():
                return errno.EISDIR
            return None

        line = "rename " + filename + " " + filename2
        (dentry, dentry2) = self.vfs_op_prelude(
            line, filename, args, filename2,
            no_follow=True,
            guess=guess_error,
            create=True)

        try:
            self.verbosef("os.rename({:s},{:s})\n", filename, filename2)
            filetype = dentry.filetype()
            dev = self.get_dev_id(filename)
            ino = self.get_file_ino(filename)
            layer = self.layers_nr()
            os.rename(filename, filename2)
            if dentry != dentry2:
                dentry.copied_up(layer)
                dentry2.replace_with(dentry)
            self.vfs_op_success(filename, dentry, args)
            self.vfs_op_success(filename2, dentry2, args, create=True, filetype=filetype,
                                hardlink_to=dentry)
            recycle = self.__recycle
            if "recycle" in args:
                recycle = args["recycle"]
            if recycle:
                # Cycle mount and possibly rotate upper after rename
                remount_union(self, rotate_upper=True)
            # Check that ino has not changed through copy up, rename and mount cycle
            self.check_dev_ino(filename2, dentry2, dev, ino, layer, recycle)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)
            self.vfs_op_error(oe, filename2, dentry2, args, create=True)

    ###########################################################################
    #
    # Remove directory operation
    #
    ###########################################################################
    def rmdir(self, filename, **args):
        # Guess the error that should be produced with terminal slashes added
        def guess_error(dentry, has_ts, dentry2, has_ts2):
            if not has_ts:
                return None
            if dentry.is_dir():
                return None
            if not dentry.is_negative():
                return errno.ENOTDIR
            return None

        line = "rmdir " + filename
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=True,
                                     guess=guess_error)

        try:
            self.verbosef("os.rmdir({:s})\n", filename)
            os.rmdir(filename)
            dentry.unlink()
            self.vfs_op_success(filename, dentry, args)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # File truncate operation
    #
    ###########################################################################
    def truncate(self, filename, size, **args):
        line = "truncate " + filename + " " + str(size)
        dentry = self.vfs_op_prelude(line, filename, args, guess=self.guess1_error)

        try:
            self.verbose("os.truncate(", filename, ",", size, ")\n")
            os.truncate(filename, size)
            self.vfs_op_success(filename, dentry, args, copy_up=upper.DATA)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # Remove file operation
    #
    ###########################################################################
    def unlink(self, filename, **args):
        line = "unlink " + filename
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=True,
                                     guess=self.guess1_error)

        try:
            self.verbosef("os.unlink({:s})\n", filename)
            os.unlink(filename)
            dentry.unlink()
            self.vfs_op_success(filename, dentry, args)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # Set file times operation
    #
    ###########################################################################
    def utimes(self, filename, **args):
        line = "utimes " + filename
        follow = True
        if "no_follow" in args:
            follow = False
        if "follow" in args:
            follow = True
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=(not follow),
                                     guess=self.guess1_error)

        try:
            self.verbosef("os.utime({:s},follow_symlinks={:d})\n", filename, follow)
            os.utime(filename, follow_symlinks=follow)
            self.vfs_op_success(filename, dentry, args, copy_up=upper.META)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)
