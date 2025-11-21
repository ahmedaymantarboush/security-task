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
    
    # Dynamically load all technique classes from the techniques package
    techniques = load_classes_from_package(techniques_pkg, Technique)
    
    # Display available techniques to the user
    technique_list = [(name, cls) for name, cls in techniques.items() if name != 'Technique']
    for i, (name, _) in enumerate(technique_list, 1):
        print(f"    {i}. {name}")
    
    # Get user choice
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

    # Instantiate the selected technique class
    technique_class = technique_list[idx][1]
    technique_instance = technique_class()
    
    # Execute the technique (this usually triggers an interactive prompt in the technique's execute method)
    result = technique_instance.execute()

    print("Result:")
    if isinstance(result, list):
        # If result is a list (e.g., brute force results), print each item
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
    """
    Dynamically load classes from a package.
    
    Args:
        package: The package to search for classes.
        base_class: Optional base class to filter by.
        
    Returns:
        dict: A dictionary mapping class names to class objects.
    """
    classes = {}

    # Walk through all modules in the package
    for finder, module_name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)

        # Inspect each member of the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Ensure the class is defined in the module (not imported)
            if obj.__module__ != module.__name__:
                continue
            # Filter by base class if provided
            if base_class and not issubclass(obj, base_class):
                continue
            classes[name] = obj

    return classes

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Handle command line arguments
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
        elif sys.argv[1] == "--create" or sys.argv[1] == "-c":
            if len(sys.argv) < 3:
                print("Error: Please provide a technique name.")
                print("Usage: python main.py --create <TechniqueName>")
                sys.exit(1)
            technique_name = sys.argv[2]
            # Create a new technique file
            if create_technique(technique_name):
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print(f"Error: Unknown option '{sys.argv[1]}'")
            print("Use 'python main.py --help' for usage information.")
            sys.exit(1)
    else:
        # Run the interactive interface if no arguments provided
        run_cipher()
