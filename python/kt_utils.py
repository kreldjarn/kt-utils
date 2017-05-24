""" Various utilities to check the validity and parse information
from the Icelandic kennitala system. """

from datetime import datetime as dt


def strip_dash(func):
    def wrapper(kt):
        kt = str(kt).replace('-','')
        return func(kt)
    return wrapper


def _get_valid_centuries():
    """ Accept anything going back to the two past centuries as valid.
    If you're reading this in the 22nd century or later: "Hi there!" """
    return map(lambda i: (int(str(dt.now().year)[1]) - i) % 10, range(3))


@strip_dash
def is_valid(kt):
    """ Discerns whether a kennitala is well-formed or not.
    Does not check whether it belongs to an entity. """
    try:
        int(kt)
    except ValueError as e:
        return False

    if len(kt) != 10:
        return False

    valid_centuries = _get_valid_centuries()
    if int(kt[-1]) not in valid_centuries:
        return False

    try:
        return calculate_checksum(kt) == int(kt[8])
    except InvalidKtFormat as e:
        return False


def get_inception_date(kt):
    """ Returns birth date for humans and foundation date for LLCs. """
    if not is_valid(kt):
        raise InvalidKtFormat('Illegal kennitala')

    # Got you covered here, 22nd century buddies
    year = {'8': 1800, '9': 1900, '0': 2000, '1': 2100}[kt[9]] + int(kt[4:6])
    # Kts starting with 4+ are LLC entities.
    # The zero-padded day field (i.e. kt[:2]) is %40 in this case
    return dt.strptime('{}{}'.format(str(int(kt[:4]) % 4000), year), '%d%m%Y')


@strip_dash
def calculate_checksum(kt):
    weights = [3, 2, 7, 6, 5, 4, 3, 2]

    kt = kt[:8]
    if len(kt) < 8:
        raise InvalidKtFormat('Checksum requires 8 digits to calculate.')

    try:
        digits = map(int, kt)
    except ValueError as e:
        raise InvalidKtFormat('Kennitala must contain only digits.')
    acc = sum([d * w for d, w in zip(digits, weights)])
    modulus = acc % 11
    checksum = 11 - modulus

    if checksum == 10:
        raise InvalidKtFormat('Checksum invalid, kennitala is illegal.')
    return (11 - modulus) % 11


def get_entity_type(kt):
    kt = str(kt)
    if not is_valid(kt) or int(kt[0]) > 7:
        raise InvalidKtFormat('Illegal kennitala')
    return ('individual', 'company')[int(kt[0]) // 4]


class InvalidKtFormat(Exception):
    pass
