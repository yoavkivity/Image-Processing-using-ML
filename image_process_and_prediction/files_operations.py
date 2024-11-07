import os
import json
from PIL import Image
from image_process_and_prediction import image_editor


# Functions for file operations
def get_path(key):
    BASE_DIR = r"..\Camel Art"

    paths = {
        "RATIO_PATH": os.path.join(BASE_DIR, "reference files", "ratio_path.txt"),
        "IMAGE_PATH": os.path.join(BASE_DIR, "reference files", "path.txt"),
        "PREDICTION_JSON": os.path.join(BASE_DIR, "reference files", "good_prediction_parameters.json"),
        "EDIT_STUDIO_JSON": os.path.join(BASE_DIR, "reference files", "output.json"),
        "PROJECTS_DIR": os.path.join(BASE_DIR, "projects"),
        "SAVE_PATH": os.path.join(BASE_DIR, "Desktop", "studio.jpg"),
        "BACKGROUND": os.path.join(BASE_DIR, "reference files", "birch-plywood.jpg"),
        "DATA_WITH_INSIGHTS": os.path.join(BASE_DIR, "reference files", "data_with_insights.xlsx"),
        "EXCEL_PATH": os.path.join(BASE_DIR, "reference files", "data.xlsx"),
        "INDEX_FILE": os.path.join(BASE_DIR, "reference files", "train_set_index.txt"),
        "BIRCH_PATH": os.path.join(BASE_DIR, "reference files", "CURRENT_PROJECT_BIRCH"),
        "OUTPUT_JSON": os.path.join(BASE_DIR, "reference files", "output.json"),
        "SEND_IMAGE": os.path.join(BASE_DIR, "send_image"),
        "GRBL_PATH": r"C:\Program Files (x86)\LaserGRBL\LaserGRBL.exe",
        "EMPTY_SEND_IMAGE": os.path.join(BASE_DIR, "send_image"),
        "IMAGE_NAME": ''
    }
    if key in ['SEND_IMAGE', "IMAGE_NAME"]:
        path = os.path.join(paths.get('SEND_IMAGE', "Key not found"))
        filename = get_file_name(path)
        if key == 'SEND_IMAGE':
            return os.path.join(path, filename)
        return filename

    return paths.get(key, "Key not found")


def get_file_name(directory_path):
    files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            files.append(file)
    return files[0]


def read_file(path):
    """Reads content from a file."""
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None


def write_to_txt(number, file_path):
    """Writes a number to a text file."""
    try:
        with open(file_path, 'w') as file:
            file.write(str(number))
        print(f"Number {number} written to {file_path} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_from_txt(file_path):
    """Reads an integer from a text file."""
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    except:
        return -1


def ensure_dir(dir_path):
    """Ensures a directory exists, creating it if necessary."""
    os.makedirs(dir_path, exist_ok=True)


def empty_dir(directory_path):
    if not os.path.isdir(directory_path):
        print("Directory does not exist.")
        return
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"Skipped: {file_path} (not a file)")


# Functions for image operations
def save_image_by_path(output_dir):
    """Saves an image from the path specified in IMAGE_PATH to the given output directory."""
    try:
        image_path = get_path("IMAGE_PATH")
        base_name, name = get_filename_from_path(image_path)
        output_path = os.path.join(output_dir, base_name)

        img = Image.open(image_path)
        new_width = image_editor.GLOBAL_WIDTH
        new_height = int((new_width / img.width) * img.height)
        img = img.resize((new_width, new_height))

        ensure_dir(os.path.dirname(output_path))
        img.save(output_path)
        print(f"Image saved successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_image(image, dir_path, name):
    """Saves an image array as a JPEG in the specified directory."""
    try:
        pil_image = Image.fromarray(image)
    except:
        pil_image = image
    file_path = os.path.join(dir_path, f"{name}.jpg")
    pil_image.save(file_path)
    return file_path


def save_birch_image(engraved_image, birch_path):
    """Saves an engraved image to a specified path."""
    engraved_image.save(birch_path)


def get_filename_from_path(path):
    """Extracts the base filename and name (without extension) from a given path."""
    base_name = os.path.basename(path)
    name, _ = os.path.splitext(base_name)
    return base_name, name


def save_in_archive():
    """Organizes image files into archive folders."""
    image_path = get_path("IMAGE_NAME")
    _, name = get_filename_from_path(image_path)

    main_dir = os.path.join(get_path("PROJECTS_DIR"), name)
    edited_dir = os.path.join(main_dir, "edited")
    birch_dir = os.path.join(main_dir, "birch")

    ensure_dir(main_dir)
    ensure_dir(edited_dir)
    ensure_dir(birch_dir)

    return main_dir, birch_dir, edited_dir, name


# Functions for JSON operations

def read_json_data():
    """Reads image processing parameters from the EDIT_STUDIO_JSON file."""
    try:
        with open(get_path("EDIT_STUDIO_JSON"), 'r') as file:
            data = json.load(file)
        return (
            data.get('Sharpness Alpha'),
            data.get('Sharpness Beta'),
            data.get('Sharpness Gamma'),
            data.get('Label'),
            data.get('Gamma Correction'),
            data.get('Filter Strength'),
            data.get('Template Window'),
            data.get('Search Window'),
            data.get('Clip Limit')
        )
    except FileNotFoundError:
        message = get_path("EDIT_STUDIO_JSON")
        print(f"File not found: {message}")
        return None


def read_prediction_json_data():
    """Reads image prediction parameters from the PREDICTION_JSON file."""
    try:
        with open(get_path("PREDICTION_JSON"), 'r') as file:
            data = json.loads(file.read())
        return (
            data['Sharpness Alpha'],
            data['Sharpness Beta'],
            data['Sharpness Gamma'],
            data['Gamma Correction'],
            data['Filter Strength'],
            data['Template Window'],
            data['Search Window'],
            data['Clip Limit']
        )
    except json.JSONDecodeError:
        print("Invalid JSON format in the prediction file.")
        return None


def overwrite_json(alpha, beta, gamma, gamma_correction, filter_strength, template_window, search_window, clip_limit):
    """Overwrites the prediction JSON file with new values."""
    data = {
        "Sharpness Alpha": float(alpha),
        "Sharpness Beta": float(beta),
        "Sharpness Gamma": float(gamma),
        "Gamma Correction": float(gamma_correction),
        "Filter Strength": float(filter_strength),
        "Template Window": float(template_window),
        "Search Window": float(search_window),
        "Clip Limit": float(clip_limit)
    }
    with open(get_path("PREDICTION_JSON"), "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Prediction JSON file updated successfully.")
