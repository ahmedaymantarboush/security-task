from abc import ABC, abstractmethod


class Technique(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def execute(self, option=None, input_text=None):
        option = option or input("Choose operation - Encrypt (E), Decrypt (D), Brute Force (B): ").upper()
        if (option not in ['E', 'D', 'B']):
            raise ValueError("Invalid option selected. Choose E, D, or B.")
        input_text = input_text or input("Enter the text to encrypt or decrypt: ")
        if option == 'E':
            return self.encrypt(input_text)
        elif option == 'D':
            return self.decrypt(input_text)
        elif option == 'B':
            return self.brute_force(input_text)
        else:
            raise ValueError("Invalid option selected.")
            
    @abstractmethod
    def encrypt(self):
        pass
    
    @abstractmethod
    def decrypt(self):
        pass
    
    @abstractmethod
    def brute_force(self):
        pass
