"""
Defines all the mixins that will make
up the WebPage class type.

The mixins can be used to define: passive, active, or mutable Webpage.
Currently, only mutable WebPage type is being created.
WebPageMixin provides all the heavy lifting code that WebPage class is required
to do: like handling events, talking to frontend, etc. 

"""
import json

from addict_tracking_changes import Dict
from ofjustpy_engine import HC_Div_type_mixins as TR
from ofjustpy_engine.WebPage_type_mixin import WebPageMixin

from .tracker import trackStub


class StaticCoreBaseMixin(
    TR.IdMixin,
    TR.jpBaseComponentMixin,
    TR.EventMixin,
):
    def __init__(self, *args, **kwargs):
        self.domDict = Dict()
        self.attrs = Dict()
        self.key = kwargs.get("key", None)
        assert self.key is not None
        TR.IdMixin.__init__(self, *args, **kwargs)
        TR.jpBaseComponentMixin.__init__(self, **kwargs)

        # We haven't yet jsonified domDict.event_modifiers
        TR.EventMixin.__init__(self, *args, **kwargs)

        # json_domDict is initialized after id is assigned
        self.json_domDict = None
        self.json_attrs = None

    def get_domDict_json(self):
        # json_domDict is jsonified after tracker has assigned a ID
        if not self.json_domDict:
            self.json_domDict = json.dumps(self.domDict, default=str)[1:-1]
        return self.json_domDict

    def get_attrs_json(self):
        if not self.json_attrs:
            self.json_attrs = json.dumps(self.attrs, default=str)[1:-1]
        return self.json_attrs


class HCCMutableCore(
    StaticCoreBaseMixin,
):
    # behaves same as StaticCoreBaseMixin
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.childs = kwargs.get("childs")


class HCCMutable_Mixin:
    """
    contains id/event/reactive childs
    adding children and building json is delayed
    """

    def __init__(self, **kwargs):
        # childs are assumed to be mutable
        # and are added via add_components
        self.components = []
        self.spathMap = Dict(track_changes=True)
        self.add_register_childs()

    def add_register_childs(self):
        for c in self.staticCore.childs:
            # register the child (only active child will register)
            c_ = c.stub()
            # attach the child as part of self.target.components
            c_(self)
            # staic components do not have ref/id/spath for
            # them to be tracked
            if not c_.is_static():
                self.spathMap[c_.id] = c_.target

    def add_component(self, child, position=None, slot=None):
        """
        add a component

        Args:
            child: the component to add
            position: the position to add to (append if None)
            slot: if given set the slot of the child
        """
        if slot:
            child.slot = slot
        if position is None:
            self.components.append(child)
        else:
            self.components.insert(position, child)

        return self


def gen_WebPage_type(staticCoreMixins=[], mutableShellMixins=[]):
    class WebPage_MutableShell(WebPageMixin, HCCMutable_Mixin, *mutableShellMixins):
        def __init__(self, *args, **kwargs):
            # should be part StaticCoreSharerBaseMixin:
            self.staticCore = kwargs.get("staticCore")
            WebPageMixin.__init__(self, *args, **kwargs)
            HCCMutable_Mixin.__init__(self, *args, **kwargs)
            for _ in mutableShellMixins:
                _.__init__(self, *args, **kwargs)

        def react(self):
            # Not sure what the purpose of this is
            pass

        @property
        def id(self):
            return self.staticCore.id

        def stub(self):
            return gen_Stub_WebPage(staticCore=self, **self.kwargs)

    class Stub_WebPage:
        def __init__(self, *args, **kwargs):
            self.kwargs = kwargs

        @classmethod
        def is_static(cls):
            return False

        def __call__(self):
            self.target = WebPage_MutableShell(**self.kwargs)
            return self.target

        @property
        def key(self):
            return self.kwargs.get("key")

        @property
        def id(self):
            return self.kwargs.get("staticCore").id

    @trackStub
    def gen_Stub_WebPage(**kwargs):
        page_stub = Stub_WebPage(**kwargs)
        return page_stub

    class WebPage_StaticCore(HCCMutableCore, *staticCoreMixins):
        def __init__(self, *args, **kwargs):
            HCCMutableCore.__init__(self, **kwargs)
            self.key = kwargs.get("key")
            self.id = None
            for _ in staticCoreMixins:
                _.__init__(self, *args, **kwargs)
            self.kwargs = kwargs
            self.args = args

        def stub(self):
            return gen_Stub_WebPage(staticCore=self, *self.args, **self.kwargs)

    return WebPage_StaticCore


WebPage = gen_WebPage_type()
