"""
mixins to put together a functioning HC/Div type:


"""
from addict_tracking_changes import Dict
from py_tailwind_utils import conc_twtags
from py_tailwind_utils import dget
from py_tailwind_utils import remove_from_twtag_list
from py_tailwind_utils import tstr

from .HC_type_mixins_extn import *


class IdMixin:
    def __init__(self, *args, **kwargs):
        self.attrs.id = kwargs.get("id", None)  # cls.stub.spath #cls.next_id
        self.domDict.id = self.attrs.id

    @property
    def id(self):
        return self.domDict.id

    @id.setter
    def id(self, value):
        self.domDict.id = value
        self.attrs.id = value


class jpBaseComponentMixin:
    """
    all attributes related to working with justpy-svelte framework;
    required to satisfy HTMLComponents.svelte processing
    """

    def __init__(self, **kwargs):
        self.domDict.vue_type = "html_component"
        self.domDict.show = kwargs.get("show", True)
        self.domDict.debug = kwargs.get("debug", False)
        self.domDict.events = []

        pass


class HTMLBaseComponentExtnMixin:
    """
    Extension to HTMLBaseComponentCoreMixin with less commonly used attributes
    "accesskey": Provides a shortcut key to activate/focus an element. This is not very commonly used, as the exact behavior can vary between browsers and can conflict with shortcut keys used by the browser or the operating system.
    "contenteditable": Specifies whether the content of an element is editable or not. This is not commonly used, as it's generally more common to use form elements (like <input> and <textarea>) for user input.
    "dir": Specifies the text direction for the content in an element. This is used when dealing with right-to-left languages like Arabic or Hebrew.
    "draggable" and "dropzone": Used for drag-and-drop functionality. These are not commonly used, as drag-and-drop is not a common requirement for most web applications.
    "lang": Specifies the language of the element's content. This is not commonly used, as the language is typically set on the <html> tag for the whole document.
    "spellcheck": Specifies whether the element is to have its spelling and grammar checked or not. This is not commonly used, as it's generally more common to rely on browser defaults or user settings.
    "tabindex": Specifies the tabbing order for an element. This is not commonly used, as the default tabbing order (following the order of elements in the HTML) is usually sufficient.
    "title": Specifies extra information about an element. This is not commonly used, as it's generally more common to provide necessary information directly in the content.

    """

    def __init__(self, **kwargs):
        # self.domDict = kwargs.get('domDict')
        # self.attrs = kwargs.get('attrs')
        # used global attributes
        for k in [
            "accesskey",
            "contenteditable",
            "dir",
            "draggable",
            "dropzone",
            "lang",
            "spellcheck",
            "tabindex",
            "title",
        ]:
            if k in kwargs:
                self.attrs[k] = kwargs.get(k)

    # global attributes
    @property
    def contenteditable(self):
        return self.attrs.get("contenteditable", None)

    @contenteditable.setter
    def contenteditable(self, value):
        if value is not None:
            self.attrs["contenteditable"] = value

    @property
    def dir(self):
        return self.attrs.get("dir", None)

    @dir.setter
    def dir(self, value):
        if value is not None:
            self.attrs["dir"] = value

    @property
    def tabindex(self):
        return self.attrs.get("tabindex", None)

    @tabindex.setter
    def tabindex(self, value):
        if value is not None:
            self.attrs["tabindex"] = value

    @property
    def title(self):
        return self.attrs.get("title", None)

    @title.setter
    def title(self, value):
        if value is not None:
            self.attrs["title"] = value

    @property
    def accesskey(self):
        return self.attrs.get("accesskey", None)

    @accesskey.setter
    def accesskey(self, value):
        if value is not None:
            self.attrs["accesskey"] = value

    @property
    def draggable(self):
        return self.attrs.get("draggable", None)

    @draggable.setter
    def draggable(self, value):
        if value is not None:
            self.attrs["draggable"] = value

    @property
    def lang(self):
        return self.attrs.get("lang", None)

    @lang.setter
    def lang(self, value):
        if value is not None:
            self.attrs["lang"] = value

    @property
    def spellcheck(self):
        return self.attrs.get("spellcheck", None)

    @spellcheck.setter
    def spellcheck(self, value):
        if value is not None:
            self.attrs["spellcheck"] = value


class HCTextMixin:
    """
    text attribute for HC components like button, span, label
    """

    def __init__(self, *args, **kwargs):
        """
        constructor
        """
        if "text" in kwargs:
            self.domDict.text = kwargs.get("text")

    # getter/setters
    @property
    def text(self):
        return self.domDict.get("text", None)

    @text.setter
    def text(self, value):
        if value is not None:
            self.domDict["text"] = value


class DivMixin:
    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "div"
        self.domDict.class_name = "Div"

    pass

    @property
    def html_tag(self):
        return self.domDict.html_tag

    @html_tag.setter
    def html_tag(self, value):
        self.domDict.html_tag = value


