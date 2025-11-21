# Security Techniques - Encryption & Decryption Tool

A modern web application for encryption and decryption using various cryptographic techniques including Caesar Cipher and AES encryption.

## Features

- **Modern UI**: Sleek sidebar layout with glassmorphism effects
- **Multiple Techniques**: Support for Caesar Cipher, AES encryption (128/192/256-bit)
- **Operations**: Encrypt, Decrypt, and Brute Force capabilities
- **Auto-discovery**: Automatically discovers and loads encryption techniques from the techniques package
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Styling**: Custom CSS with Inter font family and modern design patterns
- **Deployment**: Vercel

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Security\ Task
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment on Vercel

### Prerequisites

- Vercel CLI installed: `npm i -g vercel`
- Vercel account

### Deploy

1. Make sure you're on the production branch:
```bash
git checkout production
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy to Vercel:
```bash
vercel --prod
```

Or simply push to the production branch if you've set up Git integration with Vercel.

### Environment Variables

No environment variables are required for basic functionality.

## Project Structure

```
Security Task/
├── techniques/          # Encryption technique implementations
│   ├── __init__.py
│   ├── technique.py     # Base class
│   ├── caesar_cipher.py
│   └── aes_cipher.py
├── static/              # Static assets
│   ├── style.css
│   └── script.js
├── templates/           # HTML templates
│   └── index.html
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel configuration
└── .gitignore         # Git ignore rules
```

## Adding New Techniques

1. Create a new file in the `techniques/` directory
2. Inherit from the `Technique` base class
3. Implement the required methods
4. The application will auto-discover and load your technique

Example:
```python
from techniques.technique import Technique

class MyCustomCipher(Technique):
    def encrypt(self, plaintext):
        # Your encryption logic
        pass
    
    def decrypt(self, ciphertext):
        # Your decryption logic
        pass
```

## License

This project is for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
