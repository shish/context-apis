Context API (Go) - ALPHA
~~~~~~~~~~~~~~~~~~~~~~~~

To use:

```
package main

import (
	ctx "./context"
	"time"
)

func main() {
	ctx.SetLogFile("file://demo.ctxt")
	ctx.LogStart("test", true, true)
	time.Sleep(1 * time.Second)
	ctx.LogEndok("test")
}
```

(see https://github.com/shish/context-apis for a language-neutral overview of
which functions are available)