class TwStyMixin:
    """
    define tailwind and style attributes
    """

    def __init__(self, *args, **kwargs):
        self.twsty_tags = kwargs.get("twsty_tags", [])
        if not self.twsty_tags:
            self.domDict.classes = ""
        else:
            self.domDict.classes = tstr(*self.twsty_tags)

        if "style" in kwargs:
            self.attrs["style"] = kwargs.get("style")

    def remove_twsty_tags(self, *args):
        for _ in args:
            remove_from_twtag_list(self.twsty_tags, _)
        self.domDict.classes = tstr(*self.twsty_tags)

    def add_twsty_tags(self, *args):
        self.twsty_tags = conc_twtags(*self.twsty_tags, *args)
        self.domDict.classes = tstr(*self.twsty_tags)  # change the domDict directly

    def replace_twsty_tags(self, *args):
        """
        replace the existing twsty_tags with ones in *args
        """
        self.twsty_tags = args
        self.domDict.classes = tstr(*self.twsty_tags)  # change the domDict directly
        pass

    @property
    def style(self):
        return self.attrs.get("style", None)

    @property
    def classes(self):
        return self.domDict.get("classes", None)

    @style.setter
    def style(self, value):
        if value is not None:
            self.attrs["style"] = value


class DOMEdgeMixin:
    """
    enable building DOM tree;
    attaches ability to attach self to a parent component
    """

    def __init__(self, *args, **kwargs):
        if "a" in kwargs:
            if kwargs["a"] is not None:
                kwargs["a"].add_component(self)


class EventMixin:
    """
    for active components.
    attach event handlers to HC;

    """

    def __init__(self, *args, **kwargs):
        self.domDict.event_modifiers = Dict()
        self.domDict.transition = None
        self.allowed_events = [
            "click",
            "mouseover",
            "mouseout",
            "mouseenter",
            "mouseleave",
            "input",
            "change",
            "after",
            "before",
            "keydown",
            "keyup",
            "keypress",
            "focus",
            "blur",
            "submit",
            "dragstart",
            "dragover",
            "drop",
            "click__out",
        ]
        self.event_handlers = {}

        # event_prehook applies to all the events
        # get handler via event_prehook(func) and call
        # that when invoked
        self.event_prehook = kwargs.get("event_prehook", None)
        self.set_keyword_events(**kwargs)
        pass

    def set_keyword_events(self, **kwargs):
        for e in self.allowed_events:
            for prefix in ["", "on", "on_"]:
                if prefix + e in kwargs.keys():
                    fn = kwargs[prefix + e]
                    self.on(e, fn)
                    break

    def on(
        self,
        event_type,
        func,
        *,
        debounce=None,
        throttle=None,
        immediate=False,
    ):
        if event_type in self.allowed_events:
            if not self.event_prehook:
                self.event_handlers["on_" + event_type] = func
            else:
                self.event_handlers["on_" + event_type] = self.event_prehook(func)
                pass

            if event_type not in self.domDict.events:
                self.domDict.events.append(event_type)
            # if debounce:
            #     self.domDict.event_modifiers[event_type].debounce = {
            #         "value": debounce,
            #         "timeout": None,
            #         "immediate": immediate,
            #     }
            # elif throttle:
            #     self.domDict.event_modifiers[event_type].throttle = {
            #         "value": throttle,
            #         "timeout": None,
            #     }
        else:
            raise Exception(f"No event of type {event_type} supported")

    def add_prehook(self, prehook_func):
        """
        apply prehook to all the registered event handlers
        """
        for e in self.allowed_events:
            if "on_" + e in self.event_handlers:
                ufunc = self.event_handlers["on_" + e]
                self.event_handlers["on_" + e] = prehook_func(ufunc)

    def remove_event(self, event_type):
        if event_type in self.domDict.events:
            self.domDict.events.remove(event_type)

    def has_event_function(self, event_type):
        if getattr(self, "on_" + event_type, None):
            return True
        else:
            return False

    def add_event(self, event_type):
        if event_type not in self.domDict.allowed_events:
            self.allowed_events.append(event_type)

    def get_event_handler(self, event_type):
        return self.event_handlers[event_type]

    def add_allowed_event(self, event_type):
        self.add_event(event_type)

    @property
    def events(self):
        return self.domDict.events

    @events.setter
    def events(self, value):
        self.domDict.events = value

    # @property
    # def event_modifiers(self):
    #     return self.domDict.event_modifiers

    # @event_modifiers.setter
    # def event_modifiers(self, value):
    #     self.domDict.event_modifiers = value

    @property
    def event_propagation(self):
        return self.domDict.get("event_propagation", None)

    @event_propagation.setter
    def event_propagation(self, value):
        if value is not None:
            self.domDict["event_propagation"] = value
