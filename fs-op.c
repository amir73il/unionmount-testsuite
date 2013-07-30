/* Do arbitrary operations on files
 *
 * Copyright (C) 2012 Red Hat, Inc. All Rights Reserved.
 * Written by David Howells (dhowells@redhat.com)
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public Licence
 * as published by the Free Software Foundation; either version
 * 2 of the Licence, or (at your option) any later version.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <limits.h>
#include <sys/stat.h>

static const struct error_mapping {
	char	name[16];
	int	num;
} error_mapping[] = {
#define _(E) { .name = #E , .num = E }
	_(E2BIG),
	_(EACCES),
	_(EADDRINUSE),
	_(EADDRNOTAVAIL),
	_(EADV),
	_(EAFNOSUPPORT),
	_(EAGAIN),
	_(EALREADY),
	_(EBADE),
	_(EBADF),
	_(EBADFD),
	_(EBADMSG),
	_(EBADR),
	_(EBADRQC),
	_(EBADSLT),
	_(EBFONT),
	_(EBUSY),
	_(ECANCELED),
	_(ECHILD),
	_(ECHRNG),
	_(ECOMM),
	_(ECONNABORTED),
	_(ECONNREFUSED),
	_(ECONNRESET),
	_(EDEADLK),
	{ "EDEADLOCK", EDEADLK },
	_(EDESTADDRREQ),
	_(EDOM),
	_(EDOTDOT),
	_(EDQUOT),
	_(EEXIST),
	_(EFAULT),
	_(EFBIG),
	_(EHOSTDOWN),
	_(EHOSTUNREACH),
	_(EHWPOISON),
	_(EIDRM),
	_(EILSEQ),
	_(EINPROGRESS),
	_(EINTR),
	_(EINVAL),
	_(EIO),
	_(EISCONN),
	_(EISDIR),
	_(EISNAM),
	_(EKEYEXPIRED),
	_(EKEYREJECTED),
	_(EKEYREVOKED),
	_(EL2HLT),
	_(EL2NSYNC),
	_(EL3HLT),
	_(EL3RST),
	_(ELIBACC),
	_(ELIBBAD),
	_(ELIBEXEC),
	_(ELIBMAX),
	_(ELIBSCN),
	_(ELNRNG),
	_(ELOOP),
	_(EMEDIUMTYPE),
	_(EMFILE),
	_(EMLINK),
	_(EMSGSIZE),
	_(EMULTIHOP),
	_(ENAMETOOLONG),
	_(ENAVAIL),
	_(ENETDOWN),
	_(ENETRESET),
	_(ENETUNREACH),
	_(ENFILE),
	_(ENOANO),
	_(ENOBUFS),
	_(ENOCSI),
	_(ENODATA),
	_(ENODEV),
	_(ENOENT),
	_(ENOEXEC),
	_(ENOKEY),
	_(ENOLCK),
	_(ENOLINK),
	_(ENOMEDIUM),
	_(ENOMEM),
	_(ENOMSG),
	_(ENONET),
	_(ENOPKG),
	_(ENOPROTOOPT),
	_(ENOSPC),
	_(ENOSR),
	_(ENOSTR),
	_(ENOSYS),
	_(ENOTBLK),
	_(ENOTCONN),
	_(ENOTDIR),
	_(ENOTEMPTY),
	_(ENOTNAM),
	_(ENOTRECOVERABLE),
	_(ENOTSOCK),
	_(ENOTTY),
	_(ENOTUNIQ),
	_(ENXIO),
	_(EOPNOTSUPP),
	_(EOVERFLOW),
	_(EOWNERDEAD),
	_(EPERM),
	_(EPFNOSUPPORT),
	_(EPIPE),
	_(EPROTO),
	_(EPROTONOSUPPORT),
	_(EPROTOTYPE),
	_(ERANGE),
	_(EREMCHG),
	_(EREMOTE),
	_(EREMOTEIO),
	_(ERESTART),
	_(ERFKILL),
	_(EROFS),
	_(ESHUTDOWN),
	_(ESOCKTNOSUPPORT),
	_(ESPIPE),
	_(ESRCH),
	_(ESRMNT),
	_(ESTALE),
	_(ESTRPIPE),
	_(ETIME),
	_(ETIMEDOUT),
	_(ETOOMANYREFS),
	_(ETXTBSY),
	_(EUCLEAN),
	_(EUNATCH),
	_(EUSERS),
	{ "EWOULDBLOCK", EAGAIN },
	_(EXDEV),
	_(EXFULL),
};

static int map_error_cmp(const void *_sym, const void *_member)
{
	const char *sym = _sym;
	const struct error_mapping *member = _member;

	return strcmp(sym, member->name);
}

static int map_error(const char *sym)
{
	const struct error_mapping *p;

	if (sym[0] != 'E' || !sym[1])
		goto unknown_error;

	p = bsearch(sym,
		    error_mapping,
		    sizeof(error_mapping) / sizeof(error_mapping[0]),
		    sizeof(error_mapping[0]),
		    map_error_cmp);
	if (p)
		return p->num;

unknown_error:
	fprintf(stderr, "Unknown error string %s\n", sym);
	exit(2);
}

static __attribute__((noreturn))
void format(void)
{
	fprintf(stderr, "Format: fs-op [-E <error>] [-Lla] ...\n");
	fprintf(stderr, "        fs-op chmod <file> <mode>\n");
	fprintf(stderr, "        fs-op chown <file> <uid> <gid>\n");
	fprintf(stderr, "        fs-op mkdir <file> <mode>\n");
	fprintf(stderr, "        fs-op link <file> <dest>\n");
	fprintf(stderr, "        fs-op readlink <file> [-R <content>]\n");
	fprintf(stderr, "        fs-op rename <file> <dest>\n");
	fprintf(stderr, "        fs-op rmdir <file>\n");
	fprintf(stderr, "        fs-op truncate <file> <size>\n");
	fprintf(stderr, "        fs-op unlink <file>\n");
	fprintf(stderr, "        fs-op utimes <file>\n");
	exit(2);
}

static int expected_errno = 0;
static int atflags = 0;

/*
 *
 */
