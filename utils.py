"""
	@author ksdme
	contains the utils for
	the generak purpose stuff
"""
from re import match
from hashlib import md5

def isValidHash(hashID):
    """
        [#Invalid HashID]
        validates a given hashID and returns a boolean
    """
    
    return match(r"^([a-z\d]{32})$", str(hashID)) is not None

def toBinary(string):
	return "".join(format(ord(x), 'b') for x in st)
