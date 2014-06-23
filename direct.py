from tool_box import ArgumentError
from context import test_context
import argparse
import errno

def parse_C_int(s):
    try:
        if s.startswith("0x"):
            return int(s[2:], 16)
        elif s.startswith("0"):
            return int(s[2:], 8)
        else:
            return int(s[2:], 10)
    except ValueError:
        raise ArgumentError("Unparseable number '" + s + "'")

###############################################################################
#
# ./run --open-file <file> [-acdertvw] [-W <data>] [-R <data>] [-B] [-E <err>]
#
###############################################################################
def direct_open_file(cfg, cmdargs):
    if len(cmdargs) < 1:
        raise ArgumentError("Insufficient Arguments")

    parser = argparse.ArgumentParser(description='Open and read/write a file',
                                     prog=cfg.progname() + " --open-file <file>")
    parser.add_argument("file", nargs=1)
    parser.add_argument("-a", action="store_true")
    parser.add_argument("-c", action="store_true")
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-e", action="store_true")
    parser.add_argument("-m", nargs=1)
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-t", action="store_true")
    parser.add_argument("-v", action="store_true")
    parser.add_argument("-w", action="store_true")
    parser.add_argument("-W", nargs=1)
    parser.add_argument("-R", nargs=1)
    parser.add_argument("-B", action="store_true")
    parser.add_argument("-E", nargs=1)
    p = parser.parse_args(cmdargs)
    p = vars(p)

    args = dict()
    if p["r"]:
        if p["w"]:
            args["rw"] = 1
        else:
            args["ro"] = 1
    elif p["w"]:
        args["wo"] = 1

    if p["v"]:
        ctx.cfg.set_verbose()
    if p["c"]:
        args["crt"] = 1
    if p["d"]:
        args["dir"] = 1
    if p["e"]:
        args["ex"] = 1
    if p["m"] != None:
        args["mode"] = parse_C_int(p["m"][0])
    if p["t"]:
        args["tr"] = 1
    if p["B"]:
        args["as_bin"] = 1
    if p["R"]:
        args["read"] = p["R"][0]
    if p["W"]:
        args["write"] = p["W"][0]

    if p["E"]:
        errname = p["E"][0]
        for i in errno.errorcode.keys():
            if errno.errorcode[i] == errname:
                args["err"] = i
                break
        else:
            raise ArgumentError("Unknown error code name '" + errname + "'")

    ctx = test_context(cfg, direct_mode=True)
    ctx.open_file(p["file"][0], **args)

###############################################################################
#
# ./run --fs-op <cmd> <file> [<args>*] [-aLlv] [-R <content>] [-B] [-E <err>]
#
###############################################################################
def direct_fs_op(cfg, cmdargs):
    ctx = test_context(cfg, direct_mode=True)
    if len(cmdargs) < 2:
        raise ArgumentError("Insufficient Arguments")

    op = cmdargs[0][2:]
    parser = argparse.ArgumentParser(description='Operate upon a file',
                                     prog=cfg.progname() + " --" + op + " <file> [<arg>+]")
    parser.add_argument("file", nargs=1)
    parser.add_argument("args", nargs="*")
    parser.add_argument("-v", action="store_true")
    parser.add_argument("-a", action="store_true")
    parser.add_argument("-l", action="store_true")
    parser.add_argument("-L", action="store_true")
    parser.add_argument("-R", nargs=1)
    parser.add_argument("-B", action="store_true")
    parser.add_argument("-E", nargs=1)
    p = parser.parse_args(cmdargs[1:])
    p = vars(p)

    args = dict()
    if p["v"]:
        ctx.cfg.set_verbose()
    if p["a"]:
        args["no_automount"] = 1
    if p["l"]:
        args["no_follow"] = 1
    if p["L"]:
        args["follow"] = 1
    if p["R"]:
        args["content"] = p["R"][0]
    if p["B"]:
        args["as_bin"] = 1

    if p["E"]:
        errname = p["E"][0]
        for i in errno.errorcode.keys():
            if errno.errorcode[i] == errname:
                args["err"] = i
                break
        else:
            raise ArgumentError("Unknown error code name '" + errname + "'")

    ctx = test_context(cfg, direct_mode=True)

    f = p["file"][0]
    xargs = p["args"]
    if op == "chmod":
        if len(xargs) != 1:
            raise ArgumentError("chmod requires a single mode argument")
        ctx.chmod(f, parse_C_int(xargs[0]), **args)
    elif op == "link":
        if len(xargs) != 1:
            raise ArgumentError("link requires a single additional filename")
        ctx.rename(f, xargs[0], **args)
    elif op == "mkdir":
        if len(xargs) != 1:
            raise ArgumentError("mkdir requires a single mode argument")
        ctx.mkdir(f, parse_C_int(xargs[0]), **args)
    elif op == "readlink":
        if len(xargs) != 0:
            raise ArgumentError("readlink requires no additional arguments")
        ctx.readlink(f, **args)
    elif op == "rename":
        if len(xargs) != 1:
            raise ArgumentError("rename requires a single additional filename")
        ctx.rename(f, xargs[0], **args)
    elif op == "rmdir":
        if len(xargs) != 0:
            raise ArgumentError("rmdir requires no additional arguments")
        ctx.rmdir(f, **args)
    elif op == "truncate":
        if len(xargs) != 1:
            raise ArgumentError("truncate requires a single size argument")
        ctx.truncate(f, int(xargs[0]), **args)
    elif op == "unlink":
        if len(xargs) != 0:
            raise ArgumentError("unlink requires no additional arguments")
        ctx.unlink(f, **args)
    elif op == "utimes":
        if len(xargs) != 0:
            raise ArgumentError("utimes requires no additional arguments")
        ctx.utimes(f, **args)
    else:
        raise ArgumentError("Unknown subcommand")
