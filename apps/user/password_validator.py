import re


def NumberLetterValidator(password):
    if re.match("[a-zA-Z_][0-9a-zA-Z_]*$", password):
        return True
    else:
        return False

def SymbolValidator(password):
    if not re.findall('[()[\]{}|\\`~!@#$%^&amp;*_\-+=;:\'",<>./?]', password):
        return True
    else:
        return False
