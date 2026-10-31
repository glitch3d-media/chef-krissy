import customtkinter as ctk
import sys
import os

# Ensure we can find the 'core' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.data_manager import load_data, save_data
from desktop.photo_manager import PhotoManagerWindow# Add this line to the top of frames.py
from desktop.design_frame import DesignStudioFrame
from core.pdf_exporter import export_menu_pdf
from core.data_manager import backup_data

    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Dashboard View", font=("Helvetica", 24, "bold")).pack(pady=50)
        ctk.CTkLabel(self, text="Welcome to Chef Krissy Menu Studio.").pack()

class MenuInputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.data = load_data()
        
        # Header and Save button
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header_frame, text="Edit Menu", font=("Helvetica", 24, "bold")).pack(side="left")
        
        self.save_btn = ctk.CTkButton(header_frame, text="Save Changes", command=self.save_menu)
        self.save_btn.pack(side="right")
        
        self.status_lbl = ctk.CTkLabel(header_frame, text="", text_color="green")
        self.status_lbl.pack(side="right", padx=10)

        # Setup Days
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        # We use a Tabview to separate the days
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        self.entries = {} 

        for day in self.days:
            tab = self.tabview.add(day)
            self.build_day_ui(tab, day)

    def build_day_ui(self, parent_tab, day):
        scroll_frame = ctk.CTkScrollableFrame(parent_tab)
        scroll_frame.pack(fill="both", expand=True)
        
        self.entries[day] = {"breakfast": [], "lunch": []}
        day_data = self.data.get("schedule", {}).get(day, {"breakfast": [], "lunch": []})
        
        # --- Breakfast Section ---
        ctk.CTkLabel(scroll_frame, text="Breakfast", font=("Helvetica", 18, "bold")).pack(anchor="w", pady=(10, 5))
        self.build_meal_section(scroll_frame, day, "breakfast", day_data.get("breakfast", []))
        
        # --- Lunch Section ---
        ctk.CTkLabel(scroll_frame, text="Lunch", font=("Helvetica", 18, "bold")).pack(anchor="w", pady=(20, 5))
        self.build_meal_section(scroll_frame, day, "lunch", day_data.get("lunch", []))
        
    def build_meal_section(self, parent, day, meal_type, items):
        for item in items:
            self.add_item_row(day, meal_type, parent, item_name=item.get("name", ""), item_price=item.get("price", ""))
            
        # Add an "Add Item" button for this specific section
        ctk.CTkButton(
            parent, 
            text=f"+ Add {meal_type.capitalize()} Item", 
            width=150,
            fg_color="gray30", 
            command=lambda: self.add_item_row(day, meal_type, parent)
        ).pack(anchor="w", pady=(5, 15))

    def add_item_row(self, day, meal_type, parent_frame, item_name="", item_price=""):
        row = ctk.CTkFrame(parent_frame)
        row.pack(fill="x", pady=2)
        
        name_entry = ctk.CTkEntry(row, placeholder_text="Item Name")
        name_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        name_entry.insert(0, item_name)
        
        price_entry = ctk.CTkEntry(row, placeholder_text="$0.00", width=100)
        price_entry.pack(side="left", padx=(0, 10))
        price_entry.insert(0, item_price)
        
        # NEW: Photo button
        photo_btn = ctk.CTkButton(
            row, 
            text="Photo", 
            width=60, 
            fg_color="gray20",
            command=self.open_photo_manager
        )
        photo_btn.pack(side="left")
        
        self.entries[day][meal_type].append({"name": name_entry, "price": price_entry, "frame": row})
        # Auto-scroll to the bottom when adding a new row
        parent_frame._parent_canvas.yview_moveto(1.0)

    def open_photo_manager(self):
        # Opens the Photo Manager Popup
        PhotoManagerWindow(self.winfo_toplevel())

    def save_menu(self):
        self.data["schedule"] = {}
        for day in self.days:
            self.data["schedule"][day] = {"breakfast": [], "lunch": []}
            for meal_type in ["breakfast", "lunch"]:
                for entry in self.entries[day][meal_type]:
                    name = entry["name"].get().strip()
                    price = entry["price"].get().strip()
                    if name:
                        self.data["schedule"][day][meal_type].append({"name": name, "price": price})
        save_data(self.data)
        self.status_lbl.configure(text="Saved successfully!")
        self.after(3000, lambda: self.status_lbl.configure(text=""))

class DesignStudioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Design Studio View", font=("Helvetica", 24, "bold")).pack(pady=50)
        ctk.CTkLabel(self, text="Here you will customize fonts, backgrounds, and layout.").pack()

class ExportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.data = load_data()
        
        ctk.CTkLabel(self, text="Export Menu", font=("Helvetica", 24, "bold")).pack(pady=(50, 20))
        
        # Main Card
        card = ctk.CTkFrame(self, width=400, height=200)
        card.pack(pady=20)
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="Generate a PDF of your current menu.", font=("Helvetica", 14)).pack(pady=20)
        
        ctk.CTkButton(card, text="Save as PDF", font=("Helvetica", 16, "bold"), height=40, command=self.export_pdf).pack(pady=10)
        
        self.status_lbl = ctk.CTkLabel(self, text="", text_color="green")
        self.status_lbl.pack(pady=10)

    def export_pdf(self):
        import tkinter.filedialog as fd
        import os
        
        # Ask user where to save
        path = fd.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="Menu.pdf"
        )
        
        if path:
            try:
                # Generate the PDF using our core module
                export_menu_pdf(self.data, path)
                self.status_lbl.configure(text=f"Successfully saved to {os.path.basename(path)}!")
                self.after(3000, lambda: self.status_lbl.configure(text=""))
            except Exception as e:
                self.status_lbl.configure(text=f"Error: {str(e)}", text_color="red")


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.data = load_data()
        
        ctk.CTkLabel(self, text="Settings", font=("Helvetica", 24, "bold")).pack(pady=(20, 20))
        
        # Form frame
        form = ctk.CTkFrame(self, width=500)
        form.pack(pady=10, padx=20, fill="x")
        
        # Menu Title
        ctk.CTkLabel(form, text="Menu Title:", font=("Helvetica", 14)).pack(anchor="w", padx=20, pady=(15, 0))
        self.title_entry = ctk.CTkEntry(form, width=400)
        self.title_entry.insert(0, self.data["meta"].get("title", "Chef Krissy's Menu"))
        self.title_entry.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Business Name
        ctk.CTkLabel(form, text="Business Name:", font=("Helvetica", 14)).pack(anchor="w", padx=20, pady=(5, 0))
        self.name_entry = ctk.CTkEntry(form, width=400)
        self.name_entry.insert(0, self.data["meta"].get("business_name", ""))
        self.name_entry.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Contact Info
        ctk.CTkLabel(form, text="Contact Info (Phone/Website):", font=("Helvetica", 14)).pack(anchor="w", padx=20, pady=(5, 0))
        self.contact_entry = ctk.CTkEntry(form, width=400)
        self.contact_entry.insert(0, self.data["meta"].get("contact_info", ""))
        self.contact_entry.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        self.save_btn = ctk.CTkButton(btn_frame, text="Save Settings", command=self.save_settings)
        self.save_btn.pack(side="left", padx=10)
        
        self.backup_btn = ctk.CTkButton(btn_frame, text="Backup Data", fg_color="gray30", command=self.run_backup)
        self.backup_btn.pack(side="left", padx=10)
        
        self.status_lbl = ctk.CTkLabel(self, text="", text_color="green")
        self.status_lbl.pack()

    def save_settings(self):
        # Update data dictionary
        self.data["meta"]["title"] = self.title_entry.get().strip()
        self.data["meta"]["business_name"] = self.name_entry.get().strip()
        self.data["meta"]["contact_info"] = self.contact_entry.get().strip()
        
        # Save to JSON
        save_data(self.data)
        
        self.status_lbl.configure(text="Settings saved successfully!", text_color="green")
        self.after(3000, lambda: self.status_lbl.configure(text=""))
        
        # Note: To make the Dashboard/Design Studio update instantly, 
        # you would normally trigger a global event. For V1, they will update on next app launch.

    def run_backup(self):
        try:
            path = backup_data()
            self.status_lbl.configure(text=f"Backup created!", text_color="green")
        except Exception as e:
            self.status_lbl.configure(text=f"Backup failed: {e}", text_color="red")