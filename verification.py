import face_recognition

def load_image(image_path):
    """Loads an image from the given path."""
    image = face_recognition.load_image_file(image_path)
    return image

def get_face_encoding(image):
    """Gets face encoding (128-dimensional feature vector) from the image."""
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        return encodings[0]
    
    print("No face detected.")
    return None


def compare_faces(document_image_path, selfie_image_path):
    """Compares the face in document and selfie images and returns a similarity score."""
    # Load both images
    document_image = load_image(document_image_path)
    selfie_image = load_image(selfie_image_path)

    # Get the face encodings
    document_encoding = get_face_encoding(document_image)
    selfie_encoding = get_face_encoding(selfie_image)

    if document_encoding is None or selfie_encoding is None:
        raise Exception("No face detected in one or both images.")

    # Compare faces and return True if they match
    match_result = face_recognition.compare_faces([document_encoding], selfie_encoding)
    return match_result[0]  # Returns True if the faces match, False otherwise
