Context APIs
~~~~~~~~~~~~
All the language APIs have a fairly similar set of functions, though the
specifics will be changed to fit with each language's coding standards
(eg set_log in Python is setLog in Java, or ctx_set_log in PHP)


set_log(url, append)
--------------------
Tell context to start logging events to the given target

If filename is null / None / 0 / etc, stop logging to file

Implemented by:

- file:// - all APIs
- tcp://  - none yet
- udp://  - none yet

append defaults to true


set_profile(enabled)
--------------------
Hook into the language runtime to automatically log when every function starts and ends

enabled = boolean, true to start profiling, false to stop

Implemented by:

- Python


log_msg(location, text, marker)
-------------------------------
location = where the code is

text     = freeform text description of what's happening

marker   = BMARK, START, ENDOK, ENDER, CLEAR

Implemented by:

- ?


log_start(text)
---------------
Log that an event has started

Some APIs add optional extra paramaters for "clear stack" and "set bookmark", so you can do all three things in one call

Shortcut to log_msg(getCurrentFunction(), text, "START")


log_endok(text)
---------------
Log that an event has finished successfully


log_ender(text)
---------------
Log that an event has finished with an error


log_bmark(text)
---------------
Add a bookmark to the log


log_clear(text)
---------------
Clear the stack (it's possible that an app crash could cause a START event to
be logged with no matching ENDOK; CLEAR will turn any currently unfinished
events into ENDER)


log(text or callback)
---------------------
A decorator to log at the start and end of a function

If a callback is specified, it will be passed the function name and
paramaters, and it should return some text

Implemented by:

- Python
