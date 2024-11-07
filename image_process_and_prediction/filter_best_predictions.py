import cv2
from PIL import Image
import image_editor, files_operations

COUNTER = 0

def run(sharpness_alpha, sharpness_beta, sharpness_gamma, gamma_correction, filter_strength, template_window, search_window, clip_limit):
    global COUNTER
    image = image_editor.process_image(sharpness_alpha, sharpness_beta, sharpness_gamma, gamma_correction,
                                 filter_strength, template_window, search_window,
                                 clip_limit, files_operations.get_path("IMAGE_PATH"))

    # Convert to RGB and save
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    edited_image_path = r"C:\Users\User\Desktop\d\edited_image_{}.jpg".format(COUNTER)
    image.save(edited_image_path)
    print(f"Image saved to {edited_image_path}")
    COUNTER += 1
