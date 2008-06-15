# Copyright (c) 2007-8 Michael Foord.
# All Rights Reserved
#

import sys
import clr
clr.AddReference("OnKeyPress, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null")

from OnKeyPress import OnKeyPress

from System import EventHandler
from System.Windows import Application
from System.Windows.Browser import HtmlPage
from System.Windows.Controls import Canvas

from code import InteractiveConsole


ps1 = '>>> '
ps2 = '... '


class Console(InteractiveConsole):
    def write(self, data):
        HtmlPage.Document.interpreter.value += data


console = Console()
sys.stdout = console # we use the write method :-)
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

        HtmlPage.Document.interpreter.value += prompt
        return 'false'
        

onkeypress = HandleKeyPress()

    
HtmlPage.RegisterScriptableObject("onkeypress", onkeypress)    
console.write("Python %s on %s\nThe interactive browser interpreter by Michael Foord\n" % 
              (sys.version, sys.platform))
console.write(ps1)

root = Canvas()
Application.Current.RootVisual = root
