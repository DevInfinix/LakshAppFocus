"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.1
"""

import customtkinter as ctk
from PIL import Image
import sys
import os
import pyglet

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

ASCII = """

██╗      █████╗ ██╗  ██╗███████╗██╗  ██╗ █████╗ ██████╗ ██████╗                                                                               
██║     ██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗                                                                              
██║     ███████║█████╔╝ ███████╗███████║███████║██████╔╝██████╔╝                                                                              
██║     ██╔══██║██╔═██╗ ╚════██║██╔══██║██╔══██║██╔═══╝ ██╔═══╝                                                                               
███████╗██║  ██║██║  ██╗███████║██║  ██║██║  ██║██║     ██║                                                                                   
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝                                                                                   
    █████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗                                                                                    
    ╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝                                                                                    
██████╗ ██╗   ██╗██╗   ██╗    ███╗   ███╗███████╗     █████╗      ██████╗ ██████╗ ███████╗███████╗███████╗███████╗                            
██╔══██╗██║   ██║╚██╗ ██╔╝    ████╗ ████║██╔════╝    ██╔══██╗    ██╔════╝██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╗                         
██████╔╝██║   ██║ ╚████╔╝     ██╔████╔██║█████╗      ███████║    ██║     ██║   ██║█████╗  █████╗  █████╗  █████╗  ╚═╝                         
██╔══██╗██║   ██║  ╚██╔╝      ██║╚██╔╝██║██╔══╝      ██╔══██║    ██║     ██║   ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══╝  ██╗                         
██████╔╝╚██████╔╝   ██║       ██║ ╚═╝ ██║███████╗    ██║  ██║    ╚██████╗╚██████╔╝██║     ██║     ███████╗███████╗╚═╝                         
╚═════╝  ╚═════╝    ╚═╝       ╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚══════╝                            
██╗  ██╗ ██████╗       ███████╗██╗    ██████╗ ██████╗ ███╗   ███╗    ██╗██████╗ ███████╗██╗   ██╗██╗███╗   ██╗███████╗██╗███╗   ██╗██╗██╗  ██╗
██║ ██╔╝██╔═══██╗      ██╔════╝██║   ██╔════╝██╔═══██╗████╗ ████║   ██╔╝██╔══██╗██╔════╝██║   ██║██║████╗  ██║██╔════╝██║████╗  ██║██║╚██╗██╔╝
█████╔╝ ██║   ██║█████╗█████╗  ██║   ██║     ██║   ██║██╔████╔██║  ██╔╝ ██║  ██║█████╗  ██║   ██║██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║ ╚███╔╝ 
██╔═██╗ ██║   ██║╚════╝██╔══╝  ██║   ██║     ██║   ██║██║╚██╔╝██║ ██╔╝  ██║  ██║██╔══╝  ╚██╗ ██╔╝██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║ ██╔██╗ 
██║  ██╗╚██████╔╝      ██║     ██║██╗╚██████╗╚██████╔╝██║ ╚═╝ ██║██╔╝   ██████╔╝███████╗ ╚████╔╝ ██║██║ ╚████║██║     ██║██║ ╚████║██║██╔╝ ██╗
╚═╝  ╚═╝ ╚═════╝       ╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝    ╚═════╝ ╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
                                                                                                                                              
"""
CHECK = "✓"
CROSS = "✗"
DELETE = "⌦"
EDIT = "✎"
SUB = "::  "
SUBSUB = "     ::  "
SUBSUBSUB = "          ::  "

ADD_IMG = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/add.png")))
SUB_IMG = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/drag.png")))
EDIT_IMG = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/pencil.png")))
DELETE_IMG = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/bin.png")))
RELOAD_IMG = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/reload.png")))
SWITCH_ON = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/switch-on.png")))
SWITCH_OFF = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Configuration/switch-off.png")))
TODO_HUMAN = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Humans/todo-human.png")))


SHORT_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/short-break.png")), size=(100,24))
LONG_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/long-break.png")), size=(100,25))
FOCUS_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/focus.png")), size=(100,35))
PAUSE_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/pause.png")), size=(80,60))
RESUME_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/resume.png")), size=(80,60))
OPTIONS_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/options.png")), size=(50,50))
SKIP_POMO = ctk.CTkImage(dark_image=Image.open(resource_path("../images/Pomodoro/skip.png")), size=(50,50))

for font_file in os.listdir(resource_path("../fonts")):
    pyglet.font.add_file(resource_path(os.path.join("../fonts", font_file)))
    
def LOBSTER(size=16, weight="bold"):
    return ctk.CTkFont(family="Lobster Two", size=size, weight=weight)

def LOBSTERTWO(size=17, weight="bold"):
    return ctk.CTkFont(family="LOBSTER", size=size, weight=weight)

def UBUNTU(size=18, weight="bold", slant="roman"):
    return ctk.CTkFont(family="UBUNTU", size=size, weight=weight, slant=slant)