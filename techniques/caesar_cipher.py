from .technique import Technique


class CaesarCipher(Technique):
    def __init__(self, offset=None):
        self._offset = offset

    def set_offset(self, offset = None):
        offset = self._offset if offset is None else offset
        offset = int(input("Enter the offset value for Caesar Cipher (default 1): ") or 1) if offset is None else offset
        offset = offset % 26
        self._offset = offset
        return self._offset

    def encrypt(self, plaintext, offset=None):
        ciphertext = ""
        offset = self.set_offset(offset)
        for char in str(plaintext):
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            if char.isalpha():
                char_offset = (ord(char) - base + offset) % 26
                ciphertext += chr(base + char_offset)
            else:
                ciphertext += char
        return ciphertext
    
    def decrypt(self, ciphertext):
        offset = self.set_offset()
        return self.encrypt(ciphertext, -offset)

    def brute_force(self, ciphertext):
        probable_plaintexts = []
        for offset in range(1, 26):
            probable_plaintexts.append(self.encrypt(ciphertext, -offset))
        return probable_plaintexts