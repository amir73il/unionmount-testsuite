#!/bin/bash

. ./settings.inc

tests="
	open-plain.test
	open-trunc.test
	open-creat.test
	open-creat-trunc.test
	open-creat-excl.test
	open-creat-excl-trunc.test
	noent-plain.test
	noent-trunc.test
	noent-creat.test
	noent-creat-trunc.test
	noent-creat-excl.test
	noent-creat-excl-trunc.test
	sym1-plain.test
	sym1-trunc.test
	sym1-creat.test
	sym1-creat-excl.test
	sym2-plain.test
	sym2-trunc.test
	sym2-creat.test
	sym2-creat-excl.test
	symx-plain.test
	symx-trunc.test
	symx-creat.test
	symx-creat-excl.test
	symx-creat-trunc.test
	truncate.test
	dir-open.test
	dir-weird-open.test
	dir-open-dir.test
	dir-weird-open-dir.test
	dir-sym1-open.test
	dir-sym1-weird-open.test
	dir-sym2-open.test
	dir-sym2-weird-open.test
	impermissible.test"

if [ $# -gt 0 ]
then
    tests="$*"
fi

for t in $tests
do
    echo "***"
    echo "***" $0 $t
    echo "***"

    # Construct the union
    bash ./set_up.sh || exit $?
    export lower_fs=`stat -c %D $testdir`

    bash ./mount_union.sh || exit $?
    sync || exit $?
    export upper_fs=`stat -c %D $testdir`

    # Run a test script
    bash ./$t || exit $?

    # Make sure that all dentries and inodes are correctly released
    umount $mntroot || exit $?
    umount $mntroot || exit $?
done

# Leave the union mounted for further playing
bash ./set_up.sh || exit $?
export lower_fs=`stat -c %D $testdir`
bash ./mount_union.sh || exit $?
