"""
 Static (Passive and active) types generated using Stub_HC_TF
"""
from ofjustpy_engine import HC_Div_type_mixins as TR

from .composed_SHC import generator as HC_generator
from .Div_TF import gen_Div_type
from .HC_TF import gen_HC_type
from .HC_TF import HCType
from .ofjustpy_utils import traverse_component_hierarchy
from .ui_styles import basesty
from .ui_styles import sty


class PassiveComponents:
    Label = gen_HC_type(HCType.passive, "Label", TR.LabelMixin, stytags=sty.label)

    Span = gen_HC_type(HCType.passive, "Span", TR.SpanMixin, stytags=sty.span)

    Li = gen_HC_type(HCType.passive, "Li", TR.LiMixin, stytags=sty.li)

    P = gen_HC_type(HCType.passive, "P", TR.PMixin, stytags=sty.P)

    Prose = gen_HC_type(HCType.passive, "P", TR.PMixin, stytags=sty.prose)

    Option = gen_HC_type(HCType.passive, "Option", TR.OptionMixin, stytags=sty.option)

    Hr = gen_HC_type(HCType.passive, "Hr", TR.HrMixin, stytags=sty.hr)

    Img = gen_HC_type(HCType.passive, "Img", TR.ImgMixin, stytags=sty.img)

    H1 = gen_HC_type(HCType.passive, "H1", TR.H1Mixin, stytags=sty.h1)
    H2 = gen_HC_type(HCType.passive, "H2", TR.H2Mixin, stytags=sty.h2)
    H3 = gen_HC_type(HCType.passive, "H3", TR.H3Mixin, stytags=sty.h3)
    H4 = gen_HC_type(HCType.passive, "H4", TR.H4Mixin, stytags=sty.h4)
    H5 = gen_HC_type(HCType.passive, "H5", TR.H5Mixin, stytags=sty.h5)
    H6 = gen_HC_type(HCType.passive, "H6", TR.H6Mixin, stytags=sty.h6)

    # Div component types
    Div = gen_Div_type()
    Container = gen_Div_type(stytags=sty.container)
    LabelDiv = gen_Div_type(HCType.passive, "Label", TR.LabelMixin, stytags=sty.label)
    StackV = gen_Div_type(stytags=sty.stackv)
    StackH = gen_Div_type(stytags=sty.stackh)
    StackW = gen_Div_type(stytags=sty.stackw)
    Ul = gen_Div_type(HCType.passive, "Ul", TR.UlMixin, sty.ul)
    Collapsible = gen_Div_type(
        HCType.passive, "Collapsible", TR.CollapsibleMixin, sty.collapsible
    )
    # ChartJS  = gen_HC_type(HCType.passive, "ChartJS", TR.ChartJSMixin,
    #                        stytags=sty.chartjs
    #                   )
    Code = gen_Div_type(HCType.passive, "Code", TR.CodeMixin, stytags=sty.code)
    Pre = gen_Div_type(HCType.passive, "Pre", TR.CodeMixin, stytags=sty.pre)
    Nav = gen_Div_type(HCType.passive, "Nav", TR.NavMixin, stytags=sty.nav)
    Footer = gen_Div_type(HCType.passive, "Footer", TR.FooterMixin, stytags=sty.footer)
    A = gen_HC_type(HCType.passive, "A", TR.AMixin, stytags=sty.A)

    (
        Halign,
        Valign,
        SubheadingBanner,
        SubsubheadingBanner,
        Subsection,
        Subsubsection,
        Title,
        SubTitle,
        StackG,
        TitledPara,
    ) = HC_generator(Span, StackV, Div, H3, Prose)


class ActiveComponents:
    Span = gen_HC_type(HCType.active, "Span", TR.SpanMixin, stytags=sty.span)

    Button = gen_HC_type(HCType.active, "Button", TR.ButtonMixin, stytags=sty.button)
    TextInput = gen_HC_type(
        HCType.active, "TextInput", TR.TextInputMixin, stytags=sty.input
    )

    Img = gen_HC_type(HCType.active, "Img", TR.ImgMixin, stytags=sty.img)

    # ========================= CheckboxInput ========================
    def cb_hook(ufunc):
        """
        a wrapper over user event handler to
        update msg.value with checked value
        """

        def wrapper(dbref, msg, to_shell):
            print("cb_hook wrapper invoked")

            msg.value = msg.checked
            return ufunc(dbref, msg, to_shell)

        return wrapper

    CheckboxInputBase = gen_HC_type(
        HCType.active, "CheckboxInput", TR.CheckboxInputMixin, stytags=sty.input
    )

    class CheckboxInput(CheckboxInputBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, event_prehook=ActiveComponents.cb_hook, **kwargs)

    Textarea = gen_HC_type(
        HCType.active, "Textarea", TR.TextareaMixin, stytags=sty.input
    )
    Div = gen_Div_type(HCType.active, hc_tag="ActiveDiv")
    StackH = gen_Div_type(stytags=sty.stackh, hc_tag="AStackH")
    Select = gen_Div_type(
        HCType.active, "Select", TR.SelectInputMixin, stytags=sty.select
    )

    def form_hook(ufunc):
        """
        a pre-hook called before user function is called.
        pre-hook will perform data validation before invoking user response
        """

        def validate_wrapper(dbref, msg, to_shell_target):
            print("invoking from pre-hook")
            print("num comps = ", len(dbref.components))
            print(type(dbref))
            # for citem in dbref.components:
            for citem, pitem in traverse_component_hierarchy(dbref):
                if hasattr(citem, "key"):
                    print(citem.key, " ", citem, " ")
                    print(msg.value)
                    if hasattr(citem, "data_validators"):
                        print("child has data_validator ", citem.data_validators)

            return ufunc(dbref, msg, to_shell_target)
            pass

        return validate_wrapper

    FormBase = gen_Div_type(HCType.active, "Form", TR.FormMixin, stytags=sty.form)

    class Form(FormBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, event_prehook=ActiveComponents.form_hook, **kwargs)
            for citem, pitem in traverse_component_hierarchy(self):
                if hasattr(citem, "key"):
                    print(citem.key, " ", citem, " ")
                    if hasattr(citem, "data_validators"):
                        print("child has data_validator ", citem.data_validators)

    A = gen_HC_type(HCType.active, "A", TR.AMixin, stytags=sty.A)

    pass
