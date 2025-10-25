import sys
from techniques import CaesarCipher
from create_technique import create_technique


def run_cipher():
    """Run the cipher encryption/decryption interface."""
    techniques = {
        '1': CaesarCipher,
    }
    print()
    print("Choose a technique:")
    print("    1. Caesar Cipher")
    technique = input("Enter choice (1): ")
    technique_class = techniques.get(technique, CaesarCipher)
    technique_instance = technique_class()
    result = technique_instance.execute()

    print("Result:")
    if isinstance(result, list):
        for i, text in enumerate(result, 1):
            print(f"Option {i}: {text}")
    else:
        print(result)


def show_help():
    """Display help information."""
    print()
    print("Security Task - Encryption Techniques Tool")
    print()
    print("Usage:")
    print("    python main.py                    Run the encryption/decryption interface")
    print("    python main.py --create <Name>    Create a new technique class")
    print("    python main.py --help             Show this help message")
    print()
    print("Examples:")
    print("    python main.py --create RSACipher")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
        elif sys.argv[1] == "--create" or sys.argv[1] == "-c":
            if len(sys.argv) < 3:
                print("Error: Please provide a technique name.")
                print("Usage: python main.py --create <TechniqueName>")
                sys.exit(1)
            technique_name = sys.argv[2]
            if create_technique(technique_name):
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print(f"Error: Unknown option '{sys.argv[1]}'")
            print("Use 'python main.py --help' for usage information.")
            sys.exit(1)
    else:
        run_cipher()
