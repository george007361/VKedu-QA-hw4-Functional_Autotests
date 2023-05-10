import random

class RandomData:
    latin = ["a", "b","c", "d","e", "f","g", "h","i", "j","k", "l","m", "n",
           "o", "p","q", "r","s", "t","u", "v","w", "x","y", "z"]
    def string(char_num, alph):
        str = ''
        for x in range(char_num):
            str += ''.join(random.choice(alph))
        return str