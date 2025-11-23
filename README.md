# Security Techniques - Encryption & Decryption Tool

A modern web application and CLI tool for encryption and decryption using various cryptographic techniques, including Caesar Cipher and AES encryption.

**Live Demo:** [https://security-task.tarboush.net/](https://security-task.tarboush.net/)

## Features

- **Modern UI**: Sleek sidebar layout with glassmorphism effects and responsive design.
- **Multiple Techniques**:
  - **Caesar Cipher**: A simple substitution cipher.
  - **AES Encryption**: Advanced Encryption Standard with 128, 192, and 256-bit key support in CBC mode.
- **Operations**:
  - **Encrypt**: Convert plaintext to ciphertext.
  - **Decrypt**: Convert ciphertext back to plaintext.
  - **Brute Force**: Attempt to break the cipher (available for Caesar Cipher).
- **Auto-discovery**: Automatically discovers and loads new encryption techniques added to the `techniques/` directory.
- **Dual Interface**:
  - **Web Interface**: User-friendly web app built with Flask.
  - **CLI**: Command-line interface for quick operations.

## Tech Stack

- **Backend**: Python 3.8+, Flask 3.0.0
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Deployment**: Vercel (Serverless)

## Project Structure

```
Security Task/
├── techniques/          # Encryption technique implementations
│   ├── __init__.py
│   ├── technique.py     # Base abstract class for all techniques
│   ├── caesar_cipher.py # Caesar Cipher implementation
│   └── aes_cipher.py    # AES Cipher implementation (CBC mode)
├── static/              # Static assets (CSS, JS, Images)
│   ├── style.css
│   └── script.js
├── templates/           # HTML templates for the web app
│   └── index.html
├── .github/workflows/   # GitHub Actions workflows
│   └── deploy.yml       # Vercel deployment workflow
├── app.py               # Main Flask web application
├── main.py              # Command-line interface (CLI) entry point
├── create_technique.py  # Helper script to scaffold new techniques
├── setup_cicd.sh        # Script to setup Vercel CI/CD
├── requirements.txt     # Python dependencies
└── vercel.json          # Vercel configuration
```

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd Security\ Task
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Web Application

1. **Run the Flask app:**
   ```bash
   python app.py
   ```
2. **Open your browser:**
   Navigate to `http://localhost:5000` to use the web interface.

#### Command Line Interface (CLI)

1. **Run the interactive CLI:**

   ```bash
   python main.py
   ```

   Follow the on-screen prompts to choose a technique and perform operations.

2. **Create a new technique:**
   ```bash
   python main.py --create <TechniqueName>
   ```
   This will generate a new technique file in the `techniques/` directory.

## Deployment on Vercel

This project is configured for easy deployment on Vercel using GitHub Actions.

### Prerequisites

- A Vercel account.
- Vercel CLI installed (`npm i -g vercel`).

### Manual Deployment

1. **Login to Vercel:**

   ```bash
   vercel login
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

### CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically deploys changes to Vercel when you push to the `main` branch.

1. **Setup Secrets:**
   You need to add the following secrets to your GitHub repository:

   - `VERCEL_TOKEN`: Your Vercel API token.
   - `VERCEL_ORG_ID`: Your Vercel Organization ID.
   - `VERCEL_PROJECT_ID`: Your Vercel Project ID.

   You can use the provided helper script to set this up (requires GitHub CLI `gh`):

   ```bash
   ./setup_cicd.sh
   ```

## Adding New Techniques

The system is designed to be extensible. To add a new encryption technique:

1. **Run the creation command:**

   ```bash
   python main.py --create MyNewCipher
   ```

   This creates `techniques/my_new_cipher.py`.

2. **Implement the logic:**
   Open the created file and implement the `encrypt`, `decrypt`, and `brute_force` methods in the generated class.

3. **Use it:**
   The application (both Web and CLI) will automatically detect and load your new technique next time you run it.

## License

This project is for educational purposes.
