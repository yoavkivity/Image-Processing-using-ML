import cv2
import numpy as np
from PIL import Image
from collections import Counter
from skimage import feature, color, exposure
from skimage.measure import shannon_entropy
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.metrics import structural_similarity as ssim
import pandas as pd
from skimage.util import img_as_ubyte
from scipy.stats import entropy as scipy_entropy


# Helper functions to calculate each feature

def calculate_sharpness(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def calculate_contrast(image):
    return image.max() - image.min()


def calculate_brightness(image):
    return np.mean(image)


def calculate_average_color_intensity(image):
    return np.mean(image)


def calculate_color_std(image):
    return np.std(image)


def calculate_number_of_edges(image):
    edges = cv2.Canny(image, 100, 200)
    return np.sum(edges != 0)


def calculate_average_edge_length(image):
    edges = cv2.Canny(image, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return np.mean([cv2.arcLength(cnt, True) for cnt in contours])
    return 0


def calculate_edge_orientation(image, orientation='horizontal'):
    edges = cv2.Canny(image, 100, 200)
    if orientation == 'horizontal':
        sobel_edges = sobel(image, axis=0)
    else:
        sobel_edges = sobel(image, axis=1)
    return np.sum(sobel_edges > 0)


def calculate_entropy(image):
    return shannon_entropy(image)


def calculate_histogram_mean(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return np.mean(hist)


def calculate_histogram_std(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return np.std(hist)


def calculate_texture_features(image):
    gray_image = rgb2gray(image)
    gray_image = img_as_ubyte(gray_image)  # Convert to uint8
    lbp = feature.local_binary_pattern(gray_image, P=8, R=1, method='uniform')
    return lbp.mean()


def calculate_frequency_mean(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)  # Add small value to avoid log(0)
    return np.mean(magnitude_spectrum)


def calculate_frequency_std(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)  # Add small value to avoid log(0)
    return np.std(magnitude_spectrum)


def calculate_foreground_to_background_ratio(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    foreground = np.sum(thresh == 255)
    background = np.sum(thresh == 0)
    return foreground / (background + foreground)


def calculate_dominant_color(grayscale_image):
    pixels = grayscale_image.flatten()
    counter = Counter(pixels)
    dominant_color = counter.most_common(1)[0][0]
    return dominant_color


def calculate_gradient_magnitude(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)
    return np.mean(gradient_magnitude)


def calculate_gradient_orientation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    gradient_orientation = np.arctan2(sobely, sobelx)
    return np.mean(gradient_orientation)


def calculate_psnr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mse = np.mean((gray - gray.mean()) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))


def calculate_ssim(image):
    gray_image = rgb2gray(image)
    ssim_value, _ = ssim(gray_image, gray_image, data_range=gray_image.max() - gray_image.min(), full=True)
    return ssim_value


def calculate_clarity_score(image):
    return np.mean(image)


def calculate_smoothness(image):
    return np.std(image)


# Main function to process the image and calculate features

def process_image(image_path):
    image = cv2.imread(image_path)
    features = {
        'Serial': 0,  # Placeholder
        'File Name': image_path.split('/')[-1],
        'Label': "",  # Placeholder
        'sharpness_alpha': "",  # Placeholder
        'sharpness_beta': "",  # Placeholder
        'sharpness_gamma': "",  # Placeholder
        'gamma_correction': "",  # Placeholder
        'filter_strength': "",  # Placeholder
        'template_window': "",  # Placeholder
        'search_window': "",  # Placeholder
        'clip_limit': "",  # Placeholder
        'sharpness': calculate_sharpness(image),
        'contrast': calculate_contrast(image),
        'brightness': calculate_brightness(image),
        'average_color_intensity': calculate_average_color_intensity(image),
        'color_standard_deviation': calculate_color_std(image),
        'number_of_edges': calculate_number_of_edges(image),
        'average_edge_length': calculate_average_edge_length(image),
        'edge_orientation_horizontal': calculate_edge_orientation(image, 'horizontal'),
        'edge_orientation_vertical': calculate_edge_orientation(image, 'vertical'),
        'entropy': calculate_entropy(image),
        'histogram_mean': calculate_histogram_mean(image),
        'histogram_standard_deviation': calculate_histogram_std(image),
        'texture_features_lbp': calculate_texture_features(image),
        'frequency_mean': calculate_frequency_mean(image),
        'frequency_standard_deviation': calculate_frequency_std(image),
        'foreground_to_background_ratio': calculate_foreground_to_background_ratio(image),
        'dominant_color': calculate_dominant_color(image),
        'gradient_magnitude': calculate_gradient_magnitude(image),
        'gradient_orientation': calculate_gradient_orientation(image),
        'psnr': calculate_psnr(image),
        'ssim': calculate_ssim(image),
        'clarity_score': calculate_clarity_score(image),
        'smoothness': calculate_smoothness(image)
    }
    return features


def process_missing_data(image_path):
    image = cv2.imread(image_path)
    data = {
        'Sharpness': float(calculate_sharpness(image)),
        'Contrast': float(calculate_contrast(image)),
        'Brightness': float(calculate_brightness(image)),
        'Average Color Intensity': float(calculate_average_color_intensity(image)),
        'Color Standard Deviation': float(calculate_color_std(image)),
        'Number of Edges': float(calculate_number_of_edges(image)),
        'Average Edge Length': float(calculate_average_edge_length(image)),
        'Edge Orientation (Horizontal)': float(calculate_edge_orientation(image)),
        'Edge Orientation (Vertical)': float(calculate_edge_orientation(image)),
        'Entropy': float(calculate_entropy(image)),
        'Histogram Mean': float(calculate_histogram_mean(image)),
        'Histogram Standard Deviation': float(calculate_histogram_std(image)),
        'Texture Features (Local Binary Patterns)': float(calculate_texture_features(image)),
        'Frequency Mean': float(calculate_frequency_mean(image)),
        'Frequency Standard Deviation': float(calculate_frequency_std(image)),
        'Foreground to Background Ratio': float(calculate_foreground_to_background_ratio(image)),
        'Dominant Color': float(calculate_dominant_color(image)),
        'Gradient Magnitude': float(calculate_gradient_magnitude(image)),
        'Gradient Orientation': float(calculate_gradient_orientation(image)),
        'Peak Signal-to-Noise Ratio (PSNR)': float(calculate_psnr(image)),
        'Structural Similarity Index (SSIM)': float(calculate_ssim(image)),
        'Clarity Score': float(calculate_clarity_score(image)),
        'Smoothness': float(calculate_smoothness(image)),
    }

    features_df = pd.DataFrame([data])
    return features_df
