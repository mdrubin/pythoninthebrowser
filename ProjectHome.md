# Python in the Browser #


This project is now obsolete. It has been replaced by:

# [Try Python](http://code.google.com/p/pythoninthebrowser/) #


An interactive [Python](http://www.python.org) interpreter that runs in the browser, using [Silverlight 2](http://silverlight.net/GetStarted/) and [IronPython](http://www.codeplex.com/IronPython).

This is ideal for tutorials and documentation, where example Python code can actually be tried in the browser. The demo has some examples 'built in' that demonstrate one way it could be used.

It requires Silverlight 2, and the Python version is 2.5.

The interpreter runs in an HTML textarea, with Javascript that communicates with Silverlight and prevents you deleting text from the console except after the interactive prompt.

Target browsers are Firefox 2 & 3, Safari and IE 7 & 8. (It won't work in other browsers until there is a version of Silverlight that works with them.)

The project is a combination of IronPython (for the interpreter loop), Javascript (for the 'console behaviour' in the textarea) and C# (as a helper to call into Silverlight from Javascript).  On every keypress Javascript calls into IronPython (via the C#!). If the keypress is an 'enter', then it pushes the current line into the interpreter loop (which uses the standard library [code module](http://docs.python.org/lib/module-code.html)). Stdout is diverted to print into the textarea, where tracebacks are also sent. If you are attempting to type over, or delete, previous output then the keypress is cancelled.

Silverlight 2 is currently only available for Windows and Mac OS X, with the Firefox, Safari or IE browsers. Linux support is in the works via the [Moonlight project](http://www.mono-project.com/Moonlight) from Mono.