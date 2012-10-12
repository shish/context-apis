#include <stdio.h>
#include <time.h>
#include <sys/timeb.h>
#include <unistd.h>

#include "context.h"

FILE *_context_log;

void ctx_set_log(const char *name, int append) {
	if(name) {
		_context_log = fopen(name, append ? "a" : "w");
	}
	else {
		if(_context_log) {
			fclose(_context_log);
		}
		_context_log = NULL;
	}
}

void ctx_log_msg(const char *func, const char *text, const char *type) {
	if(_context_log) {
		struct timeb tmb;
		char hostname[256];

		ftime(&tmb);
		gethostname(hostname, 256);

        fprintf(
			_context_log,
			"%ld.%d %s %d %d %s %s %s\n",
            tmb.time, tmb.millitm,
            hostname,
			getpid(),
			getpid(), //gettid(),
            type, func, text
        );
	}
}
