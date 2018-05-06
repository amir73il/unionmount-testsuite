#
# Tools for test scripts
#
import os, sys

class ArgumentError(Exception):
    def __init__(self, msg):
        self.__msg = msg
    def __str__(self):
        return self.__msg

class TestError(Exception):
    def __init__(self, msg):
        self.__msg = msg
    def __str__(self):
        return self.__msg

def exit_error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def system(command):
    ret = os.system(command)
    if ret != 0:
        raise RuntimeError("Command failed: " + command)
    return True

def read_file(path):
    fd = open(path, "r")
    data = fd.read()
    del fd
    return data

def write_file(path, data):
    fd = open(path, "w")
    fd.write(data)
    del fd

def write_kmsg(data):
    write_file("/dev/kmsg", data);

#
# Check for taint (kernel warnings and oopses)
#
current_taint = read_file("/proc/sys/kernel/tainted")
def check_not_tainted():
    taint = read_file("/proc/sys/kernel/tainted")
    if taint != current_taint:
        raise RuntimeError("TAINTED " + current_taint + " -> ", taint)

#
# Check if boolean module param is enabled
#
# Return None is module param does not exist
#
def check_bool_modparam(param):
    # If overlay is a module, make sure it is loaded before checking its params
    try:
        system("modprobe overlay 2>/dev/null")
    except RuntimeError:
        pass
    try:
        value = read_file("/sys/module/overlay/parameters/" + param)
    except FileNotFoundError:
        return None
    return value.startswith("Y")
