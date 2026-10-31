import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.filedialog as fd
import sys
import os

# Ensure we can find the 'core' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.image_manager import rotate_image, apply_mask, remove_background

class PhotoManagerWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Photo Manager")
        self.geometry("900x600")
        
        # Make window modal and keep on top
        self.transient(master)
        self.grab_set()

        self.current_image = None

        # Left side: Image display
        self.image_label = ctk.CTkLabel(self, text="No Image Loaded", fg_color="gray20", corner_radius=10)
        self.image_label.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Right side: Control panel
        control_panel = ctk.CTkFrame(self, width=200)
        control_panel.pack(side="right", fill="y", padx=10, pady=10)
        control_panel.pack_propagate(False)

        ctk.CTkLabel(control_panel, text="Tools", font=("Helvetica", 18, "bold")).pack(pady=15)
        
        ctk.CTkButton(control_panel, text="Load Image", command=self.load_image).pack(pady=5, fill="x")
        ctk.CTkButton(control_panel, text="Rotate 90°", command=self.rotate_90, fg_color="gray30").pack(pady=5, fill="x")
        ctk.CTkButton(control_panel, text="Mask: Circle", command=lambda: self.apply_mask("circle"), fg_color="gray30").pack(pady=5, fill="x")
        ctk.CTkButton(control_panel, text="Mask: Rounded", command=lambda: self.apply_mask("rounded"), fg_color="gray30").pack(pady=5, fill="x")
        ctk.CTkButton(control_panel, text="Mask: Rectangle", command=lambda: self.apply_mask("rectangle"), fg_color="gray30").pack(pady=5, fill="x")
        ctk.CTkButton(control_panel, text="Remove Background", command=self.remove_bg, fg_color="gray30").pack(pady=5, fill="x")
        
        # Spacer
        ctk.CTkLabel(control_panel, text="").pack(expand=True)
        
        ctk.CTkButton(control_panel, text="Save & Close", command=self.save_close, fg_color="green", hover_color="darkgreen").pack(pady=15, fill="x")

    def load_image(self):
        path = fd.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            self.current_image = Image.open(path)
            self.update_image_label()

    def rotate_90(self):
        if self.current_image:
            self.current_image = rotate_image(self.current_image)
            self.update_image_label()

    def apply_mask(self, mask_type):
        if self.current_image:
            self.current_image = apply_mask(self.current_image, mask_type)
            self.update_image_label()

    def remove_bg(self):
        if self.current_image:
            # Defaulting to white background removal
            self.current_image = remove_background(self.current_image, (255, 255, 255), 50)
            self.update_image_label()

    def save_close(self):
        if self.current_image:
            path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if path:
                self.current_image.save(path)
                self.destroy()

    def update_image_label(self):
        if self.current_image:
            # Resize image to fit the label (max 600x600) for preview
            preview = self.current_image.copy()
            preview.thumbnail((600, 600), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(preview)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo # Keep reference to prevent garbage collection