import sys
import os
import re


def to_snake_case(name):
    """Convert CamelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_technique(technique_name):
    """Create a new technique class file from the stub template."""
    
    if not technique_name:
        print("Error: Technique name cannot be empty.")
        return False
    
    if not technique_name[0].isupper():
        print("Error: Technique name must start with an uppercase letter (e.g., CaesarCipher).")
        return False
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stub_path = os.path.join(base_dir, 'stubs', 'technique.stub')
    techniques_dir = os.path.join(base_dir, 'techniques')
    
    filename = to_snake_case(technique_name) + '.py'
    output_path = os.path.join(techniques_dir, filename)
    
    if os.path.exists(output_path):
        print(f"technique {technique_name} already exists")
        return False
    
    try:
        with open(stub_path, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: Stub template not found at '{stub_path}'.")
        return False
    
    content = template.replace('{{TechniqueName}}', technique_name)
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    init_path = os.path.join(techniques_dir, '__init__.py')
    try:
        with open(init_path, 'r') as f:
            init_content = f.read().strip()
        import_line = f"from .{filename[:-3]} import {technique_name}"
        if import_line not in init_content:
            init_content += f"\n{import_line}\n"
            with open(init_path, 'w') as f:
                f.write(init_content)
            print(f"✓ Added import to techniques/__init__.py")
        else:
            print(f"✓ Import already exists in techniques/__init__.py")
    except FileNotFoundError:
        print(f"Warning: techniques/__init__.py not found. Manual addition required.")
    
    print()
    print(f"✓ Created new technique class: {technique_name}")
    print(f"✓ File location: techniques/{filename}")
    print()
    print("Next steps:")
    print(f"1. Edit 'techniques/{filename}' to implement the encryption logic")
    print("2. Update 'main.py' to include the new technique in the menu (manual step required)")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print()
        print("Usage: python3 create_technique.py <TechniqueName>")
        print()
        print("Example:")
        print("    python3 create_technique.py RSACipher")
        print()
        sys.exit(1)
    
    technique_name = sys.argv[1]
    
    if create_technique(technique_name):
        sys.exit(0)
    else:
        sys.exit(1)