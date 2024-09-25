class Caesar:
    def __init__(self):
        self._key = 0  

    def get_key(self):
        return self._key

    def set_key(self, key):
        self._key = key

    def encrypt(self, plaintext):
        ciphertext = ''
        for char in plaintext:
            if char.isalpha():
                shifted = ord(char.lower()) + self._key
                shifted = (shifted - ord('a')) % 26 + ord('a')
                ciphertext += chr(shifted)
            elif char.isspace():
                ciphertext += char
            else:
                ciphertext += chr((ord(char) + self._key) % 128)
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        for char in ciphertext:
            if char.isalpha():
                shifted = ord(char.lower()) - self._key
                shifted = (shifted - ord('a')) % 26 + ord('a')
                plaintext += chr(shifted)
            elif char.isspace():
                plaintext += char
            else:
                plaintext += chr((ord(char) - self._key) % 128)
        return plaintext


if __name__ == '__main__':
    cipher = Caesar()
    cipher.set_key(3)
    print(cipher.encrypt('hello WORLD!')) 
    print(cipher.decrypt('KHOOR zruog$'))  
    
    cipher.set_key(6)
    print(cipher.encrypt('zzz'))  
    print(cipher.decrypt('FFF')) 
    
    cipher.set_key(-6)  
    print(cipher.encrypt('FFF'))  