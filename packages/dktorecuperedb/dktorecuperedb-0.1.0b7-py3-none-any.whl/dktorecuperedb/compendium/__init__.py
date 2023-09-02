from .content_compendium import Compendium
from .content_sequence import Sequence
#from .sequence import ClassSequence


def compendium_content(
        key:str=None,
        usage:str=None,
        collection:str=None,
        name:str=None,
        dis:str=None,
        lang:str=None,
        return_all_datas:bool=True,
):
    raise Exception("Legacy ! Please use 'Compendium.get_content' or 'Compendium.get_index' now")

#endDef

#

__all__ = ["Compendium", "Sequence"]
