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

__version__ = '0.1.0'
doc = "Python in the browser: version %s" % __version__
banner = ("Python %s on Silverlight\nPython in the Browser %s by Michael Foord\n" 
          "Type reset() to clear the console.\n" % (sys.version, __version__))

ps1 = '>>> '
ps2 = '... '
root = Canvas()


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


class HandleKeyPress(OnKeyPress):
    
    more = False
    
    def _method(self, start, end, key):
        contents = HtmlPage.Document.interpreter.value or ''
        pos = contents.rfind('\n') + 5
        
        #HtmlPage.Document.debugging.innerHTML = 'Start: ' + str(start) + ' End: ' + str(end) + ' Pos: ' + str(pos) + '<p>'
        if (start < pos) or (end < pos):
            #HtmlPage.Document.debugging.innerHTML += '<br /> Key=%s Ord=%s' % (key, ord(key))
            return 'false'
        if ord(key) == 8 and end <= pos:
            return 'false'
        if key not in '\r\n': # IE sends \r - go figure...
            return 'true'
        
        #HtmlPage.Document.debugging.innerHTML += ' Enter... '
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


console = None
def reset():
    global console, newline_terminated
    console = Console(context.copy())
    def SetBanner():
        HtmlPage.Document.interpreter.value = banner
                  
    newline_terminated = True
    root.Dispatcher.BeginInvoke(SetBanner)


context = {
    "__name__": "__console__", 
    "__doc__": doc,
    "__version__": __version__,
    "reset": reset
}

reset()
sys.stdout = console
sys.stderr = console
console.write(ps1)

HtmlPage.Document.interpreter.SetProperty('disabled', False)
HtmlPage.Document.SilverlightControlHost.SetStyleAttribute('visible', 'false')
Application.Current.RootVisual = root
