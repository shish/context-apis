#!/usr/bin/php
<?php
require_once "context.php";

function hello() {
	ctx_log_start("saying hello");
	printf("hello ");
	sleep(1);
	ctx_log_endok();
}

function greet($name) {
	ctx_log_start("greeting $name");
	printf("$name\n");
	sleep(2);
	ctx_log_endok();
}

ctx_set_log("file://output.php.ctxt");
ctx_log_start("running program", true);
hello();
greet("world");
ctx_log_endok();
?>
