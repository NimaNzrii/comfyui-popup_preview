import cv2
import tkinter as tk
from PIL import Image, ImageTk
import tempfile
import ctypes
from io import BytesIO
import win32clipboard
from tkinter import filedialog
import time


class ImageWindow:
    temp_image_path = tempfile.gettempdir().replace("\\", "/") + '/temp_image_preview.png'
    previous_image_hash = None
    k = 0

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.screen_width, self.screen_height = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)
        self.window_height = int(self.screen_height * 0.50)  # Initial width can be set accordingly

        # Create the Tkinter window
        self.window = tk.Tk()
        self.window.title("LIVE Show - by NimaNzri")
        self.window.geometry(f"+50+65")


        self.window.iconphoto(False, ImageTk.PhotoImage(Image.open("icon.ico")))


        self.window.bind("<Configure>", self.on_window_configure)

        self.create_canvas()
        self.create_buttons()

        # Window settings
        self.is_borderless = True
        self.window.attributes("-topmost", True)

        # Call refresh_image to initiate image display
        self.refresh_image()

        # Drag and move window binding
        self.window.bind("<ButtonPress-1>", self.start_move)
        self.window.bind("<B1-Motion>", self.on_motion)

        self.window.mainloop()

    def on_window_configure(self, event):
        self.window_width = event.width
        self.window_height = event.height

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, highlightthickness=1, highlightbackground="#282828")
        self.canvas.configure(bg="#282828") 
        self.canvas.bind("<Button-3>", self.show_right_click_menu)
        self.canvas.bind("<Button-1>", self.copy_image_to_clipboard)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def create_buttons(self):
        borderless_button = tk.Button(self.window, text="◼", command=self.borderless, width=2, height=1)
        borderless_button.place(x=0, y=0)
        
        self.right_click_menu = tk.Menu(self.window, tearoff=0)
        self.right_click_menu.add_command(label="📸 Open", command=self.open_image_with_browser) 
        self.right_click_menu.add_command(label="📄 Copy to ClipBoard", command=self.copy_image_to_clipboard)
        # self.right_click_menu.add_command(label="💾 Save Fast", command=self.contax_save_fast)
        self.right_click_menu.add_separator() 
        self.right_click_menu.add_command(label="💾 Save As", command=self.contax_save)




    # def contax_save_fast(self):
    #     file_path=os.path.join(os.path.expanduser('~'), 'Pictures', 'ComfyUi')
    #     if  os.path.exists(file_path):
    #         self.loaded_image.save( file_path, format="PNG")
    #     else:
    #         os.makedirs(file_path)
    #         self.loaded_image.save( file_path, format="PNG")
    #     print(f"Image saved: {file_path}")


    def open_image_with_browser(self):
        try:
            import webbrowser
            webbrowser.open(self.temp_image_path, new=2)
        except Exception as e:
            print("Failed to open image with browser:", e)
            self.Notif("Failed to open image with browser")

    def refresh_image(self):
        while True:
            try:
                # Load and convert the image
                new_image = cv2.imread(self.temp_image_path)
                background_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
                loaded_image = Image.open(self.temp_image_path).convert("RGB")
                self.loaded_image = loaded_image

                # Calculate the initial size based on the loaded image
                aspect_ratio = background_image.shape[1] / background_image.shape[0]
                self.window_width = int(self.window_height * aspect_ratio)

                # Resize the image and create PhotoImage
                background_image = cv2.resize(background_image, (self.window_width, self.window_height))
                loaded_image = Image.fromarray(background_image)
                photo = ImageTk.PhotoImage(image=loaded_image)

                self.image_on_canvas = self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, anchor=tk.CENTER, image=photo)
                self.photo = photo

                self.canvas.config(width=self.screen_height * 0.50 * aspect_ratio, height=self.screen_height * 0.50)
                break

            except Exception as e:
                print("Failed to load image:", e)
                time.sleep(0.05)

        if self.k < 3:
            self.k += 1
            self.borderless()

        self.window.after(100, self.refresh_image)


    def borderless(self):
        if self.is_borderless:
            self.window.overrideredirect(False)
            self.is_borderless = False
            self.window.attributes("-topmost", False)
            self.Notif("Borderless Disabled")
        else:
            self.window.attributes("-topmost", True)
            self.window.overrideredirect(True)
            self.is_borderless = True
            self.Notif("Borderless Enabled")

    def copy_image_to_clipboard(self, event=None):
        output = BytesIO()
        self.loaded_image.save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        self.Notif("Image copied to clipboard")

    def Notif(self, txt):
        existing_text = self.canvas.find_withtag(txt)
        if not existing_text:
            text_object = self.canvas.create_text(self.window_width / 2, self.window_height / 2, text=txt, fill="white", tags=txt)
            self.window.after(1500, lambda: self.canvas.delete(text_object))

    def show_right_click_menu(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def contax_save(self):
        file_path = filedialog.asksaveasfilename(initialfile='image.png', defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.loaded_image.save(file_path, format="PNG")
            print(f"Image saved: {file_path}")

# Create an instance of ImageWindow
window = ImageWindow()
