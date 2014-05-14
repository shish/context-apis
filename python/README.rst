Context API (Python)
~~~~~~~~~~~~~~~~~~~~

Stable versions of the API are packaged on pypi.python.org, with the package name "context.api"

To install the latest stable version:

```
$ pip install context.api
```

To install the current development version in development mode:

```
$ git clone https://github.com/shish/context-apis.git
$ pip install -e ./context-apis/python/
```


To use:

```
import context.api as ctx

ctx.set_log("file:///tmp/my-app-log.ctxt")

ctx.log_start("test", bookmark=True)
ctx.log_endok()
```

(see https://github.com/shish/context-apis for a language-neutral overview of
which functions are available)
