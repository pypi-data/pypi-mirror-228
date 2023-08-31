# deck example
import ofjustpy as oj
from py_tailwind_utils import *

app = oj.load_app()

labels = [oj.Mutable.Label(text="mytext1", key="mylabel1"),
          oj.Mutable.Label(text="mytext2", key="mylabel2"),
          oj.Mutable.Label(text="mytext3", key="mylabel3"),
          oj.Mutable.Label(text="mytext4", key="mylabel4"),
          ]

mydeck = oj.Mutable.StackD(key="mydeck",
                           childs=labels,
                           height_anchor_key="mylabel1",
                           
                           twsty_tags=[W/"1/2"])

idx = 1
def on_btn_click(dbref, msg, target_of):
    global idx
    mydeck_shell = target_of(mydeck)
    mydeck_shell.bring_to_front(labels[idx].id)
    idx = (idx + 1)%4
    pass

        
mybtn = oj.AC.Button(key="mybtn",
                   text="abtn",
                   pcp=[W/32, H/32, bg/rose/6],
                   on_click=on_btn_click
                   )

wp_endpoint = oj.create_endpoint(key="example_005",
                                 childs = [mydeck,
                                           mybtn
                                           ],
                                 title = "example_005"
                                 

                                 )
app.add_jproute("/", wp_endpoint)

