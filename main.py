import sys
import techniques as techniques_pkg
from techniques.technique import Technique
from create_technique import create_technique
import pkgutil
import importlib
import inspect


def run_cipher():
    """Run the cipher encryption/decryption interface."""
    print()
    print("Choose a technique:")
    techniques = load_classes_from_package(techniques_pkg, Technique)
    
    # Display available techniques
    technique_list = [(name, cls) for name, cls in techniques.items() if name != 'Technique']
    for i, (name, _) in enumerate(technique_list, 1):
        print(f"    {i}. {name}")
    choice = input(f"Enter choice (1-{len(technique_list)}) [default 1]: ").strip()

    if choice == "":
        idx = 0
    else:
        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(technique_list)):
                print("Invalid choice, default is 1.")
                idx = 0
        except (ValueError, IndexError):
            print("Invalid choice, default is 1.")
            idx = 0

    technique_class = technique_list[idx][1]
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

def load_classes_from_package(package, base_class=None):
    classes = {}

    for finder, module_name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ != module.__name__:
                continue
            if base_class and not issubclass(obj, base_class):
                continue
            classes[name] = obj

    return classes

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
