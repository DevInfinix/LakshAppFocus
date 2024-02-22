"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.0
"""

import customtkinter as ctk
from PIL import Image

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

ADD_IMG = ctk.CTkImage(dark_image=Image.open("././images/Configuration/add.png"))
SUB_IMG = ctk.CTkImage(dark_image=Image.open("././images/Configuration/drag.png"))
EDIT_IMG = ctk.CTkImage(dark_image=Image.open("././images/Configuration/pencil.png"))
DELETE_IMG = ctk.CTkImage(dark_image=Image.open("././images/Configuration/bin.png"))
RELOAD_IMG = ctk.CTkImage(dark_image=Image.open("././images/Configuration/reload.png"))
SWITCH_ON = ctk.CTkImage(dark_image=Image.open("././images/Configuration/switch-on.png"))
SWITCH_OFF = ctk.CTkImage(dark_image=Image.open("././images/Configuration/switch-off.png"))
TODO_HUMAN = ctk.CTkImage(dark_image=Image.open("././images/Humans/todo-human.png"))

def UBUNTU(size=15, weight="bold"):
    return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def HELVETICA(size=30, weight="bold", slant="italic"):
    return ctk.CTkFont(family="Helvetica", size=size, weight=weight, slant=slant)