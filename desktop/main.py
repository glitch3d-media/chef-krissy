import sys
import os
import customtkinter as ctk

# Ensure Python can find the 'desktop' folder when running the script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frames import (
    DashboardFrame,
    MenuInputFrame,
    DesignStudioFrame,
    ExportFrame,
    SettingsFrame,
)

# Set global appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chef Krissy Menu Studio")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # We start with the login screen
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)

    def on_login_success(self):
        # Destroy the login screen
        self.login_frame.destroy()
        
        # Build the main layout
        self.build_main_layout()

    def build_main_layout(self):
        # 1. Create Sidebar on the left
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Prevent shrinking

        # Sidebar Title
        ctk.CTkLabel(
            self.sidebar, 
            text="Chef Krissy\nStudio", 
            font=("Helvetica", 20, "bold")
        ).pack(pady=30)

        # Sidebar Buttons
        btn_style = {"fill": "transparent", "anchor": "w", "height": 40}
        
        ctk.CTkButton(self.sidebar, text="Dashboard", command=lambda: self.switch_frame("dashboard"), **btn_style).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Menu Input", command=lambda: self.switch_frame("menu_input"), **btn_style).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Design Studio", command=lambda: self.switch_frame("design"), **btn_style).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Export", command=lambda: self.switch_frame("export"), **btn_style).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Settings", command=lambda: self.switch_frame("settings"), **btn_style).pack(pady=5, padx=10, fill="x")

        # 2. Create Main Content Area on the right
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Default to Dashboard
        self.switch_frame("dashboard")

    def switch_frame(self, frame_name):
        # Clear existing frame in content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Instantiate the requested frame
        if frame_name == "dashboard":
            frame = DashboardFrame(self.content_area)
        elif frame_name == "menu_input":
            frame = MenuInputFrame(self.content_area)
        elif frame_name == "design":
            frame = DesignStudioFrame(self.content_area)
        elif frame_name == "export":
            frame = ExportFrame(self.content_area)
        elif frame_name == "settings":
            frame = SettingsFrame(self.content_area)
        else:
            return

        # Pack it into the content area
        frame.pack(fill="both", expand=True)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback

        # Center wrapper
        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(wrapper, text="Chef Krissy Menu Studio", font=("Helvetica", 28, "bold")).pack(pady=(0, 30))

        ctk.CTkLabel(wrapper, text="Username").pack(anchor="w")
        self.username_entry = ctk.CTkEntry(wrapper, width=300)
        self.username_entry.pack(pady=(0, 15))

        ctk.CTkLabel(wrapper, text="Password").pack(anchor="w")
        self.password_entry = ctk.CTkEntry(wrapper, width=300, show="*")
        self.password_entry.pack(pady=(0, 20))

        ctk.CTkButton(wrapper, text="Login", width=300, command=self.attempt_login).pack()

    def attempt_login(self):
        # For now, any non-empty username/password works
        if self.username_entry.get() and self.password_entry.get():
            self.login_callback()
        else:
            # Simple visual feedback for empty fields
            self.username_entry.configure(border_color="red")
            self.password_entry.configure(border_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()