int main(int argc, char **argv)
{
	const char *expected_error = NULL, *expected_content = NULL;
	char buf[PATH_MAX + 1];
	int opt, ret;

	if (argc <= 1)
		format();

	while (opt = getopt(argc, argv, "E:lALR:"),
	       opt != EOF) {
		switch (opt) {
		case 'E': expected_error = optarg;		break;
		case 'R': expected_content = optarg;		break;
		case 'L': atflags |= AT_SYMLINK_FOLLOW;		break;
		case 'l': atflags |= AT_SYMLINK_NOFOLLOW;	break;
		case 'a': atflags |= AT_NO_AUTOMOUNT;		break;
		default:
			fprintf(stderr, "Unknown option %c\n", opt);
			exit(2);
		}
	}

	argc -= optind;
	argv += optind;
	if (argc < 2)
		format();

	if (expected_error)
		expected_errno = map_error(expected_error);

	if (strcmp(argv[0], "chmod") == 0) {
		if (argc != 3)
			format();

		ret = fchmodat(AT_FDCWD, argv[1],
			       strtoul(argv[2], NULL, 0),
			       atflags);

	} else if (strcmp(argv[0], "chown") == 0) {
		if (argc != 4)
			format();

		ret = fchownat(AT_FDCWD, argv[1],
			       strtoul(argv[2], NULL, 0),
			       strtoul(argv[3], NULL, 0),
			       atflags);

	} else if (strcmp(argv[0], "mkdir") == 0) {
		if (argc != 3)
			format();

		ret = mkdirat(AT_FDCWD, argv[1],
			      strtoul(argv[2], NULL, 0));

	} else if (strcmp(argv[0], "link") == 0) {
		if (argc != 3)
			format();

		ret = linkat(AT_FDCWD, argv[1],
			     AT_FDCWD, argv[2],
			     atflags);

	} else if (strcmp(argv[0], "readlink") == 0) {
		if (argc != 2)
			format();

		ret = readlinkat(AT_FDCWD, argv[1], buf, sizeof(buf));

		if (ret >= 0 &&
		    expected_content &&
		    strcmp(buf, expected_content) != 0) {
			fprintf(stderr, "%s: Symlink has wrong content\n", argv[1]);
			exit(1);
		}

	} else if (strcmp(argv[0], "rename") == 0) {
		if (argc != 3)
			format();

		ret = renameat(AT_FDCWD, argv[1],
			       AT_FDCWD, argv[2]);

	} else if (strcmp(argv[0], "rmdir") == 0) {
		if (argc != 2)
			format();

		ret = unlinkat(AT_FDCWD, argv[1],
			       atflags | AT_REMOVEDIR);

	} else if (strcmp(argv[0], "symlink") == 0) {
		if (argc != 3)
			format();

		ret = symlinkat(argv[1],
				AT_FDCWD, argv[2]);

	} else if (strcmp(argv[0], "truncate") == 0) {
		if (argc != 3)
			format();

		ret = truncate(argv[1], atol(argv[2]));

	} else if (strcmp(argv[0], "unlink") == 0) {
		if (argc != 2)
			format();

		ret = unlinkat(AT_FDCWD, argv[1],
			       atflags);

	} else if (strcmp(argv[0], "utimes") == 0) {
		struct timespec ts[2] = {
			[0].tv_nsec = UTIME_NOW,
			[1].tv_nsec = UTIME_NOW
		};

		if (argc != 2)
			format();

		ret = utimensat(AT_FDCWD, argv[1],
				ts,
				atflags);

	} else {
		fprintf(stderr, "Unknown operation: %s\n", argv[0]);
		format();
	}

	/*
	 * Determine whether the return value and error are what we expected
	 */
	if (ret < 0) {
		if (!expected_error) {
			perror(argv[0]);
			exit(1);
		}
		if (errno != expected_errno) {
			fprintf(stderr, "%s: Unexpected error (expecting %s): %m\n",
				*argv, expected_error);
			exit(1);
		}

		/* Failed as expected */
		exit(0);
	}

	if (expected_error) {
		fprintf(stderr, "%s: Expected error (%s) was not produced\n",
			*argv, expected_error);
		exit(1);
	}

	exit(0);
}
