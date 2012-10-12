#include <stdio.h>
#include <unistd.h>

#include "context.h"

void hello() {
	ctx_log_start("saying hello");
	printf("hello ");
	sleep(1);
	ctx_log_endok("saying hello");
}

void world() {
	ctx_log_start("saying world");
	printf("world\n");
	sleep(2);
	ctx_log_endok("saying world");
}

int main(int argc, char *argv[]) {
	ctx_set_log("output.c.ctxt", 0);
	ctx_log_start("running program");
	hello();
	world();
	ctx_log_endok("running program");
	return 0;
}
