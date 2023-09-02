import sys
import json
import re
import bs4

if __name__=="__main__":
    import os
    sys.path.insert(0, os.path.abspath('../..'))
#end

from dktotoolkit import ParserHTML, clean_json
from dktotoolkit.dict import unprefix_keys
from dktotoolkit import get_aelf_office
from dktotoolkit import discordify_dict
from .db import OfficeDB
from ..compendium import Compendium


SKIP_PARSER_INFOS=["date", "date_requete", "id_office"]
SKIP_PARSER_ELTS=["cle_element", "element_defaut", "reference", "id_office", "nom_office"]

KEY_NAME="key_name" # ex :cle_element

def _split_kwargs(**kwargs):
    format_kwargs = unprefix_keys(dico=kwargs, prefix="format_")
    office_kwargs = unprefix_keys(dico=kwargs, prefix="office_")
    kwargs = {k:kwargs[k] for k in set(kwargs.keys())-set(["format_"+i for i in format_kwargs.keys()]) - set(["office_"+i for i in format_kwargs.keys()])}

    return format_kwargs, office_kwargs, kwargs

def get_office(self, **kwargs)->None:
    """Recuperer tout l'office a partir de la base de donnee, retourne les donnees au format self.format_output

    :param str kwargs[format_X]: output format (format_discordwrap, format_discordwrap_width)
    :param str kwargs[office_Y]: office kwargs (office_doxologie, ...)
    :returns: office
    :rtypes: dict
    """

    check = self.check_input()
    if check.get("status", -1) not in [200, 202]:
        out = {
            "informations": {},
            self.office if self.office else "any_office":{},
        }
        out.update(check)

        return out
    #

    format_kwargs, office_kwargs, kwargs = _split_kwargs(**kwargs)

    # 3. (dict) info, (dict) hunfolding, (dict) office (=nom_office) = call_db_complet(date_office, calendrier, source="aelf"))

    hunfolding = []

    if self.options.get("use_hunfolding", False):  # https://localhost:8000/v1/Sequence/{self.office}
        db = OfficeDB()
        hunfolding = db.get_hunfolding(self.calendar, self.date, self.office, self.source, details=self.options["details"])
        db.close()
    #

    if self.source == "aelf":
        datas = get_aelf_office(office=self.office, date=self.date, zone=self.calendar, hunfolding=hunfolding)
        elements = datas[self.office]
        infos = datas["informations"]
    else:
        raise ValueError("source must be AELF")
    #

    # 4. Si formatting = html : conversion recursive
    # 4. Si formatting = markdown : conversion recursive

    # Ajout des donnees par default:
    for element in elements:
        if element.get("default_element_key", False):
            office_kwargs[element.get(KEY_NAME, None)] = element.get("default_element_key", None)
        #
    #

    # Modification des donnees (office_kwargs):
    if office_kwargs and not "doxologie" in office_kwargs.keys():
        office_kwargs["doxologie"] = "doxologie_court"
    else:
        office_kwargs = {"doxologie":"doxologie_court"}
    #endIf

    for k, v in office_kwargs.items():

        cles = [e[KEY_NAME] if KEY_NAME in e.keys() else None for e in elements]
        mask_cle = [k == e for e in cles]

        if v is None or not v or v.lower() == "aelf": # utiliser la valeur par defaut
            continue
        #endIf

        if not k in cles: # Ne pas ajouter d'element qui ne serait pas présent dans le déroulé
            sys.stderr.write(f"Key {k} is not in the hunfolding: {cles}\n")
            continue
        #endIf

        comp = {}

        try:

            comp = Compendium(key=v)   # https://localhost:8000/v1/Compendium/{v}
            content = comp.get_content()

        except Exception as e:

            print(f"dktorecuperedb.Office.get_office : Exception (1) : {e}")
            raise Exception

        #

        if content.get("status", -1) == 202:

            content_renamed={
                "titre": content[v]["name"],
                "texte": content[v]["content"],
                "editeur": content[v]["editor"],
                "auteur": content[v]["author"],
                "reference": content[v]["collection"],
                "disambiguation":content[v]["disambiguation"],
                "langue":content[v]["language"],
            }
            content = content_renamed

            for i in range(len(elements)):
                if mask_cle[i] and isinstance(content, dict):
                    for k, v in content.items():
                        elements[i][k] = v
                    #endFor
                #endIf
            #endFor
        else:
            raise
        #endIf

    #endFor

    simplify_tags = {"span:class_=verse_number":"i", "span:class_=chapter_number":"b"}

    if self.format_output is None or self.format_output.lower() in ["html", "native"]:

        datas_out = {
            "informations": infos,
            self.office:elements
        }

    elif not isinstance(self.format_output, str):

        raise ValueError(f"format_output must be a string {self.format_output}")

    elif self.format_output.lower() in ["clean_html", "simple_html"]:

        info = ParserHTML(
            infos,
            convertEmptyNone=True,
            convert_keys=False,
        ).clean_html(inplace=False, replace_tags=simplify_tags)

        elements=ParserHTML(
            elements,
            convertEmptyNone=True,
            convert_keys=False,
        ).clean_html(inplace=False, replace_tags=simplify_tags)

        datas_out = {
            "informations": infos,
            self.office:elements
        }

    elif self.format_output.lower()=="markdown":

        info = ParserHTML(
            infos,
            convertEmptyNone=True,
            convert_keys=False,
        ).to_markdown(inplace=False, replace_tags=simplify_tags, **format_kwargs)

        elements=ParserHTML(
            elements,
            convertEmptyNone=True,
            convert_keys=False,
        ).to_markdown(inplace=False, replace_tags=simplify_tags, **format_kwargs)

        datas_out = {
            "informations": infos,
            self.office:elements
        }

    elif self.format_output.lower()=="discord":

        format_kwargs["discordwrap"]=format_kwargs.get(
            "discordwrap", True
        )

        format_kwargs["discordwrap_width"]=format_kwargs.get(
            "discordwrap_width", 1020
        )
        format_kwargs["discordwrap_keeplines"]=format_kwargs.get(
            "discordwrap_keeplines", False
        )
        format_kwargs.update({"discord_key":"texte"})
        format_kwargs.update({"replace_tags":simplify_tags})

        info = ParserHTML(
            infos,
            convertEmptyNone=True,
            convert_keys=False,
        ).to_markdown(inplace=False, discord=True, **format_kwargs)

        elements=ParserHTML(
            elements,
            convertEmptyNone=True,
            convert_keys=False,
        ).to_markdown(inplace=False, discord=True, **format_kwargs)

        datas_out = {
            "informations": infos,
            self.office:elements
        }

    else:

        raise ValueError(f"format_output not expected {self.format_output}")
    #

    datas_out.update(check)
    return datas_out
#endDef
