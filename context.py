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

from tool_box import TestError
import sys, os, errno

class dentry:
    def __init__(self, name, filetype,
                 symlink_val=None, symlink_to=None, on_upper=None, root=False):
        self.__name = name
        self.__filetype = filetype
        self.__symlink_val = symlink_val
        self.__symlink_to = symlink_to
        self.__upper = on_upper or filetype == "d"
        self.__failed_create = False
        self.__parent = None
        self.__children = dict()

    def created(self, filetype, symlink_val=None, symlink_to=None, on_upper=True):
        assert(self.__filetype == None)
        self.__filetype = filetype
        self.__symlink_val = symlink_val
        self.__symlink_to = symlink_to
        self.__upper = on_upper
        self.__failed_create = False

    def failed_to_create(self):
        if self.__filetype == None:
            self.__failed_create = True

    def clear(self):
        assert(self.__filetype != None)
        self.__filetype = None
        self.__symlink_val = None
        self.__symlink_to = None
        self.__upper = True
        self.__children = dict()

    def name(self):
        return self.__name

    def filename(self):
        if self.__parent == None:
            return ""
        return self.__parent.filename() + "/" + self.__name

    def is_negative(self):
        return self.__filetype == None

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
        del self.__children[child.__name]
        child.__parent = None

    def unlink(self):
        self.parent().unlink_child(self)

    def did_create_fail(self):
        return self.__failed_create

    def copied_up(self):
        self.__upper = True

    def on_upper(self):
        return self.__upper

    def layer(self):
        if self.on_upper():
            return "upper"
        return "lower"

    def is_dir(self):
        return self.__filetype == "d"

    def is_sym(self):
        return self.__filetype == "s"

    def sym_val(self):
        return self.__symlink_val

    def sym_target(self):
        return self.__symlink_to

    def is_neg_or_sym_to_neg(self):
        return self.__filetype == None or self.is_sym() and self.sym_target().is_neg_or_sym_to_neg()

    def is_reg_or_sym_to_reg(self):
        return self.__filetype == "r" or self.is_sym() and self.sym_target().is_reg_or_sym_to_reg()

    def is_dir_or_sym_to_dir(self):
        return self.__filetype == "d" or self.is_sym() and self.sym_target().is_dir_or_sym_to_dir()

