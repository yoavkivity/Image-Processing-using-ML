import json
import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from image_process_and_prediction import image_editor, files_operations, update_dataset

COUNTER = 0


def get_image_path():
    try:
        with open(files_operations.get_path("IMAGE_PATH"), 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        message = files_operations.get_path("IMAGE_PATH")
        print(f"File not found: {message}")
        return None


def extract_values_from_json(data):
    sharpness_alpha = data.get('Sharpness Alpha')
    sharpness_beta = data.get('Sharpness Beta')
    sharpness_gamma = data.get('Sharpness Gamma')
    gamma_correction = data.get('Gamma Correction')
    filter_strength = data.get('Filter Strength')
    template_window = data.get('Template Window')
    search_window = data.get('Search Window')
    clip_limit = data.get('Clip Limit')
    label = data.get('Label')
    return sharpness_alpha, sharpness_beta, sharpness_gamma, gamma_correction, filter_strength, template_window, search_window, clip_limit, label


def read_json():
    filename = files_operations.get_path("OUTPUT_JSON")
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


class ImageEditor(tk.Tk):
    def __init__(self, IMAGE_DATA):
        super().__init__()
        self.title("Image Editor")
        self.geometry("900x750")

        # Initialize the variables
        self.sharpness_alpha = tk.DoubleVar()
        self.sharpness_beta = tk.DoubleVar()
        self.sharpness_gamma = tk.DoubleVar()
        self.gamma_correction = tk.DoubleVar()
        self.filter_strength = tk.DoubleVar()
        self.template_window = tk.DoubleVar()
        self.search_window = tk.DoubleVar()
        self.clip_limit = tk.DoubleVar()
        self.label = tk.StringVar()

        self.update_values(IMAGE_DATA)
        self.image_label = tk.Label(self)
        self.image_label.pack(side=tk.LEFT, expand=True)
        self.create_buttons()
        self.create_sliders()
        self.update_image()

    def update_values(self, IMAGE_DATA):
        sharpness_alpha, sharpness_beta, sharpness_gamma, gamma_correction, filter_strength, template_window, search_window, clip_limit, label = extract_values_from_json(
            IMAGE_DATA)
        self.sharpness_alpha.set(sharpness_alpha)
        self.sharpness_beta.set(sharpness_beta)
        self.sharpness_gamma.set(sharpness_gamma)
        self.gamma_correction.set(gamma_correction)
        self.filter_strength.set(filter_strength)
        self.template_window.set(template_window)
        self.search_window.set(search_window)
        self.clip_limit.set(clip_limit)
        self.label.set(label)

    def update_label(self, new_label):
        self.label.set(new_label)

    def create_sliders(self):
        frame = tk.Frame(self)
        frame.pack(side=tk.RIGHT, fill=tk.Y, padx=80)

        tk.Label(frame, text="Sharpen Alpha").pack(side=tk.TOP, pady=5)
        self.alpha_value_label = tk.Label(frame, text=f"{self.sharpness_alpha.get():.3f}")
        self.alpha_value_label.pack(side=tk.TOP)
        alpha_slider = ttk.Scale(frame, from_=0.1, to=10, orient=tk.HORIZONTAL, variable=self.sharpness_alpha,
                                 length=200)
        alpha_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.sharpness_alpha.trace("w", self.update_image)

        tk.Label(frame, text="Sharpen Beta").pack(side=tk.TOP, pady=5)
        self.beta_value_label = tk.Label(frame, text=f"{self.sharpness_beta.get():.3f}")
        self.beta_value_label.pack(side=tk.TOP)
        beta_slider = ttk.Scale(frame, from_=-10, to=10, orient=tk.HORIZONTAL, variable=self.sharpness_beta, length=200)
        beta_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.sharpness_beta.trace("w", self.update_image)

        tk.Label(frame, text="Sharpen Gamma").pack(side=tk.TOP, pady=5)
        self.gamma_value_label = tk.Label(frame, text=f"{self.sharpness_gamma.get():.3f}")
        self.gamma_value_label.pack(side=tk.TOP)
        gamma_slider = ttk.Scale(frame, from_=-20, to=80, orient=tk.HORIZONTAL, variable=self.sharpness_gamma,
                                 length=200)
        gamma_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.sharpness_gamma.trace("w", self.update_image)

        tk.Label(frame, text="Gamma Correction").pack(side=tk.TOP)
        self.gamma_correction_label = tk.Label(frame, text=f"{self.gamma_correction.get():.3f}")
        self.gamma_correction_label.pack(side=tk.TOP)
        gamma_correction_slider = ttk.Scale(frame, from_=0.5, to=1.5, orient=tk.HORIZONTAL,
                                            variable=self.gamma_correction,
                                            length=200)
        gamma_correction_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.gamma_correction.trace("w", self.update_image)

        tk.Label(frame, text="Filter Strength").pack(side=tk.TOP, pady=5)
        self.a_value_label = tk.Label(frame, text=f"{self.filter_strength.get():.3f}")
        self.a_value_label.pack(side=tk.TOP)
        a_slider = ttk.Scale(frame, from_=0.1, to=25, orient=tk.HORIZONTAL, variable=self.filter_strength,
                             length=200)
        a_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.filter_strength.trace("w", self.update_image)

        tk.Label(frame, text="Template Window").pack(side=tk.TOP, pady=5)
        self.b_value_label = tk.Label(frame, text=f"{self.template_window.get():.3f}")
        self.b_value_label.pack(side=tk.TOP)
        b_slider = ttk.Scale(frame, from_=0.1, to=10, orient=tk.HORIZONTAL, variable=self.template_window,
                             length=200)
        b_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.template_window.trace("w", self.update_image)

        tk.Label(frame, text="Search Window").pack(side=tk.TOP, pady=5)
        self.c_value_label = tk.Label(frame, text=f"{self.search_window.get():.3f}")
        self.c_value_label.pack(side=tk.TOP)
        c_slider = ttk.Scale(frame, from_=0.1, to=40, orient=tk.HORIZONTAL, variable=self.search_window,
                             length=200)
        c_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.search_window.trace("w", self.update_image)

        tk.Label(frame, text="Clip Limit").pack(side=tk.TOP, pady=5)
        self.d_value_label = tk.Label(frame, text=f"{self.clip_limit.get():.3f}")
        self.d_value_label.pack(side=tk.TOP)
        d_slider = ttk.Scale(frame, from_=0.001, to=0.020, orient=tk.HORIZONTAL, variable=self.clip_limit, length=200)
        d_slider.pack(side=tk.TOP, fill=tk.X, padx=5)
        self.clip_limit.trace("w", self.update_image)

    def create_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        print_values_button = tk.Button(button_frame, text="Save JSON", command=self.print_bar_values)
        print_values_button.pack(side=tk.TOP, padx=5, pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=(5, 30))
        add_to_excel = tk.Button(button_frame, text="Add to excel",
                                 command=update_dataset.write_current_json_to_excel)
        add_to_excel.pack(side=tk.TOP, padx=5, pady=5)

    def print_bar_values(self):
        image_data = {
            "Sharpness Alpha": self.sharpness_alpha.get(),
            "Sharpness Beta": self.sharpness_beta.get(),
            "Sharpness Gamma": self.sharpness_gamma.get(),
            "Gamma Correction": self.gamma_correction.get(),
            "Label": 5,  # Get the current label value
            "Filter Strength": self.filter_strength.get(),
            "Template Window": self.template_window.get(),
            "Search Window": self.search_window.get(),
            "Clip Limit": self.clip_limit.get()
        }

        with open(files_operations.get_path("JSON_PATH"), "w") as outfile:
            json.dump(image_data, outfile, indent=4)
        print("Values saved to output.json")
        print(image_data)

        main_dir, birch_dir, edited_dir, file_name = files_operations.save_in_archive()
        file_name = files_operations.get_path("IMAGE_NAME")
        files_operations.save_image_by_path(main_dir)
        image = image_editor.process_image(self.sharpness_alpha.get(), self.sharpness_beta.get(),
                                           self.sharpness_gamma.get(),
                                           self.gamma_correction.get(), self.filter_strength.get(),
                                           self.template_window.get(), self.search_window.get(), self.clip_limit.get(),
                                           get_image_path())

        edited_image = files_operations.save_image(image, main_dir, file_name)
        files_operations.save_birch_image(image_editor.birch_effect(edited_image),
                                          main_dir + "\\\\" + file_name + " _birch effect.jpg")

    def update_image(self, *args):
        image = image_editor.process_image(self.sharpness_alpha.get(), self.sharpness_beta.get(),
                                           self.sharpness_gamma.get(),
                                           self.gamma_correction.get(), self.filter_strength.get(),
                                           self.template_window.get(), self.search_window.get(), self.clip_limit.get(),
                                           get_image_path())
        self.display_image(image)
        self.alpha_value_label.config(text=f"{self.sharpness_alpha.get():.3f}")
        self.beta_value_label.config(text=f"{self.sharpness_beta.get():.3f}")
        self.gamma_value_label.config(text=f"{self.sharpness_gamma.get():.3f}")
        self.gamma_correction_label.config(text=f"{self.gamma_correction.get():.3f}")
        self.a_value_label.config(text=f"{self.filter_strength.get():.3f}")
        self.b_value_label.config(text=f"{self.template_window.get():.3f}")
        self.c_value_label.config(text=f"{self.search_window.get():.3f}")
        self.d_value_label.config(text=f"{self.clip_limit.get():.3f}")

    def display_image(self, image):
        # Convert the image to RGB format for displaying in Tkinter
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        original_width, original_height = image.size

        max_width = 600
        if original_width > max_width:
            new_width = max_width
            new_height = int((max_width / original_width) * original_height)
        else:
            new_width = original_width
            new_height = original_height

        image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo


if __name__ == "__main__":
    IMAGE_DATA = read_json()
    if IMAGE_DATA:
        app = ImageEditor(IMAGE_DATA)
        app.mainloop()
