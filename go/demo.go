package main

import (
	ctx "github.com/shish/context-apis/go/context"
	"time"
)

func main() {
	ctx.SetLogFile("file://demo.ctxt")
	ctx.LogStart("test", true, true)
	time.Sleep(1 * time.Second)
	ctx.LogEndok("test")
}
