# FaceMatch

FaceMatch is a Flask web application that verifies a person's identity by comparing their selfie with a document image. It uses the `face_recognition` library for facial recognition and verification.

## Features

- Upload a document image (e.g., ID, passport) and a selfie image.
- Verify if the face in the document matches the face in the selfie.
- Store uploaded images in a unique folder for each verification session.

## Requirements

- Python 3.x
- Flask
- face_recognition
- face_recognition_models
- Werkzeug

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Mk-1000/FaceMatch.git
   cd FaceMatch
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. Install the required packages:

   ```bash
   pip install --upgrade setuptools
   pip install Flask
   pip install face_recognition
   pip install git+https://github.com/ageitgey/face_recognition_models
   ```

## Usage

1. Run the Flask application:

   ```bash
   flask run
   ```

   or 

   ```bash
   python app.py
   ```

2. Send a POST request to `/upload` with the following form data:

   - `documentImage`: The document image file.
   - `selfieImage`: The selfie image file.

   You can use a tool like Postman or cURL for testing.

## Example cURL Command

```bash
curl -X POST http://127.0.0.1:5000/upload \
     -F 'documentImage=@/path/to/document_image.jpg' \
     -F 'selfieImage=@/path/to/selfie_image.jpg'
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [face_recognition](https://github.com/ageitgey/face_recognition) - For the facial recognition capabilities.
- [Flask](https://flask.palletsprojects.com/) - For the web framework.
```

### `.gitignore`

```
# Python cache files
__pycache__/
*.py[cod]

# Virtual environment
venv/

# Flask instance folder
instance/

# Compiled Python files
*.pyc

# Jupyter Notebook checkpoints
.ipynb_checkpoints

# Environment variables file
.env

# Log files
*.log

# IDE specific files
.vscode/
.idea/

# OS generated files
.DS_Store
Thumbs.db