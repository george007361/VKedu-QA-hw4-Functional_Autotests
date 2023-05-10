import random
import string


def RandomText(aLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(aLength))
