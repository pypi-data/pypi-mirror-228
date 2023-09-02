def get_index(self):
    """Return a prayer
    # dis = disambiguation
    # lang = language
"""
    try:
        content = {"index":[]}
        i = 0

        for elt in self.fetch_index():

            if "title" in elt.keys():



                if not elt["title"] in content.keys():
                    content[elt["title"]] = {}
                #endIf


                if (
                        "COUNT(disambiguation)" in elt.keys() and
                        "COUNT(language)" in elt.keys() and
                        (
                            elt["COUNT(disambiguation)"] > 1 or
                            elt["COUNT(language)"] > 1 ) ):
                    del elt["key"]
                #
                if (
                        "COUNT(disambiguation)" in elt.keys() and
                        elt["COUNT(disambiguation)"] > 1 ):
                    del elt["disambiguation"]
                #
                if (
                        "COUNT(language)" in elt.keys() and
                        elt["COUNT(language)"] > 1 ):
                    del elt["language"]
                #

                i = len(content[elt["title"]])
                content[elt["title"]][i] = elt

                url = self.get_url(elt)

                content[elt["title"]][i]["url"] = url
                content["index"] += [url,]

            elif "key" in elt.keys():

                content[elt["key"]] = elt
                content["index"] += [elt["key"],]

            else:

                content["index"] += [elt,]

            #endIf

        #EndFor

        #TODO : gerer si erreur (par exemple, pas de donnee trouvee)

        #content = f"Coucou compendium : collection={collection} ; name={name} ; disambiguation={dis} ; language={lang}"
    except:
        content = {}
        raise Exception("COMP IDX 1")
    #endTry

    return content
#endDef
