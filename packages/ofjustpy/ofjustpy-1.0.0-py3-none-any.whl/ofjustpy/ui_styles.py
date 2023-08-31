import os

from . import basesty
from . import chartjssty as chartjs
from . import monalwikisty as monalwiki
from . import snowsty as snow
from . import unsty as un
from . import versasty as versa

styles = {
    "snow": snow,
    "chartjs": chartjs,
    "monalwiki": monalwiki,
    "versa": versa,
    "un": un,
}


sty = styles["snow"]

if "OJSTY" in os.environ:
    sty = styles[os.environ["OJSTY"]]


def set_style(label="snow"):
    global sty
    sty = styles[label]
