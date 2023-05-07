import random
import string


def RandomText(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))
