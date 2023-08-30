import tkinter as tk
from photoslideshow.gui.photo_frame import PhotoFrame


class PhotoFullscreen(tk.Toplevel):
    """
    Window to show photos in fullscreen mode
    """
    def __init__(self, parent, photos):
        super().__init__(parent)
        self.parent = parent
        self.photos = photos
        self.title("photo-sliedshow-fullscreen")
        self.attributes('-fullscreen', True)  # testowo wylaczone
        self.is_running = True

        self.frm_photo = PhotoFrame(self)
        self.bind("<Escape>", self.handle_keypress_esc)

    def handle_keypress_esc(self, event):
        """Print the character associated to the key pressed"""
        self.destroy()