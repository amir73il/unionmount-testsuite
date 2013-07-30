/* open-file.c: description
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
#include <sys/stat.h>

static __attribute__((noreturn))
void format(void)
{
	fprintf(stderr, "Format: open-file -[r][wa] [-cdet] [-m <mode>] <name> ...\n");
	fprintf(stderr, "        ... [-E <error>] [-W <data>] [-R <data>]\n");
	exit(2);
}

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

int main(int argc, char **argv)
{
	const char *expected_error = NULL;
	const char *read_data = NULL, *write_data = NULL;
	int expected_errno = 0;
	int open_flags = 0, opt, rd = 0, wr = 0, mode = 0, fd;

	if (argc <= 1)
		format();

	while (opt = getopt(argc, argv, "acdertwE:m:R:W:"),
	       opt != EOF) {
		switch (opt) {
		case 'a': wr = 1; open_flags |= O_APPEND;	break;
		case 'c': open_flags |= O_CREAT;		break;
		case 'd': open_flags |= O_DIRECTORY;		break;
		case 'e': open_flags |= O_EXCL;			break;
		case 'r': rd = 1;				break;
		case 't': open_flags |= O_TRUNC;		break;
		case 'w': wr = 1;				break;

		case 'E': expected_error = optarg;		break;
		case 'R': read_data = optarg;			break;
		case 'W': write_data = optarg;			break;
		case 'm': mode = strtoul(optarg, NULL, 0);	break;

		default:
			fprintf(stderr, "Unknown option %c\n", opt);
			exit(2);
		}
	}

	argc -= optind;
	argv += optind;
	if (argc != 1)
		format();

	if (rd && wr)
		open_flags |= O_RDWR;
	else if (rd)
		open_flags |= O_RDONLY;
	else if (wr)
		open_flags |= O_WRONLY;

	if (expected_error)
		expected_errno = map_error(expected_error);

	fd = open(*argv, open_flags, mode);
	if (fd < 0) {
		if (!expected_error)
			goto file_error;
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

	if (write_data) {
		if (write(fd, write_data, strlen(write_data)) == -1) {
			if (errno != EBADF || wr)
				goto file_error;
		}
	}

	if (read_data) {
		struct stat st;
		ssize_t result;
		size_t rdsize = strlen(read_data);
		char *buffer;

		if (fstat(fd, &st) == -1)
			goto file_error;

		if (st.st_size != rdsize) {
			fprintf(stderr, "%s: File size wrong (%zu not %zu)\n",
				*argv, st.st_size, rdsize);
			exit(1);
		}

		buffer = malloc(rdsize + 1);
		if (!buffer) {
			perror(NULL);
			exit(1);
		}

		if (lseek(fd, 0, SEEK_SET) == -1)
			goto file_error;

		result = read(fd, buffer, rdsize);
		if (result == -1 && errno == EBADF && !rd)
			goto skip_read;
		if (result == -1)
			goto file_error;
		if (result != rdsize) {
			fprintf(stderr, "%s: File read length incorrect (%zu not %zu)\n",
				*argv, (size_t)result, rdsize);
			exit(1);
		}
		buffer[rdsize] = 0;

		if (memcmp(read_data, buffer, rdsize) != 0) {
			fprintf(stderr, "%s: File contents differ\n", *argv);
			fprintf(stderr, "%s: Expected '%s'\n", *argv, read_data);
			fprintf(stderr, "%s: Got '%s'\n", *argv, buffer);
			exit(1);
		}

	skip_read:
		;
	}

	if (close(fd) == -1)
		goto file_error;

        return 0;

file_error:
	perror(*argv);
	exit(1);
}
