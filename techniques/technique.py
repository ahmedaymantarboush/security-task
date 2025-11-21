from abc import ABC, abstractmethod


class Technique(ABC):
    """
    Abstract Base Class for all encryption techniques.
    Defines the standard interface that all techniques must implement.
    """
    @abstractmethod
    def __init__(self):
        """Initialize the technique."""
        pass

    def execute(self, option=None, input_text=None):
        """
        Execute the technique based on the selected option.
        
        Args:
            option (str): 'E' for Encrypt, 'D' for Decrypt, 'B' for Brute Force.
                          If None, prompts the user (CLI mode).
            input_text (str): The text to process. If None, prompts the user.
            
        Returns:
            str or list: The result of the operation.
        """
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
    def encrypt(self, plaintext):
        """
        Encrypt the plaintext.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def brute_force(self, ciphertext):
        """
        Attempt to break the cipher.
        Must be implemented by subclasses.
        """
        pass
