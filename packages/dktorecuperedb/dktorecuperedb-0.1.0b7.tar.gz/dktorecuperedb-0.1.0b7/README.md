[![Latest Release](https://framagit.org/discord-catho/module_recupere_db/-/badges/release.svg)](https://framagit.org/discord-catho/module_recupere_db/-/releases)
[![pipeline status](https://framagit.org/discord-catho/module_recupere_db/badges/main/pipeline.svg)](https://framagit.org/discord-catho/module_recupere_db/-/commits/main)

---

[![coverage report](https://framagit.org/discord-catho/module_recupere_db/badges/main/coverage.svg)](https://discord-catho.frama.io/module_recupere_db/coveragepy_report/)
[![PEP8-Critical](https://img.shields.io/endpoint?url=https://discord-catho.frama.io/module_recupere_db/badges/pep8-critical.json)](https://discord-catho.frama.io/module_recupere_db/flake8_report/)
[![PEP8-NonCritical](https://img.shields.io/endpoint?url=https://discord-catho.frama.io/module_recupere_db/badges/pep8-noncritical.json)](https://discord-catho.frama.io/module_recupere_db/flake8_report/)
[![PEP8-Rate](https://img.shields.io/endpoint?url=https://discord-catho.frama.io/module_recupere_db/badges/pep8-rate.json)](https://discord-catho.frama.io/module_recupere_db/flake8_report/)
[![Profiling](https://img.shields.io/static/v1?label=Profiling&message=yep&color=informational)](https://discord-catho.frama.io/module_recupere_db/profiler_report)

---

[![Downloads](https://pepy.tech/badge/dktorecuperedb/month)](https://pepy.tech/project/dktorecuperedb)
[![Supported Versions](https://img.shields.io/pypi/pyversions/dktorecuperedb.svg)](https://pypi.org/project/dktorecuperedb)

---

[![Catholic project](https://img.shields.io/static/v1?label=catholic&message=unofficial&color=orange&style=plastic&logo=feathub)]()

---


# Installer ce module en local (après `$ git clone ...`):
```
$ cd /path/module_recupere_db
$ pip install -e .[doc]
```

# Variables d'environnement :
## Offices

* RECUPEREDB_OFFICE_PATH : (default: ./datas/office.db)
* RECUPEREDB_OFFICE_JSONPATH : (default:  {RECUPEREDB_OFFICE_PATH}/../office/{self.office}.json)
* RECUPEREDB_OFFICE_INFO_NAME :  (default: office_info)
* RECUPEREDB_OFFICE_ELEMENT_NAME : (default: office_element)
* RECUPEREDB_OFFICE_HUNFOLDING_NAME : (default: office_deroule)
* RECUPEREDB_OFFICE_ADDITIONNAL_NAME : (default : office_addition)

## Compendium
* RECUPEREDB_COMPENDIUM_PATH : (default:./datas/compendium.db)
* RECUPEREDB_COMPENDIUM_CONTENT_NAME : (default: content)
* RECUPEREDB_COMPENDIUM_SEQUENCE_NAME : (default: sequence)
* RECUPEREDB_COMPENDIUM_COLLECTION_NAME : (default: content_collection)

## Bible

* RECUPEREDB_BIBLE_PATH : (default: ./datas/bible.db)
* RECUPEREDB_BIBLE_NAME : (default: verses)

### 1 an
* RECUPEREDB_BIBLE1YEAR_PATH : (default: ./datas/bible1year.db)
* RECUPEREDB_BIBLE1YEAR_NAME : (default: bible_references)

# TODO :
* Unifier les bases de données avec différentes tables

## Remarques :
* Je mets à jour pip23.1.2

* N'ont pas fonctionnés dans le fichier setup.cfg
```
parserhtml==1.0.0 @ git+ssh://git@framagit.org:discord-catho/module_html_parser.git@v1.0.0#egg=parserhtml
parserhtml @ git+ssh://git@framagit.org:discord-catho/module_html_parser.git@v1.0.0#egg=parserhtml
easysqlite3 @ git+ssh://git@framagit.org:discord-catho/easy_sqlite3.git#egg=easysqlite3
parserhtml @ git+ssh://git@framagit.org:discord-catho/module_html_parser.git
easysqlite3 @ git+ssh://git@framagit.org:discord-catho/easy_sqlite3.git
parserhtml @ file:///home/pierre/Documents/Projets/catho/module_html_parser
easysqlite3 @ file:///home/pierre/Documents/Projets/catho/easy_sqlite3
parserhtml @ git+https://framagit.org/discord-catho/module_html_parser.git@v1.0.0#egg=parserhtml
parserhtml @ git+https://framagit.org/discord-catho/module_html_parser.git@v1.0.0#egg=parserhtml
easysqlite3 @ git+https://framagit.org/discord-catho/easy_sqlite3.git#egg=easysqlite3
```