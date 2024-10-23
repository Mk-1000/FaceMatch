from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from verification import compare_faces
import uuid  # Import UUID for unique folder names

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'  # Base directory where uploaded images will be saved
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_files():
    # Check if both files are in the request
    if 'documentImage' not in request.files or 'selfieImage' not in request.files:
        return jsonify({"error": "Both document and selfie images are required"}), 400

    document_file = request.files['documentImage']
    selfie_file = request.files['selfieImage']

    if not allowed_file(document_file.filename) or not allowed_file(selfie_file.filename):
        return jsonify({"error": "Only images with .png, .jpg, .jpeg extensions are allowed"}), 400

    # Create a unique folder for this verification session
    unique_folder = str(uuid.uuid4())  # Generate a unique folder name
    verification_folder = os.path.join(app.config['UPLOAD_FOLDER'], unique_folder)
    os.makedirs(verification_folder)  # Create the directory

    # Secure the filenames
    document_filename = secure_filename(document_file.filename)
    selfie_filename = secure_filename(selfie_file.filename)

    # Save the files to the unique folder
    document_path = os.path.join(verification_folder, document_filename)
    selfie_path = os.path.join(verification_folder, selfie_filename)

    document_file.save(document_path)
    selfie_file.save(selfie_path)

    # Generate a unique image_id for the current request
    image_id = str(uuid.uuid4())  # or any other unique identifier you want to use

    # Perform face verification
    try:
        is_match = compare_faces(document_path, selfie_path, image_id)  # Pass the image_id
        if is_match:
            return jsonify({"message": "Face verified successfully!"})
        else:
            return jsonify({"message": "Faces do not match."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
