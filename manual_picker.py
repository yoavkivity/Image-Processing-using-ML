import os
import shutil
import subprocess
import time
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

from image_process_and_prediction import files_operations

GRBL_ENGRAVING_FILE = ""
ROOT = None
def change_last_folder_in_path(path, old_folder, new_folder):
    path_parts = path.split(os.sep)

    if path_parts[-2] == old_folder:
        path_parts[-2] = new_folder

    new_path = os.sep.join(path_parts)
    return new_path

def approve_image(image_path):
    global GRBL_ENGRAVING_FILE
    print(image_path)
    copy_birch_parent_directory(image_path)

    upload_to_grbl = change_last_folder_in_path(image_path, "birch", "edited")
    print(upload_to_grbl)
    GRBL_ENGRAVING_FILE = upload_to_grbl
    copy_file_to_parent_directory(GRBL_ENGRAVING_FILE)
    files_operations.empty_dir(files_operations.get_path("EMPTY_SEND_IMAGE"))
    ROOT.destroy()


def remove_image(image_path, images, frame, canvas):
    images.remove(image_path)
    refresh_images(frame, images, canvas)


def create_image_buttons(image_frame, image_path, images, frame, canvas):
    # כפתור אישור V
    btn_approve = Button(image_frame, text="✔", command=lambda: approve_image(image_path))
    btn_approve.pack(side=TOP, padx=5, pady=5)

    # כפתור הסרה X
    btn_remove = Button(image_frame, text="✖", command=lambda: remove_image(image_path, images, frame, canvas))
    btn_remove.pack(side=TOP, padx=5, pady=5)

def refresh_images(frame, images, canvas):
    for widget in frame.winfo_children():
        widget.destroy()
    row = 0
    col = 0
    for image_path in images:
        image_frame = Frame(frame)
        image_frame.grid(row=row, column=col, padx=10, pady=10)

        image = Image.open(image_path)
        image.thumbnail((700, 700))
        img = ImageTk.PhotoImage(image)

        image_label = Label(image_frame, image=img)
        image_label.image = img
        image_label.pack(side=LEFT)

        create_image_buttons(image_frame, image_path, images, frame, canvas)

        col += 1
        if col == 2:
            col = 0
            row += 1

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def load_images_from_folder(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

def on_mouse_wheel(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def create_image_viewer(folder_path):
    global ROOT
    root = Tk()
    ROOT = root
    root.title("Image Viewer")

    window_width = 1150
    window_height = 700 + 100

    root.geometry(f"{window_width}x{window_height}")
    canvas = Canvas(root)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    images = load_images_from_folder(folder_path)
    refresh_images(frame, images, canvas)
    canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))

    start = time.time()
    root.mainloop()
    end = time.time() + 5
    print("Total manual time: {}".format(end-start))
    open_program_with_file(files_operations.get_path("GRBL_PATH"), GRBL_ENGRAVING_FILE)

def open_program_with_file(program_path, file_path):
    if os.path.exists(program_path) and os.path.exists(file_path):
        subprocess.run([program_path, file_path])
    else:
        print("GRBL isn't found on computer")


def copy_file_to_parent_directory(file_path):
    if os.path.exists(file_path):
        parent_directory = os.path.dirname(os.path.dirname(file_path))
        new_file_path = os.path.join(parent_directory, os.path.basename(file_path))
        shutil.copy(file_path, new_file_path)
    else:
        print("Image file isn't found!")

def copy_birch_parent_directory(file_path):
    if os.path.exists(file_path):
        parent_directory = os.path.dirname(os.path.dirname(file_path))
        new_file_name = f"birch_{os.path.basename(file_path)}"
        new_file_path = os.path.join(parent_directory, new_file_name)
        shutil.copy(file_path, new_file_path)
    else:
        print("Image file isn't found!")



folder_path = files_operations.read_file(files_operations.get_path("BIRCH_PATH"))
create_image_viewer(folder_path)


