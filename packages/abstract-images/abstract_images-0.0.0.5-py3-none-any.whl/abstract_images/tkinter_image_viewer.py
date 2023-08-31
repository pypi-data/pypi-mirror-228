import os
import tkinter as tk
from tkinter import Button, Label, filedialog
from PIL import Image, ImageTk

class ImageBrowser:
    """
    A simple image browser to navigate through images in a directory using a GUI.

    Attributes:
        root (tk.Tk): The main window for the GUI.
        images (list): List of image paths.
        index (int): Current index of the image being viewed.
        img_label (tk.Label): Label to display the image.
    """
    def __init__(self, root, images):
        """
        Initialize the ImageBrowser with root window and images.

        Parameters:
            root (tk.Tk): The main window for the GUI.
            images (list): List of image paths.
        """
        self.root = root
        self.images = images
        self.index = 0
        self.img_label = Label(root)
        self.img_label.pack(pady=20)

        prev_button = Button(root, text="Previous", command=self.prev_image)
        prev_button.pack(side="left", padx=10)

        next_button = Button(root, text="Next", command=self.next_image)
        next_button.pack(side="right", padx=10)

        self.show_image()

    def prev_image(self):
        """Displays the previous image in the list."""
        self.index -= 1
        if self.index < 0:
            self.index = len(self.images) - 1
        self.show_image()

    def next_image(self):
        """Displays the next image in the list."""
        self.index += 1
        if self.index == len(self.images):
            self.index = 0
        self.show_image()

    def show_image(self):
        """Displays the current image and resizes it to fit the window."""
        image_path = self.images[self.index]
        image = Image.open(image_path)
        image = resize_image(image, 600)  # Resize image to fit window
        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo
        self.root.title(f"Viewing {os.path.basename(image_path)}")

def resize_image(image, base_width):
    """
    Resizes an image while maintaining its aspect ratio.

    Parameters:
        image (PIL.Image): The image to resize.
        base_width (int): The desired width for the resized image.

    Returns:
        PIL.Image: The resized image.
    """
    w_percent = base_width / float(image.size[0])
    h_size = int(float(image.size[1]) * float(w_percent))
    return image.resize((base_width, h_size), Image.LANCZOS)

def find_images(directory, extensions=("jpg", "jpeg", "png", "gif")):
    """
    Yields image paths from a directory that match the given extensions.

    Parameters:
        directory (str): Path to the directory.
        extensions (tuple): Acceptable image extensions.

    Yields:
        str: Image path.
    """
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                yield os.path.join(dirpath, filename)

def main():
    """Main function to run the image browser."""
    dir_path = filedialog.askdirectory(title="Select Directory")
    if not dir_path:
        return

    images = list(find_images(dir_path))
    if not images:
        print("No images found in the selected directory!")
        return

    root = tk.Tk()
    root.geometry('620x650')  # Set static window size (includes some buffer for buttons and padding)
    app = ImageBrowser(root, images)
    root.mainloop()

if __name__ == "__main__":
    main()
