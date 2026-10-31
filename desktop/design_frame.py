import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as fd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.data_manager import load_data, save_data

class DesignStudioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data = load_data()
        
        # Canvas state
        self.bg_image_pil = None
        self.bg_image_tk = None
        self.bg_opacity = self.data["meta"].get("bg_opacity", 100) / 100.0
        
        # Track draggable items
        self.items = {}
        self.selected_item = None
        
        # Split layout: Left (Tools), Right (Canvas)
        self.tools_panel = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.tools_panel.pack(side="left", fill="y")
        self.tools_panel.pack_propagate(False)
        
        self.canvas_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="gray15")
        self.canvas_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.build_tools_panel()
        self.build_canvas()

    def build_tools_panel(self):
        ctk.CTkLabel(self.tools_panel, text="Design Studio", font=("Helvetica", 18, "bold")).pack(pady=15)
        
        # Background Section
        ctk.CTkLabel(self.tools_panel, text="Background", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        ctk.CTkButton(self.tools_panel, text="Upload Image", command=self.upload_bg).pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(self.tools_panel, text="Opacity").pack(anchor="w", padx=10, pady=(5, 0))
        self.opacity_slider = ctk.CTkSlider(self.tools_panel, from_=0, to=1, command=self.change_opacity)
        self.opacity_slider.set(self.bg_opacity)
        self.opacity_slider.pack(padx=10, pady=5, fill="x")
        
        # Typography Section
        ctk.CTkLabel(self.tools_panel, text="Typography (Select text)", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        ctk.CTkLabel(self.tools_panel, text="Font Size").pack(anchor="w", padx=10)
        self.size_slider = ctk.CTkSlider(self.tools_panel, from_=8, to=72, command=self.change_size)
        self.size_slider.set(24)
        self.size_slider.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(self.tools_panel, text="Text Color (Hex)").pack(anchor="w", padx=10)
        self.color_entry = ctk.CTkEntry(self.tools_panel, placeholder_text="#FFFFFF")
        self.color_entry.insert(0, "#FFFFFF")
        self.color_entry.pack(padx=10, pady=5, fill="x")
        self.color_entry.bind("<Return>", lambda e: self.change_color())
        
        self.bold_var = tk.BooleanVar()
        self.bold_cb = ctk.CTkCheckBox(self.tools_panel, text="Bold", variable=self.bold_var, command=self.change_weight)
        self.bold_cb.pack(anchor="w", padx=10, pady=5)
        
        # Save Button
        ctk.CTkLabel(self.tools_panel, text="").pack(expand=True)
        ctk.CTkButton(self.tools_panel, text="Save Design", fg_color="green", command=self.save_design).pack(padx=10, pady=15, fill="x")
        
    def build_canvas(self):
        # Using a standard Tkinter Canvas for complex drag-and-drop
        self.canvas = tk.Canvas(self.canvas_frame, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        
        # Draw initial texts
        self.refresh_canvas()

    def refresh_canvas(self):
        self.canvas.delete("all")
        self.items = {}
        
        # Draw Background Image if exists
        if self.bg_image_pil:
            # Resize image to fit canvas roughly
            cw = self.canvas.winfo_width() or 800
            ch = self.canvas.winfo_height() or 600
            bg_resized = self.bg_image_pil.copy()
            bg_resized.thumbnail((cw, ch), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(bg_resized)
            self.canvas.create_image(cw//2, ch//2, image=self.bg_image_tk, anchor="center")
            
        # Draw draggable texts based on saved positions
        positions = self.data["meta"].get("design", {}).get("element_positions", {})
        
        default_positions = {
            "title": (400, 100),
            "business_name": (400, 150),
            "Monday": (150, 250),
            "Tuesday": (400, 250),
            "Wednesday": (650, 250)
        }
        
        for key, default_pos in default_positions.items():
            pos = positions.get(key, default_pos)
            text_val = "MENU" if key == "title" else key.replace("_", " ").title()
            if key == "business_name":
                text_val = self.data["meta"].get("business_name", "Your Business")
                
            item_id = self.canvas.create_text(
                pos[0], pos[1], 
                text=text_val, 
                fill=self.color_entry.get() or "#FFFFFF", 
                font=("Helvetica", int(self.size_slider.get()), "bold" if self.bold_var.get() else "normal"),
                tags=key
            )
            self.items[key] = item_id

    def on_button_press(self, event):
        # Find item under mouse
        item = self.canvas.find_withtag("current")
        if item:
            self.selected_item = item[0]
            # Update sliders to match selected item's properties (optional for V1, but good UX)
            self.canvas.tag_raise(self.selected_item)

    def on_move_press(self, event):
        if self.selected_item:
            # Move item to new mouse coordinates
            self.canvas.coords(self.selected_item, event.x, event.y)

    def change_opacity(self, value):
        self.bg_opacity = float(value)
        # Note: True opacity blending requires reconstructing the PIL image. 
        # For V1, we will just redraw.
        self.refresh_canvas()

    def upload_bg(self):
        path = fd.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            self.bg_image_pil = Image.open(path)
            # Auto-upscale to 300 DPI as per Master Prompt rules
            self.refresh_canvas()

    def change_size(self, value):
        if self.selected_item:
            current_font = self.canvas.itemcget(self.selected_item, "font")
            # Parse current font and rebuild (basic implementation)
            self.refresh_canvas() # Simplification for V1

    def change_color(self):
        if self.selected_item:
            self.canvas.itemconfig(self.selected_item, fill=self.color_entry.get())

    def change_weight(self):
        if self.selected_item:
            font_tuple = ("Helvetica", int(self.size_slider.get()), "bold" if self.bold_var.get() else "normal")
            self.canvas.itemconfig(self.selected_item, font=font_tuple)

    def save_design(self):
        # 1. Save element positions
        positions = {}
        for key, item_id in self.items.items():
            coords = self.canvas.coords(item_id)
            if coords:
                positions[key] = coords
                
        # Ensure meta and design dictionaries exist
        if "meta" not in self.data: self.data["meta"] = {}
        if "design" not in self.data["meta"]: self.data["meta"]["design"] = {}
        
        self.data["meta"]["design"]["element_positions"] = positions
        self.data["meta"]["design"]["bg_opacity"] = int(self.bg_opacity * 100)
        
        # 2. Save to file
        save_data(self.data)
        print("Design saved to JSON.")