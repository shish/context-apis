#!/usr/bin/perl

$|++;
use context;

sub hello {
	log_start("Saying hello");
	print "hello ";
	sleep(1);
	log_endok("Saying hello");
}

sub world {
	log_start("Saying world");
	print "world\n";
	sleep(2);
	log_endok("Saying world");
}

set_log("file://output.pl.ctxt");
log_start("Running program");
hello();
world();
log_endok("Running program");
