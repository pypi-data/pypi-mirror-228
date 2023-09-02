import os
import sys
import json

from dktotoolkit import parser_date, compat_mode
#from . import call_api(source=aelf, ...)
#from . import parser(dico/list/str, output_format)

def _todict(obj):
    # https://github.com/matthewwithanm/python-markdownify/blob/develop/markdownify/__init__.py
    return dict((k, getattr(obj, k)) for k in dir(obj) if not k.startswith('_'))
#

"""
Database:
---------

* All datas are in HTML - ascii

[office] :
- id_office => index
- source       = source de l'office = aelf uniquement pour le moement
- date_requete = yyyy-mm-dd
- zone         = calendrier  (AELF)
- calendrier   = calendrier  (dans le cas ou on utilise la zone "romain" pour un calendrier francais par exemple)
- date         = yyyy-mm-dd  (AELF)
- nom          = nom de l'office (AELF)
- couleur      = couleur liturgique (AELF)
- annee        = A, B ou C (pour les messes uniquement) (AELF)
- temps_liturgique = (AELF)
- semaine = (AELF)
- jour = (AELF)
- jour_liturgique_nom = (AELF)
- fete = (AELF)
- degre = (AELF)
- ligne1 = (AELF)
- ligne2 = (AELF)
- ligne3 = (AELF)
- couleur2 = (AELF)
- couleur3 = (AELF)

[liaison] :
- id_office
- id_element
- cle_element

[element] :
- id_element
- titre
- texte
- editeur
- auteur
- reference
# Remarque : a la difference d'AELF, je renvoie toujours cette structure, et éléments vides avec None

[deroule]:
- id_deroule => index
- nom_office
- id_deroule : position (exemple : intro des vepres = 0, confiteor des vepres = 1, hymne des vepres = 2, ...)
- cle_element : exemple : "psaume1", "antienne1" : bref, les cles d'AELF
- titre_particulier : pour forcer le titre
- ajouter_doxologie : ajouter la doxologie apres l'element s'il n'est pas vide
- element_defaut : aelf ou nom de la variante dans la BD compendium


                +--------------+
                |   office     |
                +--------------+
                  | id_office (PK)
                  | ...
                  |
                  |     +----------------+
                  |     |   liaison      |
                  |     +----------------+
                  |     | id_office (FK) |
                  |     | id_element (FK)|
                  |     | cle_element    |
                  |     +----------------+
                  |
                  |     +-----------------+
                  +---->|    element      |
                  |     +-----------------+
                  |     | id_element (PK) |
                  |     | titre           |
                  |     | texte           |
                  |     | editeur         |
                  |     | auteur          |
                  |     | reference       |
                  |     +-----------------+
                  |
                  |     +-------------------+
                  +---->|    deroule        |
                        +-------------------+
                        | id_deroule (PK)   |
                        | nom_office        |
                        | id_deroule        |
                        | cle_element       |
                        | titre_particulier |
                        | ajouter_doxologie |
                        | element_defaut    |
                        +-------------------+

"""

class Office(object):
    """
RECUPERER LES INFOS DU BOT (office)

:param list(str) available_source: = ["aelf", ]
:param list(str) available_format_output: = ["html", "markdown"]
:param list(str) available_calendar: = ["francais", "romain"]
:param list(str) available_office: = ["vepres", "complies"] #TODO : a remplir !!

:param str format_output: Format de sortie
:param str date: date (YYYY-MM-DD) Date de l'office
:param str calendar: Calendrier / zone utilisé
:param str office: nom de l'office
:param str source: source principale de l'office (uniquement AELF actuellement)
"""
    class DefaultOptions:
        available_source = ["aelf", ]
        available_format_output = ["simple_html", "clean_html", "html", "markdown", "discord", "native"]
        available_calendar = ["romain", "france", "luxembourg", "belgique"]
        available_office = ["laudes", "sextes", "nones", "vepres", "complies", "lectures", "messe"]

        date="today"
        calendar="france"
        source="aelf"

        format_output="html"

        use_hunfolding=False

        details=False
    #

    class Options(DefaultOptions):
        use_hunfolding=True
        format_output="discord"
        pass
    #

    def __init__(self, **kwargs):
        """
Constructeur

:param str formatting: [html, markdown] format de sortie
:param str calendar: calendrier
:param str|Date date: date de l'office
:param str office: nom de l'office
:param str source: source (AELF uniquement actuellement)
"""
        # Create an options dictionary. Use DefaultOptions as a base so that
        # it doesn't have to be extended.
        # https://github.com/matthewwithanm/python-markdownify/blob/develop/markdownify/__init__.py

        self.options = _todict(self.DefaultOptions)
        self.options.update(_todict(self.Options))

        kwargs = compat_mode("date", ["jour", "day"], replace_in_kwargs=True, **kwargs)
        kwargs = compat_mode("office", ["name", "nom"], replace_in_kwargs=True, **kwargs)
        kwargs = compat_mode("calendar", ["calendrier", ], replace_in_kwargs=True, **kwargs)

        self.options.update(kwargs)

        self.format_output = self.options.get("format_output", None).lower()
        self.date = parser_date(self.options.get("date", None).lower())  # Appeler la fonction "convert_date" ou jsp comment : YYYY-MM-DD
        self.calendar = self.options.get("calendar", None).lower()
        self.source = self.options.get("source", None).lower()
        self.office = self.options.get("office", None).lower()

    #endDef


    # Update
    from ._update_hunfolding import update_hunfolding

    from ._check_input import check_input

    from ._get_info_from_db import get_info_from_db
    from ._get_office import get_office
    from ._get_hunfolding import get_hunfolding
    from ._get_alternatives import get_alternatives

    from ._hunfolding_from_json import hunfolding_from_json

    def update_attributes(self, format_output:str=None,**kwargs):
        """
        Update attributes of the class from the kwargs
        """
        if format_output is None:
            pass
        elif not isinstance(format_output, str):
            sys.stderr.write(f"> Office.get_office(): format_output={format_output} must be a string\n")
        elif format_output.lower() in self.available_format_output:
            self.format_output = format_output.lower()
        elif format_output.lower() not in self.available_format_output:
            sys.stderr.write(f"> Office.get_office(): format_output={format_output} not available ; please use one in {self.available_format_output}\n")
        else:
            sys.stderr.write(f"> Office.get_office(): format_output={format_output} unexpected\n")
        #endIf

        return kwargs
    #endDef

    def update_db(self):
        self.update_hunfolding()
    #endDef



#endClass
