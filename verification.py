import face_recognition
from PIL import Image, ExifTags
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_image(image_path):
    """Loads an image from the given path."""
    try:
        image = face_recognition.load_image_file(image_path)
        logging.info(f"Successfully loaded image from: {image_path}")
        return image
    except FileNotFoundError:
        logging.error(f"File not found: {image_path}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error loading image {image_path}: {e}")
        raise

def correct_image_orientation(image_path):
    """Corrects the orientation of the image based on EXIF data."""
    try:
        with Image.open(image_path) as img:
            # Check for EXIF data
            exif = img._getexif()
            if exif is not None:
                orientation_key = 274  # Key for orientation in EXIF
                orientation = exif.get(orientation_key)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

            # Save corrected image temporarily
            temp_path = f"{image_path}_corrected.jpg"
            img.save(temp_path)
            return temp_path
    except Exception as e:
        logging.error(f"Error correcting image orientation: {e}")
        raise

def crop_face_and_save(image_path, image_id, image_type='selfie', output_dir=None):
    """Loads an image, corrects its orientation, crops the first detected face, and saves the cropped face image."""
    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(image_path)

    os.makedirs(output_dir, exist_ok=True)

    file_ext = os.path.splitext(image_path)[1]
    
    # Set the cropped file name based on image type
    if image_type == 'document':
        cropped_file_name = f"{image_id}_cropped_image{file_ext}"
    else:  # Default to selfie
        cropped_file_name = f"{image_id}_selfie_cropped_image{file_ext}"

    save_path = os.path.join(output_dir, cropped_file_name)

    try:
        # Correct image orientation
        corrected_image_path = correct_image_orientation(image_path)
        image = load_image(corrected_image_path)
        
        # Detect face locations
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            raise Exception(f"No face found in {corrected_image_path}")
        
        # Crop the first detected face
        top, right, bottom, left = face_locations[0]
        pil_image = Image.fromarray(image)
        cropped_image = pil_image.crop((left, top, right, bottom))
        
        # Save the cropped face image
        cropped_image.save(save_path)
        logging.info(f"Cropped face saved to: {save_path}")
        
        return save_path

    except Exception as e:
        logging.error(f"Error while processing {image_path}: {e}")
        raise

def get_face_encoding(image):
    """Gets the face encoding (128-dimensional feature vector) from the image."""
    try:
        encodings = face_recognition.face_encodings(image)
        if encodings:
            return encodings[0]
        logging.warning("No face encoding found.")
        return None
    except Exception as e:
        logging.error(f"Error getting face encoding: {e}")
        raise

def compare_faces(document_image_path: str, selfie_image_path: str, image_id: str, 
                  tolerance: float = 0.6, output_dir: str = None) -> (bool, float):
    """
    Compares the face in the cropped document image and selfie image.
    
    :param document_image_path: Path to the document image containing a face.
    :param selfie_image_path: Path to the selfie image containing a face.
    :param image_id: Unique identifier for the image (used in file naming).
    :param tolerance: The tolerance for face comparison (lower is stricter).
    :param output_dir: Directory to save cropped faces, defaults to image directories.
    :return: True if the faces match, False otherwise, and accuracy percentage.
    """
    try:
        # Crop faces and save them
        cropped_document_image_path = crop_face_and_save(document_image_path, image_id, image_type='document', output_dir=output_dir)
        cropped_selfie_image_path = crop_face_and_save(selfie_image_path, image_id, image_type='selfie', output_dir=output_dir)

        # Load the cropped face images
        cropped_document_image = load_image(cropped_document_image_path)
        cropped_selfie_image = load_image(cropped_selfie_image_path)

        # Get the face encodings for both images
        document_encoding = get_face_encoding(cropped_document_image)
        selfie_encoding = get_face_encoding(cropped_selfie_image)

        if document_encoding is None or selfie_encoding is None:
            raise ValueError("Face not detected in one or both cropped images.")

        # Compare the faces
        match_result = face_recognition.compare_faces([document_encoding], selfie_encoding, tolerance=tolerance)
        distances = face_recognition.face_distance([document_encoding], selfie_encoding)
        accuracy_percentage = (1 - distances[0]) * 100  # Convert distance to percentage

        logging.info(f"Faces match result = {match_result}")
        logging.info(f"Match accuracy: {accuracy_percentage:.2f}%")

        if accuracy_percentage < 50:  # Example threshold for logging
            logging.warning(f"Low accuracy detected for image ID {image_id}: {accuracy_percentage:.2f}%")

        return match_result[0], accuracy_percentage  # Return match result and accuracy

    except ValueError as ve:
        logging.error(f"ValueError comparing faces: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error comparing faces: {e}")
        raise


# Example of batch processing
def crop_faces_batch(image_paths, image_ids, output_dir=None):
    """
    Processes a batch of images, cropping faces and saving them.

    :param image_paths: List of image paths to process.
    :param image_ids: List of unique identifiers for the images.
    :param output_dir: Directory to save the cropped faces, defaults to image directories.
    :return: List of paths to cropped images.
    """
    cropped_images = []
    for image_path, image_id in zip(image_paths, image_ids):
        try:
            cropped_image = crop_face_and_save(image_path, image_id, output_dir=output_dir)
            cropped_images.append(cropped_image)
        except Exception as e:
            logging.error(f"Failed to process {image_path}: {e}")
    
    return cropped_images