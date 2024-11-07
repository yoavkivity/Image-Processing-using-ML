import os
import numpy as np
import cv2
from PIL import Image, ImageEnhance
from skimage import exposure
from image_process_and_prediction import files_operations

GLOBAL_WIDTH = 500

def get_image_path():
    """Retrieve the path of the image from a text file."""
    try:
        with open(files_operations.get_path("IMAGE_PATH"), 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        message = files_operations.get_path("IMAGE_PATH")
        print(f"File not found: {message}")
        return None


def convert_image_dpi(input_image_path, dpi=318):
    """Convert the DPI of an image to the specified value."""
    img = Image.open(input_image_path).convert("RGB")
    img.info['dpi'] = (dpi, dpi)
    file_name, file_extension = os.path.splitext(input_image_path)
    img.save(file_name + file_extension, dpi=(dpi, dpi))


def size_image(image):
    """Resize an image to a global width while maintaining aspect ratio."""
    aspect_ratio = image.shape[1] / image.shape[0]
    new_width = GLOBAL_WIDTH
    new_height = int(new_width / aspect_ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image, new_height, new_width


def convert_grayscale(image):
    """Convert an image to grayscale."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.uint8(gray_image)


def gamma_correction(gray_image, gamma):
    """Apply gamma correction to an image."""
    return exposure.adjust_gamma(gray_image, gamma=gamma)


def image_sharpening(gamma_corrected, alpha, beta, gamma_value):
    """Sharpen an image using Gaussian blur and addWeighted function."""
    blurred = cv2.GaussianBlur(gamma_corrected, (0, 0), 2)
    return cv2.addWeighted(gamma_corrected, alpha, blurred, beta, gamma_value)


def denoise(sharpened_image, filter_strength, template_window, search_window):
    """Denoise an image using fast non-local means denoising."""
    return cv2.fastNlMeansDenoising(sharpened_image, None, int(filter_strength), int(template_window),
                                    int(search_window))


def enhance_contrast(denoised_image, clip_limit):
    """Enhance the contrast of an image using adaptive histogram equalization."""
    contrast_enhanced = exposure.equalize_adapthist(denoised_image, clip_limit=clip_limit)
    return np.uint8(contrast_enhanced * 255)


def resize_final_image(new_height, new_width, contrast_enhanced):
    """Resize the final processed image to the specified dimensions."""
    return cv2.resize(contrast_enhanced, (new_width, new_height))


def process_image(alpha, beta, gamma, gamma_correction_value, filter_strength, template_window, search_window,
                  clip_limit, image_path):
    """Process the image through a pipeline of resizing, grayscale conversion, gamma correction, sharpening, denoising, and contrast enhancement."""
    convert_image_dpi(image_path)
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image file not found at path: {image_path}")

    image, new_height, new_width = size_image(image)
    image = convert_grayscale(image)
    image = gamma_correction(image, gamma_correction_value)
    image = image_sharpening(image, alpha, beta, gamma)
    image = denoise(image, filter_strength, template_window, search_window)
    image = enhance_contrast(image, clip_limit)
    image = resize_final_image(new_height, new_width, image)
    return image


def birch_effect(top_image):
    """Apply a birch-wood effect to the top image by blending it with a birch wood background."""
    top_image = Image.open(top_image)
    background = Image.open(files_operations.get_path("BACKGROUND")).resize(top_image.size, Image.LANCZOS).convert('RGB')
    top_image = top_image.convert('RGB')

    # Enhance contrast and adjust brightness of the top image
    top_image = ImageEnhance.Contrast(top_image).enhance(1.2)
    top_image = ImageEnhance.Brightness(top_image).enhance(0.8)

    # Blend the top image onto the birch-wood background
    engraved_image = Image.new('RGB', background.size, (255, 255, 255))
    engraved_image.paste(background, (0, 0))
    engraved_image = Image.blend(engraved_image, top_image, alpha=0.5)

    return engraved_image
