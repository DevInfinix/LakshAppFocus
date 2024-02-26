"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.1
"""

__version__ = "1.0.1"

import customtkinter as ctk
import os
from PIL import Image
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class SplashApp(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("LakshApp - Stay Focused and Motivated - Loading")
        self.resizable(False, False)
        
        self.width = 440
        self.height = 600
        place_x = (self.winfo_screenwidth()//2) - (self.width//2)
        place_y = (self.winfo_screenheight()//2) - (self.height//2)
        self.geometry(f"{self.width}x{self.height}+{place_x}+{place_y}")
        self.overrideredirect(1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.configure(fg_color="black")
        
        self.wm_attributes("-topmost", True)
        self.lift()
        self.wm_attributes("-topmost", True)
        #.360
        self.bg = ctk.CTkLabel(self, image=self.get_splash(), text="", fg_color="transparent")
        self.bg.place(x=-76, y=-80)
        self.label = ctk.CTkButton(self, text=f"LOADING [v{__version__}]...", font=ctk.CTkFont(family="Ubuntu", size=18, weight="bold"), fg_color="gray20", corner_radius=30, hover_color="gray13")
        self.label.place(relx=0.015, rely=0.01)
        self.label2 = ctk.CTkButton(self, text="🗕  🗖  🗙", font=ctk.CTkFont(family="Ubuntu", size=18, weight="normal"), fg_color="gray20", corner_radius=30, hover_color="gray13")
        self.label2.place(relx=0.665, rely=0.01)
        
        for l in [self.label, self.label2]:
            l.bind("<Enter>", self.hover_cursor_on)
            l.bind("<Leave>", self.hover_cursor_off)
        
    def hover_cursor_on(self, event):
        self.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        self.configure(cursor="")
        
    def get_splash(self):
        # choice = random.choice(os.listdir("././images/Splash"))
        return ctk.CTkImage(dark_image=Image.open(resource_path('../images/Splash/lakshapp-splash-4.jpg')), size=(590,760))