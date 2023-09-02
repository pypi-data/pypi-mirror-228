def get_whatever_i_can(self):
    """Return the index or the content
"""
    idx = self.get_index()

    if len(idx["index"]) > 1:

        return idx

    else:

        return self.get_content()

    #endIf

