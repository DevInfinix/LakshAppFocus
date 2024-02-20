import customtkinter as ctk
from PIL import Image

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

def UBUNTU(size=15, weight="bold"):
    return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def HELVETICA(size=30, weight="bold", slant="italic"):
    return ctk.CTkFont(family="Helvetica", size=size, weight=weight, slant=slant)