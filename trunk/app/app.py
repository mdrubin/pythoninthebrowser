# Copyright (c) 2007-8 Michael Foord.
# All Rights Reserved
#

import sys
import clr
clr.AddReference("OnKeyPress, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null")

from OnKeyPress import OnKeyPress

from System.Windows import Application
from System.Windows.Browser import HtmlPage
from System.Windows.Controls import Canvas

from code import InteractiveConsole


root = Canvas()

ps1 = '>>> '
ps2 = '... '

# nicely format unhandled exceptions
def excepthook(sender, e):
    print Application.Current.Environment.GetEngine('py').FormatException(e.ExceptionObject)

Application.Current.UnhandledException += excepthook

# Handle infinite recursion gracefully
sys.setrecursionlimit(1000)


class Console(InteractiveConsole):
    def write(self, data):
        # Invoke it so that we can print 'safely' from another thread
        # It also makes print asynchronous!
        global newline_terminated
        newline_terminated = data.endswith('\n')
        root.Dispatcher.BeginInvoke(lambda: _print(data))

newline_terminated = True

def _print(data):
    HtmlPage.Document.interpreter.value += data
    height = HtmlPage.Document.interpreter.GetProperty('scrollHeight')
    if height:
        HtmlPage.Document.interpreter.SetProperty('scrollTop', height)


console = Console()
sys.stdout = console
sys.stderr = console


class HandleKeyPress(OnKeyPress):
    
    more = False
    
    def _method(self, start, end, key):
        contents = HtmlPage.Document.interpreter.value or ''
        pos = contents.rfind('\n') + 5
        mod = contents[:pos].count('\r\n') # the Javascript cursor code counts newlines as single characters for IE
        start += mod
        end += mod
        
        HtmlPage.Document.debugging.innerHTML = 'Start: ' + str(start) + ' End: ' + str(end) + ' Pos: ' + str(pos) + '<p>'
        if (start < pos) or (end < pos):
            HtmlPage.Document.debugging.innerHTML += '<br /> Key=%s Ord=%s' % (key, ord(key))
            return 'false'
        if ord(key) == 8 and end <= pos:
            return 'false'
        if key not in '\r\n': # IE sends \r - go figure...
            return 'true'
        
        HtmlPage.Document.debugging.innerHTML += ' Enter... '
        line = contents[pos:]
        console.write('\n')
        self.more = console.push(line)

        if self.more:
            prompt = ps2
        else:
            prompt = ps1
            if not newline_terminated:
                console.write('\n')

        root.Dispatcher.BeginInvoke(lambda: _print(prompt))
        return 'false'
        

onkeypress = HandleKeyPress()

HtmlPage.RegisterScriptableObject("onkeypress", onkeypress)

# Clear console area
HtmlPage.Document.interpreter.value = ''

console.write("Python %s on Silverlight\nPython in the Browser by Michael Foord\n" % 
              (sys.version,))
console.write(ps1)

Application.Current.RootVisual = root
