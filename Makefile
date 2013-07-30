CPPFLAGS += -D_GNU_SOURCE
CFLAGS += -O2 -Wall

all: fs-op open-file

fs-op: fs-op.c
open-file: open-file.c

clean:
	$(RM) *~ fs-op open-file
