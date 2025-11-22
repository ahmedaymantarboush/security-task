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
    
    def get_extra_info(self):
        """
        Return extra information about the technique.
        Can be overridden by subclasses to provide additional metadata.
        
        Returns:
            dict: Empty dict by default. Subclasses can return custom metadata.
        """
        return {}
    
    def get_description(self):
        """
        Return a description of the technique for UI display.
        
        Returns:
            str: Brief description of the technique.
        """
        return "Encryption technique."
    
    @staticmethod
    def create_param(name, label, param_type='text', **kwargs):
        """
        Helper function to create a parameter definition.
        
        Args:
            name (str): Parameter name (used as key in params dict)
            label (str): Display label for the UI
            param_type (str): Type of input - 'text', 'number', 'radio'
            **kwargs: Additional options:
                - placeholder (str): Placeholder text
                - min (int): Minimum value for number inputs
                - max (int): Maximum value for number inputs
                - required (bool): Whether the parameter is required
                - default: Default value
                - options (list): For radio type - list of dicts with 'value' and 'label'
        
        Returns:
            dict: Parameter definition dictionary
        
        Example:
            create_param('key_size', 'Key Size', 'radio', 
                         default=128,
                         options=[
                             {'value': 128, 'label': '128-bit'},
                             {'value': 256, 'label': '256-bit'}
                         ])
        """
        param = {
            'name': name,
            'label': label,
            'type': param_type
        }
        
        # Add all additional keyword arguments
        param.update(kwargs)
        
        return param
    
    def get_params(self):
        """
        Return parameter definitions for this technique.
        Used to auto-generate UI form fields.
        
        Returns:
            list: List of parameter dictionaries. Each dict should have:
                - name: parameter name
                - label: display label
                - type: 'text', 'number', 'radio'
                - options: (for radio) list of dicts with 'value' and 'label'
                - placeholder: (optional) placeholder text
                - min, max: (optional, for number)
                - required: (optional) boolean
        """
        return []
