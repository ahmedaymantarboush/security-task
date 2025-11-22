from .technique import Technique


class CaesarCipher(Technique):
    """
    Implementation of the Caesar Cipher.
    A simple substitution cipher where each letter is shifted by a fixed number of positions.
    """
    def __init__(self, offset=None):
        self._offset = offset

    def set_offset(self, offset = None):
        """
        Set the shift offset for the cipher.
        If not provided, prompts the user for input (CLI mode).
        """
        offset = self._offset if offset is None else offset
        offset = int(input("Enter the offset value for Caesar Cipher (default 1): ") or 1) if offset is None else offset
        offset = offset % 26
        self._offset = offset
        return self._offset

    def encrypt(self, plaintext, offset=None):
        """
        Encrypt the plaintext by shifting characters.
        
        Args:
            plaintext (str): The text to encrypt.
            offset (int): The shift amount (optional).
            
        Returns:
            str: The encrypted ciphertext.
        """
        ciphertext = ""
        offset = self.set_offset(offset) if offset is None else offset
        for char in str(plaintext):
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            if char.isalpha():
                # Shift character and wrap around alphabet
                char_offset = (ord(char) - base + offset) % 26
                ciphertext += chr(base + char_offset)
            else:
                # Keep non-alphabetic characters unchanged
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext, offset=None):
        """
        Decrypt the ciphertext by shifting characters back.
        """
        offset = self.set_offset(offset) if offset is None else offset
        # Decryption is just encryption with negative offset
        return self.encrypt(ciphertext, -offset)

    def brute_force(self, ciphertext):
        """
        Attempt to decrypt by trying all possible offsets (1-25).
        
        Returns:
            list: A list of all possible plaintexts.
        """
        probable_plaintexts = []
        for offset in range(1, 26):
            probable_plaintexts.append(self.encrypt(ciphertext, -offset))
        return probable_plaintexts
    
    def get_description(self):
        """Return description for UI."""
        return "Classical substitution cipher that shifts letters by a fixed offset. Simple but historically significant."
    
    def get_params(self):
        """Return parameter definitions for UI auto-generation."""
        return [
            self.create_param(
                'offset',
                'Offset (1-25, optional - will prompt if not provided)',
                'number',
                placeholder='Leave empty for interactive prompt',
                min=1,
                max=25,
                required=False
            )
        ]