###############################################################################
#
# The main test context
#
###############################################################################
class test_context:
    def __init__(self, cfg, termslash=False, direct_mode=False):
        self.__cfg = cfg
        self.__root = dentry("/", "d", root=True)
        self.__cwd = None
        self.__filenr = 99
        self.__lower_fs = None
        self.__upper_fs = None
        self.__upper_dir_fs = None
        self.__verbose = cfg.is_verbose()
        self.__direct_mode = direct_mode
        self.__skip_layer_test = cfg.testing_none()
        if cfg.is_termslash():
            self.__termslash = "/"
        else:
            self.__termslash = ""

    def config(self):
        return self.__cfg

    def direct_mode(self):
        return self.__direct_mode

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

    def get_dev_id(self, path):
        if path.endswith("/"):
            path = path[:len(path) - 1]
        self.verbose("os.lstat(", path, ")\n")
        st = os.lstat(path)
        return st.st_dev

    def lstat_file(self, path):
        if path.endswith("/"):
            path = path[:len(path) - 1]
        self.verbose("os.lstat(", path, ")\n")
        return os.lstat(path)

    def get_file_size(self, path):
        return self.lstat_file(path).st_size

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

    def upper_fs(self):
        return self.__upper_fs

    def upper_dir_fs(self):
        return self.__upper_dir_fs

    def skip_layer_test(self):
        return self.__skip_layer_test

    # Display the banner beginning the test
    def begin_test(self, source, nr, name):
        ix = source.rfind("/")
        if ix >= 0:
            source = source[ix + 1:]
        self.output("TEST ", source, ":", nr, ": ", name, "\n")
        self.__filenr += 1

    # Increment the test fileset number
    def incr_filenr(self):
        self.__filenr += 1

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
        if args["linkcount"] <= 0:
            raise TestError(args["orig_filename"] + ": Too many symlinks")
        args["linkcount"] -= 1
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
        if self.direct_mode():
            cursor = dentry(filename, None)
            return (cursor, cursor)
        args["linkcount"] = 20
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
    def record_file(self, filename, filetype, symlink_val=None, symlink_to=None, on_upper=False):
        (parent, dentry) = self.pathwalk(filename, missing_ok=True)
        dentry.created(filetype, symlink_val, symlink_to, on_upper)
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

    ###########################################################################
    #
    # Layer check operation
    #
    ###########################################################################
    def check_layer(self, filename, dir_fd=None):
        if self.direct_mode():
            return
        (parent, dentry) = self.pathwalk(filename, no_follow=True, dir_fd=dir_fd,
                                         missing_ok=True)
        name = dentry.filename()
        try:
            dev = self.get_dev_id(name)
        except (FileNotFoundError, NotADirectoryError):
            if not dentry.is_negative():
                raise TestError(name + ": File is missing")
            return

        if dentry.is_negative():
            raise TestError(name + ": File unexpectedly found")

        #self.output("- check_layer ", dentry.filename(), " -", dentry.layer(), " # ", dev, "\n")
        if self.skip_layer_test():
            pass
        elif dev == self.lower_fs():
            if dentry.is_dir():
                raise TestError(name + ": Directory unexpectedly on lower filesystem")
            if dentry.on_upper():
                raise TestError(name + ": Test file not on upper filesystem")
        elif dentry.is_dir():
            if dev != self.upper_dir_fs():
                raise TestError(name + ": Directory not on union layer")
        elif dev != self.upper_fs() and self.upper_fs() != self.upper_dir_fs():
            raise TestError(name + ": File unexpectedly on union layer")
        elif not dentry.on_upper():
            raise TestError(name + ": File unexpectedly on upper layer")

        if dentry.is_sym():
            self.check_layer(dentry.sym_val(), dir_fd=parent)

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

        copy_up = False
        if rd and wr:
            flags |= os.O_RDWR
            copy_up = True
        elif rd:
            flags |= os.O_RDONLY
        else:
            flags |= os.O_WRONLY
            copy_up = True

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
            copy_up = True

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

        if "as_bin" in args:
            line += " -B"

        want_error = args["err"]
        if want_error:
            line += " -E " + errno.errorcode[want_error]

        self.output(" ./run --open-file ", filename, line, "\n")

        # Open the file
        try:
            if "as_bin" in args:
                self.verbosef("os.setegid(1)")
                os.setegid(1)
                self.verbosef("os.seteuid(1)")
                os.seteuid(1)
            self.verbosef("os.open({:s},{:x},{:o})\n", filename, flags, mode)
            fd = os.open(filename, flags, mode)
            if "as_bin" in args:
                self.verbosef("os.seteuid(0)")
                os.seteuid(0)
                self.verbosef("os.setegid(0)")
                os.setegid(0)
            if want_error:
                raise TestError(filename + ": Expected error (" +
                                os.strerror(want_error) + ") was not produced")
            if not self.direct_mode():
                if dentry.is_negative():
                    if not create:
                        raise TestError(filename + ": File was created without O_CREAT")
                    dentry.created("f")
                else:
                    if copy_up:
                        dentry.copied_up()
        except OSError as oe:
            if "as_bin" in args:
                self.verbosef("os.seteuid(0)")
                os.seteuid(0)
                self.verbosef("os.setegid(0)")
                os.setegid(0)
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
    # VFS Operation common bits
    #
    ###########################################################################
    def vfs_op_prelude(self, line, filename, args,
                       create=False, tslash_ok=False, no_follow=True, expect_sym=False):
        line = line.replace("//", "/")
        filename = filename.replace("//", "/")
        if "no_follow" in args:
            no_follow = True
        if "err" not in args:
            args["err"] = None
        want_error = args["err"]
        missing_ok = (want_error != None) or create

        (parent, dentry) = self.pathwalk(filename, no_follow=no_follow,
                                         missing_ok=missing_ok)

        # Determine the error we might expect.  This is complicated by the fact
        # that we have to automatically change the error if we expect a failure
        # due to a path with a terminal slash.
        #
        if not tslash_ok and filename.endswith("/"):
            if not dentry.is_negative():
                if dentry.is_sym():
                    if dentry.is_dir_or_sym_to_dir():
                        if expect_sym:
                            args["err"] = errno.EINVAL
                        else:
                            args["err"] = errno.ENOTDIR
                    elif expect_sym and dentry.is_neg_or_sym_to_neg():
                        args["err"] = errno.ENOENT
                    else:
                        args["err"] = errno.ENOTDIR
                elif dentry.is_reg_or_sym_to_reg():
                    if create:
                        args["err"] = errno.EISDIR
                    else:
                        args["err"] = errno.ENOTDIR
            elif dentry.is_negative():
                if create:
                    args["err"] = errno.EISDIR
                elif dentry.did_create_fail():
                    args["err"] = errno.ENOENT

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
        if want_error:
            line += " -E " + errno.errorcode[want_error]
        self.output(" ./run --", line, "\n")

        self.check_layer(filename)

        if "as_bin" in args:
            self.verbosef("os.setegid(1)")
            os.setegid(1)
            self.verbosef("os.seteuid(1)")
            os.seteuid(1)

        return dentry

    # Determine how to handle success
    def vfs_op_success(self, filename, dentry, args, filetype="f", create=False, copy_up=False):
        if "as_bin" in args:
            self.verbosef("os.seteuid(0)")
            os.seteuid(0)
            self.verbosef("os.setegid(0)")
            os.setegid(0)
        want_error = args["err"]
        if want_error:
            raise TestError(filename + ": Expected error (" +
                            os.strerror(want_error) + ") was not produced")
        if dentry.is_negative():
            if not create:
                if filetype == "d":
                    raise TestError(filename + ": Directory was created unexpectedly")
                elif filetype == "s":
                    raise TestError(filename + ": Symlink was created unexpectedly")
                else:
                    raise TestError(filename + ": File was created unexpectedly")
            dentry.created(filetype)
        else:
            if copy_up:
                dentry.copied_up()
        self.check_layer(filename)

    # Determine how to handle an error
    def vfs_op_error(self, oe, filename, dentry, args, create=False):
        if "as_bin" in args:
            self.verbosef("os.seteuid(0)")
            os.seteuid(0)
            self.verbosef("os.setegid(0)")
            os.setegid(0)
        actual = os.strerror(oe.errno)
        want_error = args["err"]
        if not want_error:
            raise TestError(filename + ": Unexpected error: " + actual)
        wanted = os.strerror(want_error)
        if want_error != oe.errno:
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
        dentry = self.vfs_op_prelude(line, filename, args)

        try:
            self.verbosef("os.chmod({:s},0{:o})\n", filename, mode)
            os.chmod(filename, mode, follow_symlinks=("no_follow" in args))
            self.vfs_op_success(filename, dentry, args, copy_up=True)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # Make directory operation
    #
    ###########################################################################
    def mkdir(self, filename, mode, **args):
        line = "mkdir " + filename + " 0{:o}".format(mode)
        dentry = self.vfs_op_prelude(line, filename, args, create=True, tslash_ok=True)

        try:
            self.verbosef("os.mkdir({:s},0{:o})\n", filename, mode)
            os.mkdir(filename, mode)
            self.vfs_op_success(filename, dentry, args, filetype="d", create=True)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args, create=True)

    ###########################################################################
    #
    # Readlink operation
    #
    ###########################################################################
    def readlink(self, filename, **args):
        line = "readlink " + filename
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=True, expect_sym=True)

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
    # Remove directory operation
    #
    ###########################################################################
    def rmdir(self, filename, **args):
        line = "rmdir " + filename
        dentry = self.vfs_op_prelude(line, filename, args, tslash_ok=True, no_follow=True)

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
        dentry = self.vfs_op_prelude(line, filename, args)

        try:
            self.verbose("os.truncate(", filename, ",", size, ")\n")
            os.truncate(filename, size)
            self.vfs_op_success(filename, dentry, args, copy_up=True)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)

    ###########################################################################
    #
    # Remove file operation
    #
    ###########################################################################
    def unlink(self, filename, **args):
        line = "unlink " + filename
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=True)

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
        dentry = self.vfs_op_prelude(line, filename, args, no_follow=(not follow))

        try:
            self.verbosef("os.utime({:s},follow_symlinks={:d})\n", filename, follow)
            os.utime(filename, follow_symlinks=follow)
            self.vfs_op_success(filename, dentry, args, copy_up=True)
        except OSError as oe:
            self.vfs_op_error(oe, filename, dentry, args)
