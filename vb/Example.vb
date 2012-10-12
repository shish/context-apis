Module Example
    Private Sub hello()
        Threading.Thread.Sleep(300)
        Context.start("saying hello")
        Console.Write("hello ")
        Threading.Thread.Sleep(800)
        Context.endok("finished hello")
    End Sub

    Private Sub world(ByVal i As Integer)
        For j As Integer = 0 To i
            Context.start("saying world", j)
            Console.WriteLine("world")
            Threading.Thread.Sleep(500)
            Context.endok()
        Next
    End Sub

    Sub Main()
        Context.setLog("output.vb.ctxt")
        Context.start("running program with args:", My.Application.CommandLineArgs)

        Dim t As Threading.Thread = New Threading.Thread(AddressOf hello)
        t.IsBackground = True
        t.Start()

        world(3)

        Context.endok("running program finished")
        Context.closeLog()
    End Sub
End Module