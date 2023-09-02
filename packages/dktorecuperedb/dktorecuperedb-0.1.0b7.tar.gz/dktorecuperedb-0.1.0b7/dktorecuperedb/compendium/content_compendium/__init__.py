import os
import sys
import logging
from ._collection2data import _collectionkey2data

class Compendium:
    """
    Compendium class handles the functionalities related to the Compendium module.

    Attributes:
        key (str): The key attribute.
        title (str): The title attribute.
        text (str): The text attribute.
        collection (str): The collection attribute.
        language (str): The language attribute.
        disambiguation (str): The disambiguation attribute.
        default (bool): The default attribute.
        author (str): The author attribute.
        editor (str): The editor attribute.

    :func fetch_names: Récupère la liste des variantes du sous-compendium.
    :func fetch_variantes: Récupère la liste des variantes du sous-compendium.
    :func get_prayer: Récupère le texte de la prière du sous-compendium.
    """

    def __init__(self,
                 key:str=None,  # TODO : verifier qu'a tous les appels args=val !
                 usage:str=None,
                 title:str=None, text:str=None, collection:str=None,
                 disambiguation:str=None, language:str=None, default:bool=None,
                 author:str=None,editor:str=None
                 ):
        """
        Initialise une instance de la classe SubclassCompendium.
        """

        self.key = key
        self.title = title
        self.text = text
        self.collection = collection
        self.language = language
        self.disambiguation = disambiguation # par exemple, dominicain ou missel
        self.default = default
        self.author = author
        self.editor = editor
        self.default = default
    #endDef

    def fetch_names(self)->list:
        """
        Récupère la liste des variantes

        :return: Liste des variantes.
        :rtype: list
        """

        return (("name1", "variante1"),("name1", "variante2"), ("name2",))
    #endDef


    def fetch_variantes(self)->list:
        """
        Récupère la liste des variantes

        :return: Liste des variantes.
        :rtype: list
        """

        return ("variante1", "variante2")
    #endDef

    def get_prayer(self)->str:
        """
        Récupère le texte de la prière du sous-compendium.

        :return: Texte de la prière.
        :rtype: str
        """

        # Appel DB
        return "<p>Ma pri&eacute;re</p>"
    #endDef

    def get_content(self):
        #sys.stderr.write("Please use get_text")
        # Fetch content
        exec_code = self.fetch_content()

        content = {}

        if exec_code == 0:
            content[self.key] = {
                "name": self.title,
                "collection": self.collection,
                "disambiguation":self.disambiguation,
                "language":self.language,
                "content": self.text,
                "author": self.author,
                "editor": self.editor,
            }
            content["status"] = 202
        else:
            logging.warning(f"content_compendium : {self.__dict__}")
            content["status"] = exec_code
        #

        return content

    def get_text(self):
        # Fetch content
        self.name2data()

        return self.text


    def to_dict(self)->dict:
        """
        Convert to dict
        :return: {key, name, collection, disambiguation, language, content, author, editor}
        :rtype: dict
        """
        return {
            "key":self.key,
            "name": self.title,
            "collection": self.collection,
            "disambiguation":self.disambiguation,
            "language":self.language,
            "content": self.text,
            "author": self.author,
            "editor": self.editor,
        }
    #endDef

    from ._fetch_content import fetch_content, set_from_db #TODO : fetch_content : ajouter option "return dict" + si plusieurs, creer une liste pour chaque attribu
    from ._fetch_index import fetch_index

    from ._get_index import get_index

    from ._get_whatever_i_can import get_whatever_i_can

    @classmethod
    def get_url(cls, elt):

        coll = None
        ttl = None
        dis = None
        lang = None

        if isinstance(elt, dict):
            coll = elt['collection']
            ttl =  elt['title']
            dis = elt.get("disambiguation", None)
            lang = elt.get("language", None)
        elif isinstance(elt, Compendium):
            coll = elt.collection
            ttl = elt.title
            dis = elt.disambiguation
            lang = elt.language
        #endIf

        url = os.environ.get('API_URL', 'http://localhost:8000')
        url += f"/v1/Compendium/{coll}/{ttl}"

        if dis is not None:

            url += f"?dis={dis}"

            if lang is not None:
                url +=f"&lang={lang}"
            #endIf

        elif lang is not None:
            url +=f"?lang={lang}"
        #endIf

        return url
    #endDef

    @staticmethod
    def collectionkey2data(usage:str="hymne_mariale"):
        return _collectionkey2data(usage=usage)
    #endIf

#endClass
