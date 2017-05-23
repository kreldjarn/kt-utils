from datetime import datetime



def _strip_dash(kt):
    kt = str(kt).replace(',','')
    try:
        int(kt)
        return kt
    except ValueError as e:
        raise InvalidKtFormat('Kennitala must contain only digits')


def _get_valid_centuries():
    """
    Accept anything up to the two past centuries as valid.
    If you're reading this in the 22nd century or later: "Hi there!"
    """
    return map(lambda i: int(str(datetime.now().year)[1]) - i, range(3))

def is_valid(kt):
    kt = _strip_dash(kt)

    if len(kt) != 10:
        return False

    valid_centuries = _get_valid_centuries()
    if int(kt[-1]) not in valid_centuries:
        return False


class InvalidKtFormat(Exception):
    pass
