
from settings import *
from tool_box import *

declare -i filenr
filenr=100

###############################################################################
#
# Open of existing directory; with O_DIRECTORY and create, exclusive and truncate
#
###############################################################################

# Open read-only and create
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -c $file -E EISDIR
open_file -d -r $file

# Open read-only and create exclusive
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -c -e $file -E EEXIST ${termslash:+-E EISDIR}
open_file -d -r $file

# Open read-only and truncate
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_TRUNC"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -t $file -E EISDIR
open_file -d -r $file

# Open read-only and truncate create
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -t -c $file -E EISDIR
open_file -d -r $file

# Open read-only and truncate create exclusive
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -d -r -t -c -e $file -E EEXIST ${termslash:+-E EISDIR}
open_file -d -r $file

# Open write-only and create
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w -c $file -E EISDIR
open_file -d -r $file

# Open write-only and create exclusive
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w -c -e $file -E EEXIST ${termslash:+-E EISDIR}
open_file -d -r $file

# Open write-only and truncate
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_TRUNC"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w -t $file -E EISDIR
open_file -d -r $file

# Open write-only and truncate create
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w -t -c $file -E EISDIR
open_file -d -r $file

# Open write-only and truncate create exclusive
echo "TEST$filenr: Open O_DIRECTORY | O_RDONLY | O_TRUNC | O_CREAT | O_EXCL"
file=$testdir/dir$((filenr++))$termslash

open_file -d -w -t -c -e $file -E EEXIST ${termslash:+-E EISDIR}
open_file -d -r $file
