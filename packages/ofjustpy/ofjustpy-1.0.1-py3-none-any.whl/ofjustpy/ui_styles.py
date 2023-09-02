import os
import sys
import importlib
from . import snowsty as snow
from . import unsty as un


styles = {
    "snow": snow,
    "un": un,
}


sty = styles["snow"]
if "OJSTY" in os.environ:
    print("Loading custom module")
    OJSTY_MODULE_NAME = os.environ["OJSTY"]
    sys.path.append(os.path.dirname(OJSTY_MODULE_NAME))
    sty = importlib.import_module(os.path.basename(OJSTY_MODULE_NAME))

def set_style(label="snow"):
    global sty
    sty = styles[label]
    print("Changing sty to ", sty)
