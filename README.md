# debug_print
Python library for convenient debug printing, with some added features.

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

If debug_flag is False, printing will be shut off. However, this can be overridden see the print() method.
