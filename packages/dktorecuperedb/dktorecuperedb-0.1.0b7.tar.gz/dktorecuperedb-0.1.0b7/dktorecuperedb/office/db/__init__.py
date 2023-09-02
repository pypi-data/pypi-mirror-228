import os
from threading import Lock # verrou

from dktoeasysqlite3 import MyDB

class OfficeDB(MyDB):
    def __init__(self):
        self.db_path=os.path.abspath(os.environ.get("RECUPEREDB_OFFICE_PATH", "./datas/compendium.db"))

        self.db_thunfolding_name=os.environ.get("RECUPEREDB_OFFICE_HUNFOLDING_NAME", "sequence")
        self.db_tadditionnal_name=os.environ.get("RECUPEREDB_OFFICE_ADDITIONNAL_NAME", "content")

        super().__init__(lock_in=Lock())

        self.to_html=True

    #endDef

    #
    # from ._get_office import get_office
    # get_office(nom, date, calendrier)
    # - aller chercher la cle dans aelf_info a partir de nom, date, calendrier
    # - si n'existe pas : REQUETE à AELF pour remplir aelf_data + aelf_info
    # return : dico complet avec elements office + infos (donc retourne tout ce qu'AELF donne)

    # from ._get_office import get_office_keys
    # get_office_keys(nom, date, calendrier)
    # return : clé des éléments [introduction, hymne, antienne 1, psaume 1, ...] qui ne sont pas vides !
    # return : None si tous sont vides

    # from ._get_info import get_info
    # get_info(date, calendrier)
    # si necessaire : REQUETE à AELF
    # return les infos comme sur AELF

    from ._add_additionnal import add_additionnal
    from ._add_hunfolding import add_hunfolding
    from ._get_hunfolding import get_hunfolding

#endClass
