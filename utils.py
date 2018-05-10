"""
    @author ksdme
    contains the utils for
    the generak purpose stuff
"""
from re import match
from hashlib import md5
from codecs import encode

def isValidHash(hashID):
    """
        [#Invalid HashID]
        validates a given hashID and returns a boolean
    """

    return match(r"^([a-z\d]{40})$", str(hashID)) is not None

def paddedString(of, wyth, length):
    padded = str(format(ord(of), "b"))
    return (wyth*(8-len(padded)) + padded)

def toBinary(string):
    return "".join(paddedString(x, "0", 8) for x in string)

def toReadable(hexString):
    return encode(hexString, "hex").decode("utf-8")
