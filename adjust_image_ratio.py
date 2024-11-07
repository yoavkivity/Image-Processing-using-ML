import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pillow_heif
from image_process_and_prediction import files_operations

pillow_heif.register_heif_opener()


class ImageCropper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Cropper")
        self.geometry("750x900")
        self.image_path = files_operations.get_path("SEND_IMAGE")
        self.image = None
        self.resized_image = None
        self.tk_image = None
        self.desired_width = 500
        self.aspect_ratio = 37 / 50
        self.desired_height = int(self.desired_width / self.aspect_ratio)

        self.frame_width = self.desired_width
        self.frame_height = self.desired_height

        self.canvas = tk.Canvas(self, width=1000, height=800, bg='white')
        self.canvas.pack(expand=True)

        self.rect = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.resize_data = {"x": 0, "y": 0, "item": None, "initial_width": 0, "initial_height": 0}

        # פונקציה לחיתוך תמונה
        self.crop_button = tk.Button(self, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()

        self.open_button = tk.Button(self, text="Open Image", command=self.open_image)
        self.open_button.pack()

        self.open_image(default=True)

        self.canvas.bind("<ButtonPress-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)
        self.canvas.bind("<ButtonPress-3>", self.on_resize_start)
        self.canvas.bind("<B3-Motion>", self.on_resize_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_resize_drop)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<Configure>", self.on_resize)
        self.bind("<KeyPress>", self.on_key_press)

    def open_image(self, default=False):
        if not default:
            self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.resized_image = self.image.resize(
                (self.desired_width, int(self.image.height * (self.desired_width / self.image.width))))
            self.tk_image = ImageTk.PhotoImage(self.resized_image)
            self.adjust_frame_orientation()
            self.update_canvas()

    def adjust_frame_orientation(self):
        """Adjust the frame orientation based on the image dimensions."""
        img_width, img_height = self.image.size

        if img_width > img_height:
            self.aspect_ratio = 50 / 37
        else:
            self.aspect_ratio = 37 / 50

        self.desired_height = int(self.desired_width / self.aspect_ratio)
        self.frame_width = self.desired_width
        self.frame_height = self.desired_height

    def update_canvas(self):
        if self.image:
            self.canvas.delete("all")
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_x = (canvas_width - self.tk_image.width()) // 2
            img_y = (canvas_height - self.tk_image.height()) // 2
            self.canvas.create_image(img_x, img_y, anchor='nw', image=self.tk_image)

            # מרכז את המסגרת האדומה
            self.start_x = (canvas_width - self.frame_width) // 2
            self.start_y = (canvas_height - self.frame_height) // 2

            end_x = self.start_x + self.frame_width
            end_y = self.start_y + self.frame_height
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline='red', width=2)
            button_x = canvas_width - 30
            button_y = canvas_height - 30
            self.crop_button.place(x=button_x, y=button_y / 2, anchor='se')

    def on_start(self, event):
        if self.rect and self.canvas.find_withtag(tk.CURRENT):
            self.drag_data["item"] = self.rect
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_drag(self, event):
        if self.drag_data["item"]:
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            self.canvas.move(self.drag_data["item"], delta_x, delta_y)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.start_x += delta_x
            self.start_y += delta_y

    def on_drop(self, event):
        self.drag_data["item"] = None

    def on_resize_start(self, event):
        if self.rect and self.canvas.find_withtag(tk.CURRENT):
            self.resize_data["item"] = self.rect
            self.resize_data["x"] = event.x
            self.resize_data["y"] = event.y
            self.resize_data["initial_width"] = self.frame_width
            self.resize_data["initial_height"] = self.frame_height

    def on_resize_drag(self, event):
        if self.resize_data["item"]:
            delta_x = event.x - self.resize_data["x"]
            delta_y = event.y - self.resize_data["y"]
            delta = max(delta_x, delta_y)

            if delta_x < 0 and delta_y < 0:
                delta = min(delta_x, delta_y)
            else:
                delta = max(delta_x, delta_y)

            new_width = self.resize_data["initial_width"] + delta
            new_height = int(new_width / self.aspect_ratio)

            if new_width > 0 and new_height > 0:
                self.frame_width = new_width
                self.frame_height = new_height

            self.update_canvas()

    def on_resize_drop(self, event):
        self.resize_data["item"] = None

    def on_key_press(self, event):
        if self.rect:
            delta_x = 0
            delta_y = 0
            if event.keysym == 'Left':
                delta_x = -1
            elif event.keysym == 'Right':
                delta_x = 1
            elif event.keysym == 'Up':
                delta_y = -1
            elif event.keysym == 'Down':
                delta_y = 1
            self.start_x += delta_x
            self.start_y += delta_y
            self.canvas.move(self.rect, delta_x, delta_y)

    def on_resize(self, event):
        self.update_canvas()

    def on_mouse_wheel(self, event):
        scale_factor_image = 1.01 if event.delta > 0 else 0.99
        scale_factor_frame = 0.99 if event.delta > 0 else 1.01

        self.desired_width = int(self.desired_width * scale_factor_image)
        self.frame_width = int(self.frame_width * scale_factor_frame)
        self.desired_height = int(self.desired_width / self.aspect_ratio)
        self.frame_height = int(self.frame_width / self.aspect_ratio)

        self.resized_image = self.image.resize(
            (self.desired_width, int(self.image.height * (self.desired_width / self.image.width))))
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.update_canvas()

    def crop_image(self):
        if self.image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_width = self.resized_image.width
            img_height = self.resized_image.height

            # calc cropping area
            start_x = int((self.start_x - (canvas_width - img_width) / 2) * (self.image.width / img_width))
            start_y = int((self.start_y - (canvas_height - img_height) / 2) * (self.image.height / img_height))
            end_x = start_x + int(self.frame_width * (self.image.width / img_width))
            end_y = start_y + int(self.frame_height * (self.image.height / img_height))
            box = (start_x, start_y, end_x, end_y)

            cropped_image = self.image.crop(box)
            pixels = cropped_image.load()
            for x in range(cropped_image.width):
                for y in range(cropped_image.height):
                    if pixels[x, y] == (0, 0, 0):  # black pixel
                        pixels[x, y] = (255, 255, 255)  # white pixel

            file_name, file_extension = os.path.splitext(self.image_path)
            file_extension = ".png"

            save_path = f"{file_name}_ratio{file_extension}"
            cropped_image.save(save_path)
            print(save_path)
            files_operations.write_to_txt(save_path, files_operations.get_path("IMAGE_PATH"))


if __name__ == "__main__":
    app = ImageCropper()
    app.mainloop()
