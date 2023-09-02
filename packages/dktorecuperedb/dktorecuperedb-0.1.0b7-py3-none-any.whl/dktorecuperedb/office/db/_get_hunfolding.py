def get_hunfolding(self, calendar, date_office, name_office, source_office="aelf", details:bool=False, as_alternative:bool=False): #->list(dict(str))
    """ details : name and reference"""

    # non retourne: "cle_deroule", "cle_element", "id_deroule"
    keys_hunfolding = [
        "key",
        "key_name",
        "name",
        "gloria_patri",
        "same_page",
        "default_element_key"
    ]

    keys_table=[f"{self.db_thunfolding_name}.{e}" for e in keys_hunfolding]

    query=f"""
SELECT {",".join(keys_table)}
FROM {self.db_thunfolding_name}
WHERE {self.db_thunfolding_name}.sequence_name = ?
ORDER BY {self.db_thunfolding_name}.id_key
"""

    out = self.request_db(query, (name_office,))
    datas_out = [{keys_table[i].split(".")[1]:e[i] for i in range(len(e))} for e in out]

    if details:
        keys_hunfolding = [
            "id_deroule",
        ]

        keys_table=[f"{self.db_thunfolding_name}.{e}" for e in keys_hunfolding]

        # non retourne: "cle_element", "cle_office", "id_element"
        keys_elements = [
            "titre",
            "editeur",
            "auteur",
            "reference"
        ]
        keys_table=keys_table + [f"tabletmp.{e}" for e in keys_elements]

        query=f"""
SELECT {','.join(keys_table)}
FROM {self.db_thunfolding_name}
LEFT JOIN (
   SELECT * FROM {self.db_telement_name}
   UNION
   SELECT * FROM  {self.db_tadditionnal_name}
) AS tabletmp
ON  tabletmp.cle_element = {self.db_thunfolding_name}.cle_element
WHERE (
  (
    tabletmp.id_office = (
      SELECT {self.db_tinfo_name}.id_office
      FROM {self.db_tinfo_name}
      WHERE {self.db_tinfo_name}.calendrier=?
        AND {self.db_tinfo_name}.date=?
        AND {self.db_tinfo_name}.nom=?
        AND {self.db_tinfo_name}.source=?
    )
   OR (
     tabletmp.id_office IS NULL
    )
  )
  AND tabletmp.texte IS NOT NULL
  AND {self.db_thunfolding_name}.nom_office = ?
)
ORDER BY  {self.db_thunfolding_name}.id_deroule
        """
        datas_out_tmp = {e['id_deroule']:e for e in datas_out}
        out = self.request_db(query, (calendar, date_office, name_office, source_office, name_office))
        out1 = [{keys_table[i].split(".")[1]:e[i] for i in range(len(e))} for e in out]
        out2 = {e['id_deroule']:e for e in out1}

        for k, v in out2.items():

            if k in datas_out_tmp.keys():
                del v['id_deroule']

                if not any(v.values()):
                    continue
                #endIf

                v["key"] = "aelf"

                if as_alternative:
                    alt = datas_out_tmp[k].get('alternative', [])

                    if not alt or not isinstance(alt, list) or not isinstance(alt, tuple):
                        datas_out_tmp[k]['alternative'] = [v,]
                    else:
                        datas_out_tmp[k]['alternative'] = datas_out_tmp[k]['alternative'] + [v,]
                    #endIf
                else:
                    for kk, vv in v.items():
                        if datas_out_tmp[k].get(kk, False):
                            # La cle existe deja et n'est pas nulle
                            continue
                        #
                        datas_out_tmp[k][kk] = vv
                    # endFor

                #endIf

            #endIf

        #endFor

    #endIf

    return datas_out
#endIf
