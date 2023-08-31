"""
A single API to generate various types of mutable Div: HCCMutable, HCCStatic, Mutable
"""
import json

from addict_tracking_changes import Dict

from . import HC_Div_type_mixins as TR
from .mutable_TF_impl import CoreChildMixin
from .mutable_TF_impl import DivMutable_JsonMixin
from .mutable_TF_impl import HCCMixin_MutableChilds
from .mutable_TF_impl import HCCMixin_StaticChilds
from .mutable_TF_impl import HCCMutable_JsonMixin
from .mutable_TF_impl import HCCStatic_JsonMixin
from .mutable_TF_impl import StaticCore_JsonMixin
from .mutable_TF_impl import StaticCoreSharer_BaseMixin
from .mutable_TF_impl import StaticCoreSharer_ClassesMixin
from .mutable_TF_impl import StaticCoreSharer_EventMixin
from .mutable_TF_impl import StaticCoreSharer_HCCStaticMixin
from .mutable_TF_impl import StaticCoreSharer_IdMixin


def classTypeGen(
    hc_tag="Div",
    hctag_mixin=TR.DivMixin,
    static_core_mixins=[],
    mutable_shell_mixins=[],
    is_childs_mutable=True,
    is_self_mutable=False,
):
    assert is_childs_mutable or is_self_mutable

    if is_self_mutable:
        core_mixins = [
            TR.IdMixin,
            TR.jpBaseComponentMixin,
            TR.EventMixin,
            StaticCore_JsonMixin,
            CoreChildMixin,
            hctag_mixin,
        ]
        shell_mixins = [
            TR.TwStyMixin,
            StaticCoreSharer_EventMixin,
        ]
        static_core_sharer = [
            StaticCoreSharer_BaseMixin,
            StaticCoreSharer_IdMixin,
        ]

    else:
        core_mixins = [
            TR.jpBaseComponentMixin,
            TR.TwStyMixin,
            StaticCore_JsonMixin,
            CoreChildMixin,
            hctag_mixin,
        ]

        shell_mixins = []
        static_core_sharer = (StaticCoreSharer_BaseMixin, StaticCoreSharer_ClassesMixin)

    if is_childs_mutable:
        shell_mixins.append(HCCMixin_MutableChilds)

    else:
        core_mixins.append(HCCMixin_StaticChilds)
        static_core_sharer.append(StaticCoreSharer_HCCStaticMixin)

    match is_self_mutable, is_childs_mutable:
        case False, True:
            shell_mixins.append(HCCMutable_JsonMixin)
            pass
        case True, True:
            shell_mixins.append(DivMutable_JsonMixin)
        case True, False:
            shell_mixins.append(HCCStatic_JsonMixin)
        case _:
            assert False

    shell_mixins.append(TR.DOMEdgeMixin)

    class StaticCore(*core_mixins, *static_core_mixins):
        def __init__(self, *args, **kwargs):
            self.domDict = Dict()
            self.attrs = Dict()
            self.key = kwargs.get("key", None)
            for _ in core_mixins:
                _.__init__(self, *args, **kwargs)

            for _ in static_core_mixins:
                _.__init__(self, *args, **kwargs)

    class MutableShell(
        *static_core_sharer,
        *shell_mixins,
        *mutable_shell_mixins,
    ):
        def __init__(self, *args, **kwargs):
            self.domDict = Dict(track_changes=True)
            self.attrs = Dict(track_changes=True)
            for _ in static_core_sharer:
                _.__init__(self, *args, **kwargs)

            for _ in shell_mixins:
                _.__init__(self, *args, **kwargs)

            for _ in mutable_shell_mixins:
                _.__init__(self, *args, **kwargs)

            pass

    return StaticCore, MutableShell
