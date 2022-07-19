import binascii
import os

ALPHABET = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
DEFAULT_UUID_LENGTH = 20


def int_to_string(number: int, padding: int) -> str:
    output = ""
    alpha_len = len(ALPHABET)
    while number:
        number, digit = divmod(number, alpha_len)
        output += ALPHABET[digit]
    remainder = max(padding - len(output), 0)
    output = output + ALPHABET[0] * remainder
    return output[::-1]


def generate_uuid(length: int = DEFAULT_UUID_LENGTH) -> str:
    random_num = int(binascii.b2a_hex(os.urandom(length)), 16)
    return int_to_string(random_num, padding=length)[:length]
