import sys, os

testing_unionmount = False
testing_overlayfs = False

if "TEST_OVERLAYFS" not in os.environ:
    testing_unionmount = True
    lower_mntroot = "/mnt"
    union_mntroot = "/mnt"
else:
    testing_overlayfs = True
    lower_mntroot = "/lower"
    upper_mntroot = "/upper"
    union_mntroot = "/mnt"

lowerdir = lower_mntroot + "/a"
testdir = union_mntroot + "/a"

termslash = ""
if "TERMSLASH" in os.environ and os.environ["TERMSLASH"] == "1":
    termslash = "/"
