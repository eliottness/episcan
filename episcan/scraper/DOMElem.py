from selenium.webdriver.common.by import By

class DOMElem:

    by        : By  # Search method to find the particular element
    value     : str # Search value
    send_keys : str # Keys to enter if the value is a field

    def __init__(self, by, val, keys=None):
        self.by         = by
        self.value      = val
        self.send_keys  = keys
