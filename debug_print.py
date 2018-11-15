# -*- coding: UTF-8 -*-
#    Copyright 2017, 2018 Michael Schwager

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# File: debug_print.py
#       print debugging information with various controls, because I generally
#       program in bugs (my language of choice).
#
#       ...that's a joke.
#
#       This was designed to work with kivy, although that's not necessary
#       (only if you print_widget_ancestry). That's not a joke.

from __future__ import print_function
import traceback
import sys


# There are two ways to use this: as a Singleton, all controlled by this global
# debug_flag. Or you can instantiate an object of class Debug, and print using the
# object's print method. The upside is that the latter can be controlled on a file-by-file
# basis.
debug_flag = False


def set_debug_flag(flag):
    global debug_flag
    debug_flag = flag


def debug_print(*args, **kwargs):
    if not debug_flag:
        return
    trace = traceback.extract_stack()
    # print (len(trace))
    this_entry=trace[len(trace)-2]
    basename = this_entry[0].split('/')
    basename = "%-10s" % basename[len(basename)-1]
    method = this_entry[2] + "()"
    method = "%-15s" % method
    print (basename + ":" + str(this_entry[1]), method, *args, **kwargs)


def debug_widget_title(widget):
    try:
        title = widget.title
    except AttributeError:
        title = "No title"
    return title


class Debug():
    """
    Instantiate this bad boy in your file, and you can turn it on and off as you
    wish in your file. Then you can print debug messages, like so:

    from kivydnd.debug_print import Debug
    debug = Debug(True)

    debug.print ("Here's a message")

    Output looks like this:

    dndwidgets.py:453 on_drag_finish() beginning, parent: <kivy.core.window.window_sdl2.WindowSDL object at 0x7f707ef0a2f0> copy? False
    dndwidgets.py:454 on_drag_finish() self: <draggablestuff.DraggableButton object at 0x7f707eec0d70> is_double_tap? False

    That is, it prints:

    filename:line_number method()  <your_text_here>

    If debug_flag is False, printing will be shut off. However, this can be overridden
    see the print() method.
    """
    def __init__(self, *args, **kwargs):
        """

        :param debug_flag: This is a normal argument. Value: True or False.
        False will disable debug output.
        :param register:  This is a keyword argument. Set to a hexadecimal value,
        which would be considered a debug level. If during your debug.print() call
        you give it a "level" keyword argument, the level will be AND'ed against the
        register variable. If true, the debug.print() will generate output.

        For example:
        debug = Debug(register=0x01)
        """
        global debug_flag
        self.debug_flag=debug_flag
        for arg in args:
            self.debug_flag = arg
        self.register = kwargs.pop("register", 0x00)
        file = kwargs.pop("file", None)
        err = kwargs.pop("err", None)
        if file is not None:
            self.out_fp = open(file)
        else:
            self.out_fp = sys.stdout
        if err is not None:
            self.err_fp = open(file)
        else:
            self.err_fp = sys.stderr


    def _print(self, *args, **kwargs):
        """
        If the debug_flag is False this will not print. However, this can be overridden
        by either:
        1. By setting the keyword "definitely" to "True" in the debug.print() call, or
        2. By setting the keyword "level" to a hexadecimal flag value. If that value when
           AND-ed against the register value is truthy *, then the print will occur.
           * see https://stackoverflow.com/questions/39983695/what-is-truthy-and-falsy-in-python-how-is-it-different-from-true-and-false)
        For example:
        debug = Debug(register=0x01)

        :param args: The stuff to be printed.
        :param kwargs: definitely, or level
        :return: nothing
        """
        definitely = kwargs.pop('definitely', False)
        level = kwargs.pop('level', 0x00)
        fp = kwargs.pop('fp')
        if not definitely:
            if not (level & self.register):
                if not self.debug_flag:
                    return
        trace = traceback.extract_stack()
        # print (len(trace))
        this_entry = trace[len(trace) - 2]
        basename = this_entry[0].split('/')
        basename = "%-10s" % basename[len(basename) - 1]
        method = this_entry[2] + "()"
        method = "%-15s" % method
        print(basename + ":" + str(this_entry[1]), method, args, kwargs, file=fp)

    def print(self, *args, **kwargs):
        self._print(*args, **kwargs, fp=self.out_fp)

    def err_print(self, *args, **kwargs):
        self._print(*args, **kwargs, fp=self.err_fp)

    def print_trace(self, *args, **kwargs):
        definitely = kwargs.pop('definitely', False)
        level = kwargs.pop('level', 0x00)
        if not definitely:
            if not (level & self.register):
                if not self.debug_flag:
                    return
        traceback.print_stack()

    def print_widget_ancestry(self, widget, *args, **kwargs):
        import kivy.core.window._window_sdl2

        definitely = kwargs.get('definitely',False)
        if not definitely:
            if not self.debug_flag:
                return
        self.print ("ancestry:", widget, definitely=definitely)
        i=0
        while not isinstance(widget, kivy.core.window.window_sdl2.WindowSDL):
            print ("ancestry:", widget.parent)
            widget=widget.parent
            i = i + 1
            if i > 20:
                print ("ancestry: too deep, introspection ended.")
                return (0)
        return(1)
