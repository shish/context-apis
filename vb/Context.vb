Public Class Context
    Private Shared log_file As System.IO.StreamWriter
    Private Shared epoc As Date = CDate("1.1.1970 00:00:00")
    'Private Shared time_offset As Double
    'Private Shared stopwatch As Stopwatch = setupTimer()

    'Private Shared Function setupTimer() As Stopwatch
    'setupTimer = New System.Diagnostics.Stopwatch()
    'time_offset = DateAndTime.Now.Subtract(epoc).TotalSeconds()
    'setupTimer.Start()
    'End Function

    Private Shared Function getTime() As Double
        getTime = DateAndTime.Now.Subtract(epoc).TotalSeconds
        'getTime = (stopwatch.ElapsedTicks / stopwatch.Frequency) + time_offset
    End Function

    Private Shared Function getMethodName() As String
        Dim s As StackTrace = New System.Diagnostics.StackTrace()
        getMethodName = s.GetFrame(3).GetMethod().Name
    End Function

    Private Shared Function threadName() As String
        threadName = Threading.Thread.CurrentThread.Name
        If Not threadName Is Nothing Or threadName = "" Then
            threadName = CStr(Threading.Thread.CurrentThread.ManagedThreadId)
        End If
    End Function

    Private Shared Function compactString(ByVal o As Object) As String
        compactString = ""
        If o.GetType.IsArray Or o.GetType.IsAssignableFrom(GetType(IEnumerable)) Then
            For Each oo As Object In o
                compactString += compactString(oo)
            Next
        Else
            compactString += o.ToString + " "
        End If
    End Function


    Private Shared Function compactStrings(ByVal ParamArray o() As Object) As String
        compactStrings = compactString(o)
    End Function


    Private Shared Function genMessage(ByVal text As String, ByVal type As String) As String
        genMessage = ""
        genMessage += Format(getTime(), "0.000000") + " " ' time
        genMessage += System.Net.Dns.GetHostName + " " ' host
        genMessage += CStr(Process.GetCurrentProcess.Id) + " " ' PID
        genMessage += threadName().Replace(" ", "-") + " " ' Thread name
        genMessage += type + " "
        genMessage += getMethodName() + " "
        genMessage += text
    End Function

    Private Shared Sub logMsg(ByVal msg As String)
        Try
            If Not log_file Is Nothing Then
                log_file.WriteLine(msg)
            Else
                Debug.Print(msg)
            End If
        Catch ex As Exception
            closeLog()
        End Try
    End Sub

    Public Shared Sub setLog(ByVal filename As String)
        log_file = New System.IO.StreamWriter(filename, False)
    End Sub

    Public Shared Sub closeLog()
        Try
            log_file.Close()
        Catch ex As Exception
        End Try
        log_file = Nothing
    End Sub

    Public Shared Sub start(ByVal ParamArray text() As Object)
        logMsg(genMessage(compactStrings(text), "START"))
    End Sub
    Public Shared Sub endok(ByVal ParamArray text() As Object)
        logMsg(genMessage(compactStrings(text), "ENDOK"))
    End Sub
    Public Shared Sub ender(ByVal ParamArray text() As Object)
        logMsg(genMessage(compactStrings(text), "ENDER"))
    End Sub
    Public Shared Sub bmark(ByVal ParamArray text() As Object)
        logMsg(genMessage(compactStrings(text), "BMARK"))
    End Sub
    Public Shared Sub clear(ByVal ParamArray text() As Object)
        logMsg(genMessage(compactStrings(text), "CLEAR"))
    End Sub

End Class
