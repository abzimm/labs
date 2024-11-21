def shift_char(char: str, key: int) -> str:
    if char.isalpha():
        base = ord('a')
        shifted = ord(char.lower()) + key
        return chr((shifted - base) % 26 + base)
    elif char.isspace():
        return char
    else:
        return chr((ord(char) + key) % 128)

def encrypt(text: str, key: int) -> str:
    return ''.join(shift_char(char, key) for char in text)

def decrypt(text: str, key: int) -> str:
    return encrypt(text, -key)

if __name__ == '__main__':
    test_key = 3
    print(encrypt('hello WORLD!', test_key))
    print(decrypt('KHOOR zruog$', test_key))
    
    test_key_2 = 6
    print(encrypt('zzz', test_key_2))
    print(decrypt('FFF', test_key_2))
    
    test_key_3 = -6
    print(encrypt('FFF', test_key_3))