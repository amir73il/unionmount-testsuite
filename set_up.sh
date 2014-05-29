#!/bin/bash
#
# Create and set up a lower layer for the test scripts to use
#
. ./settings.inc

# Discard anything already mounted to avoid contamination
sync
umount $mntroot
umount $mntroot

# Create a lower layer to union over
mount -t tmpfs lower_layer $mntroot || exit $?

# Systemd has weird ideas about things
mount --make-private $mntroot || exit $?

#
# Create a few test files we can use in the lower layer
#
mkdir $testdir || exit $?

for ((i=100; i<130; i++))
do
    # Under the test directory, we create a bunch of regular files
    # containing data called foo100 to foo129:
    echo -n ":xxx:yyy:zzz" >$testdir/foo$i || exit $?

    # Then we create a bunch of direct symlinks to those files
    ln -s ../a/foo$i $testdir/direct_sym$i

    # Then we create a bunch of indirect symlinks to those files
    ln -s direct_sym$i $testdir/indirect_sym$i

    # Then we create a bunch symlinks that don't point to extant files
    ln -s no_foo$i $testdir/pointless$i

    # We create a bunch of directories, each with an empty file
    mkdir $testdir/dir$i
    touch $testdir/dir$i/a

    # And add direct and indirect symlinks to those
    ln -s ../a/dir$i $testdir/direct_dir_sym$i
    ln -s $testdir/direct_dir_sym$i $testdir/indirect_dir_sym$i

    # And a bunch of empty directories
    mkdir $testdir/empty$i

    # Everything above is then owned by the bin user
    chown -h bin.bin $testdir/{foo,direct_sym,indirect_sym,pointless}$i || exit $?

    # Create some root-owned regular files also
    echo -n ":xxx:yyy:zzz" >$testdir/rootfile$i || exit $?
done

# The mount has to be read-only for us to make use of it
mount -o remount,ro $mntroot || exit $?
sync || exit $?
