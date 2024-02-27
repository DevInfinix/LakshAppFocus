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

class SplashApp(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("LakshApp - Stay Focused and Motivated - Loading")
        self.resizable(False, False)
        
    def hover_cursor_on(self, event):
        self.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        self.configure(cursor="")
        
    def get_splash(self):
        # choice = random.choice(os.listdir("././images/Splash"))
        return ctk.CTkImage(dark_image=Image.open(resource_path('../images/Splash/lakshapp-splash-4.jpg')), size=(590,760))
