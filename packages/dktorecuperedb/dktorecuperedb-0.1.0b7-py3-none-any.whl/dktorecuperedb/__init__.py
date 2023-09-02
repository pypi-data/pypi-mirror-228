"""
Database
"""

from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
    __pkg_name__,
)

from .bible import Bible, BibleOneYear
from .compendium import Compendium, Sequence, compendium_content
from .office import Office

def getOffice(office, calendar, date, format_output):
    """Get the office

:param str office: the name of the office
:param str calendar: the date
:param str date: the date
:param str format_output: the outputformat
"""
    o = Office(
        calendar=calendar,
        office=office,
        date=date,
        format_output=format_output)
    o.check_input()
    return o.get_office()
#

def getCompendium(
        collection:str=None,
        name:str=None,
        dis:str=None,
        lang:str=None,
):
    """Get the compendium
:param str collection: the collection of the element
:param str name: name of the element
:param str dis: disambiguation (fe : "Nicée-Constantinople" for Credo)
:param str lang: the language
"""
    return compendium_content(collection=collection, name=name, dis=dis, lang=lang)

def getBible(book:str=None, ref:str=None):
    """
Get a passage of the Bible
:param str book: name (or short-name) of the book
:param str ref: the reference inside the book chapter:verse,verse-verse (, = concat ; - = passage)
"""
    b = Bible(book=book, ref=ref)
    b.ref2text()
    return b.text


__all__ = [
    '__author__', '__author_email__',
    '__copyright__', '__description__', '__license__',
    '__title__', '__version__', '__pkg_name__',
    "Bible", "BibleOneYear",
    "Compendium", "Sequence",
    "Office",
    "getOffice", "getCompendium"

]
