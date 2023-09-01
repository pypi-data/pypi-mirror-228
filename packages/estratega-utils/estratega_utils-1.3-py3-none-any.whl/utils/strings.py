import unicodedata
import random
import string


def remover_acentos(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def clean(input_str):
    str = input_str.replace(" ", "").lower()
    nfkd_form = unicodedata.normalize('NFKD', str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


DEFAULT_KEY: int = 7


def generar_random_str(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def cifrar(string: str, key: int = DEFAULT_KEY):
    cadena_cifrada: str = ''
    for s in string:
        ascii_code = ord(s) + key
        random_caracter = generar_random_str(1)
        cadena_cifrada += chr(ascii_code) + random_caracter
    return cadena_cifrada


def descifrar(string: str, key: int = DEFAULT_KEY):
    cadena_descifrada: str = ''
    for index, s in enumerate(string):
        if index % 2 == 0:
            ascii_code = ord(s) - key
            cadena_descifrada += chr(ascii_code)
    return cadena_descifrada
