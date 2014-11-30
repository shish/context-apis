<?php
$_context_log = null;

function ctx_set_log($url, $append=True) {
	global $_context_log;
	if($url) {
		$p = parse_url($url);
		if($p["scheme"] == "file") {
			if(@$p["host"] && @$p["path"]) {
				$path = $p["host"] . $p["path"];
			}
			elseif(@$p["host"]) {
				$path = $p["host"];
			}
			elseif(@$p["path"]) {
				$path = $p["path"];
			}
			else {
				throw new Exception("Filename not recognised");
			}
			$_context_log = fopen($path, $append ? "a" : "w");
		}
		else {
			throw new Exception("Only file:// protocol is supported");
		}
	}
	else {
		$_context_log = null;
	}
}

function ctx_log_msg($func, $text, $type) {
	global $_context_log;
	if($_context_log) {
        fprintf(
			$_context_log,
			"%f %s %d %d %s %s %s\n",
            microtime(true), # returning a float is 5.0+
            php_uname('n'),  # gethostname() is 5.3+
			posix_getpid(),
			function_exists("hphp_get_thread_id") ? hphp_get_thread_id() : posix_getpid(),
            $type, $func, $text
        );
	}
}

function __get_func() {
	$stack = debug_backtrace();
	if(count($stack) < 3) {
		return "top-level";
	}
	$p = $stack[2];
	return $p['function'];
}

function ctx_log_bmark($text=null) {ctx_log_msg(__get_func(), $text, "BMARK");}
function ctx_log_clear($text=null) {ctx_log_msg(__get_func(), $text, "CLEAR");}
function ctx_log_endok($text=null) {ctx_log_msg(__get_func(), $text, "ENDOK");}
function ctx_log_ender($text=null) {ctx_log_msg(__get_func(), $text, "ENDER");}

function ctx_log_start($text=null, $bookmark=false, $clear=false) {
	if($clear) {
		ctx_log_msg(__get_func(), $text, "CLEAR");
	}
	if($bookmark) {
		ctx_log_msg(__get_func(), $text, "BMARK");
	}
	ctx_log_msg(__get_func(), $text, "START");
}
?>
