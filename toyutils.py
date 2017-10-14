"""
    @author ksdme
    @created 26 August 2017 IST
    reusable utilities
"""
from math import floor
from time import time
from json import dumps
from base64 import b64encode
from rsa.pkcs1 import VerificationError
from rsa import sign, verify, PublicKey, PrivateKey

# required constant, helps during translation
# of the public key from a number to string
_MAP_GEN_TUPLE = ([(str(l), chr(l+97)) for l in xrange(0, 26)] +
                  [(str(l), chr(l+39)) for l in xrange(26, 52)] +
                  [(str(l), chr(l-4))  for l in xrange(52, 62)])

# useful when translating from pub key to alpha
_KEY_TRANSLATE_MAP_FORWARD = dict(_MAP_GEN_TUPLE)

# used when translating from alpha to pub key
_KEY_TRANSLATE_MAP_BACKWARD = dict(map(
    lambda elm: (elm[1], elm[0]), _MAP_GEN_TUPLE))

class enum(object):
    """
        make an subclass act like its
        an enum class
    """

    def __setattr__(self, key, val):
        return

def validate_wallet(wallet):
    """
        validate if the wallet instance
        passed is indeed an tuple of length
        two and the first and second keys r
        true
    """
    flag = True

    flag = isinstance(wallet, tuple)
    flag = flag and len(wallet) == 2

    flag = flag and isinstance(wallet[0], PublicKey)
    flag = flag and isinstance(wallet[1], PrivateKey)

    return flag

def validate_wallet_address(addr):
    """
        validates a wallet address,
        it only does a syntactic validation
        of the address
    """

    return True

def validate_block_hash(hesh):
    """
        validates the hash of the block
        basically it validates that the
        given hash is a valid md5
    """

    return True

def sign_txn(wallet, payload, encode=True):
    """
        signs a payload using the
        given wallet key
    """
    assert isinstance(payload, str)

    ret = sign(payload, wallet[1], "MD5")

    if encode:
        ret = b64encode(ret)

    return ret

def verify_output_sign(pub_key, output):
    """
        validate a given txn,
        simply checks if the public key
        can validate the signature
    """

    partial_output = {
        "as": output["as"],
        "amt": output["amt"]
    }

    # again sort it before dumping
    partial_output = sort_by_alpha(partial_output)
    partial_output = dumps(partial_output)

    # validate it here
    try:
        verify(partial_output, partial_output["sign"], pub_key)
        return True
    except VerificationError:
        return False

def get_time_milli():
    """
        get the current time in milliseconds,
        its a bit useful since the block was
        made earlier
    """
    return floor(time()*1000)

def sort_by_alpha(pay):
    """
        sorts a given pay dict
        by its keys
    """
    assert isinstance(pay, dict)
    return dict(sorted(pay.iteritems(), key=lambda elm: elm[0]))

def transform_pub_key_to_alpha(key):
    """
        transforms a given pub key into
        an alphanumeric key used for txn
    """
    key, transformed = str(key), ""
    current, key_len = 0, len(key)

    while current < key_len:
        partial = key[current]
        try:
            transformed += _KEY_TRANSLATE_MAP_FORWARD[partial+key[current+1]]
            current += 2
        except (KeyError, IndexError):
            transformed += _KEY_TRANSLATE_MAP_FORWARD[partial]
            current += 1

    return transformed

def transform_alpha_to_pub_key(key):
    """
        transforms a given alpha numeric
        key into its pub key form
    """
    transformed, key = "", str(key)
    for elm in key:
        transformed += _KEY_TRANSLATE_MAP_BACKWARD[elm]

    return transformed
