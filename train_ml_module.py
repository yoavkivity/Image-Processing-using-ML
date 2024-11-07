import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import random
from image_process_and_prediction import image_editor, files_operations, update_dataset


IMAGES_AMOUNT = 2
def generate_alpha_beta_gamma():
    alpha = random.uniform(3, 8)
    beta_min = -alpha + 0.5
    beta_max = -alpha + 1.7
    beta = random.uniform(beta_min, beta_max)
    gamma = random.uniform(0, 20)
    return alpha, beta, gamma


def print_data(event, alpha, beta, gamma, filter_strength, template_window, search_window, clip_limit,
               gamma_correction):
    data = {
        'Sharpness Alpha': alpha,
        'Sharpness Beta': beta,
        'Sharpness Gamma': gamma,
        'Gamma Correction': gamma_correction,
        'Label': event,
        'Filter Strength': filter_strength,
        'Template Window': template_window,
        'Search Window': search_window,
        'Clip Limit': clip_limit
    }
    json_str = json.dumps(data)
    print(json_str)
    with open(r"C:\Users\User\PycharmProjects\pythonProject\Camel Art\reference files\output.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Values saved to output.json")


def on_image_click(event, alpha, beta, gamma, filter_strength, template_window, search_window, clip_limit,
                   gamma_correction):
    # Save the prepared image
    global click_count
    click_count += 1
    data = {
        'Sharpness Alpha': alpha,
        'Sharpness Beta': beta,
        'Sharpness Gamma': gamma,
        'Gamma Correction': gamma_correction,
        'Label': event,
        'Filter Strength': filter_strength,
        'Template Window': template_window,
        'Search Window': search_window,
        'Clip Limit': clip_limit
    }
    json_str = "'" + json.dumps(data) + "'"
    print(json_str)
    with open(files_operations.get_path("OUTPUT_JSON"), "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Values saved to output.json")
    # edit_studio.run_studio(json_str)
    update_dataset.write_current_json_to_excel()

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))


# Function to handle mouse scroll
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Update the scroll region to include the whole image frame
def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def generate_blur():
    filter_strength = 7
    window_template = 3
    search_window = 20
    clip_limit = random.uniform(0.001,0.012)
    return filter_strength, window_template, search_window, clip_limit


root = tk.Tk()
root.title("Sharpness Combinations")

window_width = 1050
window_height = 780

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2) - 50
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

INDEX = files_operations.read_from_txt(files_operations.get_path("INDEX_FILE"))
click_count = 0  # Initialize the click counter

# Create a frame to hold the canvas and scrollbars
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas widget with a vertical scrollbar
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a vertical scrollbar linked to the canvas
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.config(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", _on_mousewheel)
frame.bind("<Configure>", configure_scroll_region)

# Create another frame inside the canvas to hold the images
image_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=image_frame, anchor=tk.NW)
image_frame.bind('<Configure>', on_configure)
images = []


def create_images():
    for i in range(IMAGES_AMOUNT):
        Alpha, Beta, Gamma = generate_alpha_beta_gamma()
        filter_strength, template_window, search_window, clip_limit = generate_blur()
        # gamma_correction = 1.2
        gamma_correction = random.uniform(0.6, 1.18)

        image = image_editor.process_image(Alpha, Beta, Gamma, gamma_correction, filter_strength, template_window, search_window,
                                     clip_limit, files_operations.get_path("IMAGE_PATH"))
        images.append(image)

        row, col = divmod(i, 2)
        alpha, beta, gamma = generate_alpha_beta_gamma()
        prepared_image = image
        prepared_image_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(prepared_image, cv2.COLOR_BGR2RGB)))

        # Place "Bad" button
        bad = ttk.Label(image_frame, text="Very Bad", relief="solid", borderwidth=1, background="#ff9999", padding=10)
        bad_row = 2 * row
        bad_col = col * 4
        bad.grid(row=bad_row, column=bad_col, padx=5, pady=5)

        # Place "Good Soft" button
        good_soft = ttk.Label(image_frame, text="Bad", relief="solid", borderwidth=1, background="#ff9999",
                              padding=10)
        good_soft_row = 2 * row
        good_soft_col = col * 4 + 1
        good_soft.grid(row=good_soft_row, column=good_soft_col, padx=5, pady=5)

        # Place "Good Mid" button
        good_mid = ttk.Label(image_frame, text="Good", relief="solid", borderwidth=1, background="#99ff99", padding=10)
        good_mid_row = 2 * row
        good_mid_col = col * 4 + 2
        good_mid.grid(row=good_mid_row, column=good_mid_col, padx=5, pady=5)

        # Place "Good Hard" button
        good_hard = ttk.Label(image_frame, text="Very Good", relief="solid", borderwidth=1, background="#99ff99",
                              padding=10)
        good_hard_row = 2 * row
        good_hard_col = col * 4 + 3
        good_hard.grid(row=good_hard_row, column=good_hard_col, padx=5, pady=5)

        # Place image below the buttons
        label = ttk.Label(image_frame, text=f"Image {i + 1}", image=prepared_image_tk, relief="solid", borderwidth=1,
                          padding=5)
        label.grid(row=2 * row + 1, column=col * 4, columnspan=4, padx=5, pady=(0, 50))
        label.image = prepared_image_tk

        filter_strength, template_window, search_window, clip_limit

        # Bind events to buttons
        bad.bind("<Button-1>",
                 lambda e, alpha=Alpha, beta=Beta, gamma=Gamma, a=filter_strength, b=template_window, c=search_window,
                        d=clip_limit,
                        index=INDEX + click_count: on_image_click(1, alpha,
                                                                  beta, gamma, a, b, c, d, gamma_correction))
        good_soft.bind("<Button-1>",
                       lambda e, alpha=Alpha, beta=Beta, gamma=Gamma, a=filter_strength, b=template_window, c=search_window,
                              d=clip_limit,
                              index=INDEX + click_count: on_image_click(2,
                                                                        alpha,
                                                                        beta,
                                                                        gamma, a, b, c, d, gamma_correction))
        good_mid.bind("<Button-1>",
                      lambda e, alpha=Alpha, beta=Beta, gamma=Gamma, a=filter_strength, b=template_window, c=search_window,
                             d=clip_limit,
                             index=INDEX + click_count: on_image_click(3,
                                                                       alpha,
                                                                       beta, gamma, a, b, c, d, gamma_correction))
        good_hard.bind("<Button-1>",
                       lambda e, alpha=Alpha, beta=Beta, gamma=Gamma, a=filter_strength, b=template_window, c=search_window,
                              d=clip_limit,
                              index=INDEX + click_count: on_image_click(4,
                                                                        alpha, beta,
                                                                        gamma, a, b, c, d, gamma_correction))
        label.bind("<Button-1>",
                   lambda e, alpha=Alpha, beta=Beta, gamma=Gamma, a=filter_strength, b=template_window, c=search_window,
                          d=clip_limit: print_data(f"Image {click_count + 1}",
                                                   alpha, beta, gamma, a, b,
                                                   c, d, gamma_correction))


create_images()
root.mainloop()

update_dataset.style_excel(files_operations.get_path("EXCEL_PATH"),INDEX + click_count)
print(str(click_count) + " new images trained.")

