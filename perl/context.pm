#!/usr/bin/perl

package context;

use Sys::Hostname;
use Time::HiRes qw (gettimeofday);
use base 'Exporter';
our @EXPORT = ('set_log', 'log_msg', 'get_func',
		'log_bmark', 'log_start', 'log_endok', 'log_ender', 'log_clear');

# Global output file handler
my $_output;

# Set the output location
sub set_log {
	my $fname = shift;
	$fname =~ s#file://##;
	open $_output, ">>$fname" or die "$!\n";
}

# Log a bit of text with a given type
sub log_msg {
	my ($func, $text, $type) = @_;
	if ($_output) {
		my ($second, $micro) = gettimeofday;
		printf $_output "%d.%d %s %d %s %s %s %s\n",
			$second, $micro,
			hostname, $$, $$, # threadname
			$type, $func, $text;
	}
}

# Get the name of the calling subroutine
sub get_func {
	my $subname = (caller(1))[3];
	$subname = (split("::", $subname))[-1];
	return $subname;
}

# Shortcut to log some text with the bookmark type
sub log_bmark { my $text = shift; &log_msg(&get_func(), $text, "BMARK"); }

# Shortcut to log some text with the event-start type
sub log_start { my $text = shift; &log_msg(&get_func(), $text, "START"); }

# Shortcut to log some text with the event-end (success) type
sub log_endok { my $text = shift; &log_msg(&get_func(), $text, "ENDOK"); }

# Shortcut to log some text with the event-end (error) type
sub log_ender { my $text = shift; &log_msg(&get_func(), $text, "ENDER"); }

# Shortcut to log some text with the event-clear type
sub log_clear { my $text = shift; &log_msg(&get_func(), $text, "CLEAR"); }

1;
