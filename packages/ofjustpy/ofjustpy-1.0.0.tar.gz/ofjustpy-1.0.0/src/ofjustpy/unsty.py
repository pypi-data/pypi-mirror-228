from py_tailwind_utils import *

h1 = [xl3, lh.normal, lh.normal]

h2 = [fz.lg, lh.normal, fw.semibold]  # "prose", "prose-2xl"

h3 = [fz.lg, fw.semibold, lh.normal]  # "prose", "prose-2xl"

h4 = [fz._, lh.normal, fw.semibold]  # "prose", "prose-2xl"

h5 = [fz._, lh.normal, fw.semibold]  # "prose", "prose-2xl"

h6 = [fz._, lh.normal, fw.semibold]  # "prose", "prose-2xl"

para = [base, fw.light, relaxed]

ul = [li.disc]
ol = [W / "1/2", li.disc]
img = []
li = []
button = [bold, outline._, shadow._, shadow.sm, tt.u]

title_text = [xl6, fw.bold]
subtitle_text = [xl4, fw.medium]

heading_box = [db.f, jc.around]
heading_text = [*h1, fw.bold]
subheading_box = [db.f, jc.around]
subheading_text = [*h2, fw.bold]

subsubheading_text = [*h3, fw.medium, W / 96]

spacing = []
centering_div = [db.f, jc.center]
span = []

form = [db.f, jc.center]
theme = []
P = []
A = [*hover()]

stackv = [db.f, flx.col]
stackh = [db.f]
stackw = [db.f, flx.wrap, jc.center]
stackd = [db.f]
_ = dbr = Dict()
_.banner = []
_.result = [hidden / ""]

border_style = []

icon_button = [ta.center, shadow.md, *hover()]

theme = []

heading = heading_box
heading2 = subheading_box
heading_span = heading_text
heading2_span = subheading_text

prose = [prose.lg]

divbutton = [db.f, jc.center]

expansion_item = []

inputJbutton = [flex, jc.center, *border_style]
select = [fz.sm]
selectwbanner = []

infocard = []

barpanel = []

slider = [H / 6, db.f, ai.center]
circle = [W / 6, H / 6, bdr.full, *hover(noop / bds.double, noop / bt.bd)]

expansion_item = []

textarea = [fz.sm, fw.bold, fw.light, ta.center, W / "full", H / "full"]

textinput = [db.f, jc.center]
input = []

cell = [fz.xl]

left_cell = [*cell, ta.end, W / "5/12"]
right_cell = [*cell, ta.start, W / "5/12"]
eq_cell = [*cell, ta.center, op.c]

option = []
label = [db.f, jc.center]

wp = []

nav = [container, top / 0]
footer = [container]
div = []

hr = [container]


def stackG(num_cols, num_rows):
    return [db.g, G / cols / f"{num_cols}", G / rows / f"{num_rows}", gf.row]


def get_color_tag(colorname):
    return globals()[colorname]


def build_classes(*args):
    return tstr(*args)


td = [bt.bd, ta.center]
tr = []

tbl = [fz.sm, tbl.auto, W / full, ovf / auto, ovf / x / auto]

expansion_container = [fz.lg]

togglebtn = []

checkbox = []


def halign(align="center"):
    """
    align the contents : options are start, end, center, between, evenly, around
    """
    return [db.f, getattr(jc, align)]


def valign(align="center"):
    """
    align the contents : options are start, end, center, between, evenly, around
    """
    return [db.f, getattr(ai, align)]


def align(halign="center", valign="center"):
    """
    vertical and horizonal align
    """
    return [db.f, getattr(ai, valign), getattr(jc, halign)]


container = [container]

default_border = [bd / 2, bdr.lg]
dockbar = [*stackh, jc.center, W / full, H / 16]
code = []
pre = []
collapsible = []
chartjs = []
