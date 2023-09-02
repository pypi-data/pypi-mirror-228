from .db import OfficeDB

from dktotoolkit import ParserHTML

def get_hunfolding(self, details=False):
    """Recuperer uniquement le deroulement, retourne les donnees au format self.format_output (a priori, pas d'importance, mais bon)
TODO : sortir les références du jour !!!

    :returns:  [{"position_element_deroule", "cle_element"}]
    :rtypes: list(dict(str:str))

    Voir aussi
    ----------
    :func:`OfficeDB.get_hunfolding`
    """

    db = OfficeDB()
    self.update_db()
    datas = db.get_hunfolding(self.calendar, self.date, self.office, self.source, details=details)
    db.close()

    infos = self.call_api()["informations"]

    infos_parser = ParserHTML(
        infos,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=["date", "date_requete", "id_office"],
    )
    infos_parser.utf8_to_html(inplace=True)

    datas_parser = ParserHTML(
        datas,
        convertEmptyNone=True,
        convert_keys=False,
        skip_values=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]
    )

    datas_parser.utf8_to_html(inplace=True)

    if self.format_output == "html" :

        return {
            "informations":infos_parser.html_to_utf8(),
            self.office:datas_parser.html_to_utf8()
        }

    elif self.format_output == "markdown" :

        return {
            "informations":infos_parser.html_to_markdown(),
            self.office:datas_parser.html_to_markdown()
        }

    #endIf

    return None

#endDef
