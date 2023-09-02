from ..db import CompendiumDB
from .sort_datas import sort_datas

def fetch_index(self)->None:
    """
    @input : no input
    @output: no output
    @descr: set :

    self.text
    self.collection
    self.language
    self.disambiguation
    self.author
    self.editor
    """

    c_db = CompendiumDB()

    group = None
    if self.collection is None: # Sortir la liste des collections
        list_keys = [
            "collection", "COUNT(title)"
        ]
        group="collection"
    elif self.title is None: # Sortir la liste des titres dans la collection
        list_keys = [
            "collection", "title", "COUNT(disambiguation)", "COUNT(language)", "key", "disambiguation", "language"
        ]
        group = "title"
    elif self.disambiguation is None or self.language is None : # Sortir la liste des variantes
        # http://0.0.0.0:8000/v1/Compendium/Compendium/Acte%20de%20contrition  ici
        list_keys = [
            "collection", "title", "disambiguation", "language", "key"
        ]
    else:
        list_keys = [
            "collection", "title", "disambiguation", "language"
        ]
    #endIf

    unsorted_datas = c_db.get_item_compendium(
        items=list_keys,
        collection=self.collection,
        name=self.title,
        disambiguation=self.disambiguation,
        language=self.language,
        group=group
    )

    print("OUT compendirum _get_index", unsorted_datas)
    return sort_datas(keys=list_keys, list_of_list_values=unsorted_datas)

#endDef
