import logging
import sys

def check_input(self):

    """
    Vérifie les paramètres d'entrée de l'objet OfficeAELF.

    :returns: Un dictionnaire contenant le statut de vérification.
        - Si les paramètres sont valides, le dictionnaire contient {"status": "200"}.
        - Si des erreurs sont détectées, le dictionnaire contient {"status": "404", "error": "<liste_des_erreurs>"}.
    :rtype: dict
    """

    err = []
    if self.format_output.lower() not in self.options["available_format_output"]:
        msg = f"OfficeAELF.__init__() : formatting = {self.format_output}, not in {self.options['available_format_output']} ! I'll use '{self.options['available_format_output'][0]}'"
        logging.warning(msg)
        err += [msg,]
        self.format_output = self.options['available_format_output'][0]
    #endIf

    if self.calendar.lower() not in self.options["available_calendar"]:
        msg=f"OfficeAELF.__init__() : calendar = {self.calendar}, not in {self.options['available_calendar']} !  I'll use '{self.options['available_calendar'][0]}'"
        logging.warning(msg)
        err += [msg,]
        self.calendar = self.options['available_calendar'][0]
    #endIf

    if self.source.lower() not in self.options["available_source"]:
        msg=f"OfficeAELF.__init__() : source = {self.source}, not in {self.options['available_source']} ! I'll use '{self.options['available_source'][0]}'"
        logging.warning(msg)
        err += [msg,]
        self.source = self.options['available_source'][0]
    #endIf

    if self.office is None or not isinstance(self.office, str):
        msg=f"OfficeAELF.__init__() : office = {self.office}, not in {self.options['available_office']} ! STOP 1"
        logging.error(msg)
        err += [msg,]
        self.office = None
    elif self.office.lower() not in self.options["available_office"]:
        msg=f"OfficeAELF.__init__() : office = {self.office}, not in {self.options['available_office']} ! STOP 2"
        logging.error(msg)
        err += [msg,]
        #self.office = None
    #endIf

    if err:
        sys.stderr.write(">>"+"\n>>".join(err))
        return {"status" : 404, "error" : "\n".join(err)}
    else:
        return {"status":200}
    #endIf

    return {"status":-1, "error":"unexpected"}
#endDef
