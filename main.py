from techniques import CaesarCipher


if __name__ == "__main__":
    techniques = {
        '1': CaesarCipher,
    }
    technique = input("""
Choose a technique:
    1. Caesar Cipher 
Enter choice (1): """)
    technique_class = techniques.get(technique, CaesarCipher)
    technique_instance = technique_class()
    result = technique_instance.execute()

    print("Result:")
    if isinstance(result, list):
        for i, text in enumerate(result, 1):
            print(f"Option {i}: {text}")
    else:
        print(result)
