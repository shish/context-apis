package context

import (
	"fmt"
	"time"
	"os"
	"io"
	"net/url"

	// for GoRoutineID()
	"runtime"
	"bytes"
	"strconv"
)


// based on something in camlistore
var goroutineSpace = []byte("goroutine ")
func GoRoutineID() int64 {
	b := make([]byte, 31)
	runtime.Stack(b, false)
	// Parse the 4707 otu of "goroutine 4707 ["
	b = bytes.TrimPrefix(b, goroutineSpace)
	i := bytes.IndexByte(b, ' ')
	if i < 0 {
		panic(fmt.Sprintf("No space found in %q", b))
	}
	b = b[:i]
	n, err := strconv.Atoi(string(b))
	if err != nil {
		panic(fmt.Sprintf("Failed to parse goroutine ID out of %q: %v", b, err))
	}
	return int64(n)
}


//######################################################################
// Library API
//######################################################################

var output io.Writer


// Set where to log to
func SetLogFile(logUrl string) {
	p, err := url.Parse(logUrl)
	if err != nil {panic(err)}
	if p.Scheme == "file" {
		fp, err := os.Create(p.Host + p.Path)
		if err != nil {panic(err)}
		SetLogStream(fp)
	} else {
		panic("Go API currently only supports file:// logs")
	}
}

func SetLogStream(out io.Writer) {
	output = out
}


// Log a bit of text with a given type
func LogMsg(function, text, msgType string) {
    if output != nil {
		hostname, _ := os.Hostname()
        fmt.Fprintf(output, "%f %s %d %d %s %s %s\n",
            float64(time.Now().UnixNano()) / 1000000000,
            hostname, os.Getpid(), GoRoutineID(),
            msgType, function, text)
	}
}


// Decorator to log event-start at the start of a function
// call and event-end at the end, optionally with a bookmark
// at the start
/*
func Log(text string, bookmark, exceptions, clear bool) {
    @decorator
    def _log(function, *args, **kwargs):
        if callable(text):
            _text = text(function, args, kwargs)
        else:
            _text = text
        try:
            if clear:
                Logmsg(function.func_name, None, "CLEAR")
            if bookmark:
                Logmsg(function.func_name, _text, "BMARK")
            Logmsg(function.func_name, _text, "START")
            d = function(*args, **kwargs)
            Logmsg(function.func_name, None, "ENDOK")
            return d
        except Exception as e:
            if exceptions:
                Logmsg(function.func_name, str(e), "ENDER")
            else:
                Logmsg(function.func_name, None, "ENDOK")
            raise
    return _log
}
*/


//######################################################################
// Library Convenience
//######################################################################

// Shortcut to log some text with the bookmark type
func LogBmark(text string) {
    LogMsg("-", text, "BMARK")
}


// Shortcut to log some text with the event-start type
func LogStart(text string, bookmark, clear bool) {
    if clear {
        LogMsg("-", text, "CLEAR")
	}
    if bookmark {
        LogMsg("-", text, "BMARK")
	}
    LogMsg("-", text, "START")
}


// Shortcut to log some text with the event-end (success) type
func LogEndok(text string) {
    LogMsg("-", text, "ENDOK")
}


// Shortcut to log some text with the event-end (error) type
func LogEnder(text string) {
    LogMsg("-", text, "ENDER")
}


// Shortcut to log some text with the event-clear type
func LogClear(text string) {
    LogMsg("-", text, "CLEAR")
}


//######################################################################
// Automatic Profiling Mode
//######################################################################

/*
def _profile(frame, action, params):
    if action == 'call' and Logmsg:
        Logmsg(
            "%s:%d" % (frame.f_code.co_filename, frame.f_code.co_firstlineno),
            frame.f_code.co_name,
            "START"
        )
    if action == 'return' and Logmsg:
        Logmsg(
            "%s:%d" % (frame.f_code.co_filename, frame.f_code.co_firstlineno),
            frame.f_code.co_name,
            "ENDOK"
        )


def set_profile(active=False):
    if active:
        Logstart("Profiling init", bookmark=True)
        sys.setprofile(_profile)
    else:
        sys.setprofile(None)
        Logendok("Profiling exit")


_profile_decorator_level = 0

def profile():
    """Decorator to enable profiling for a function

    Can be used recursively:

        @ctx.profile()
        def a():
            b()

        @ctx.profile()
        def b():
            print "moo"

        a()

    will turn on profiling from the start of a() to the end of a()
    """
    @decorator
    def _profile(function, *args, **kwargs):
        global _profile_decorator_level
        try:
            if _profile_decorator_level == 0:
                set_profile(True)
            _profile_decorator_level += 1

            d = function(*args, **kwargs)
        finally:
            _profile_decorator_level -= 1
            if _profile_decorator_level == 0:
                set_profile(False)

        return d
    return _profile
*/

//######################################################################
// Lock Debugging
//######################################################################

/*
class LockWrapper(object):
    """
    A class which adds lock block / acquire / release events to the
    event stream.

    Regular code:

       foo = threading.Lock()
       foo.acquire()
       foo.release()

    Annotated code:

       foo = ctx.LockWrapper(threading.Lock())
       foo.acquire()
       foo.release()
    """
    def __init__(self, lock, name):
        self.lock = lock
        self.lock_id = id(lock)
        self.name = name

    def acquire(self, blocking=1):
        if blocking:
            Logmsg(self.lock_id, self.name, "LOCKB")
        ret = self.lock.acquire(blocking)
        if ret:
            Logmsg(self.lock_id, self.name, "LOCKA")
        return ret

    def release(self):
        Logmsg(self.lock_id, self.name, "LOCKR")
        return self.lock.release()
*/
