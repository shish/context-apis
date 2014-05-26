package main

import (
	//ctx "github.com/shish/context-apis/go/context"
	ctx "./context"
	"time"
	"sync"
)

var myLock sync.Locker

func main() {
	myLock = &ctx.LockWrapper{&sync.Mutex{}, "lock542452", "Example Lock"}
	ctx.SetLogFile("file://demo.ctxt")
	go thing()
	go thing()
	time.Sleep(3 * time.Second)
}

func thing() {
	ctx.LogStart("test", true, true)
	myLock.Lock()
	time.Sleep(1 * time.Second)
	myLock.Unlock()
	ctx.LogEndok("test")
}
