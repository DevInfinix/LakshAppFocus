"""
Advanced TO-DOs integrated with Lice Sessions for Focus and Productivity
Author: DevInfinix
License: Apache-2.0
"""

import customtkinter as ctk
import tkinter
from tkinter import filedialog
from modules.CTkDataVisualizingWidgets import * #https://github.com/ZikPin/CTkDataVisualizingWidgets
from modules.CTkScrollableDropdown import *
from CTkMessagebox import CTkMessagebox
from async_tkinter_loop import async_handler
from async_tkinter_loop.mixins import AsyncCTk
from modules.database_handler import Database

import pytube
import pyperclip
import pygame
import json
import random

import os
from os import environ
import dotenv
import datetime
import asyncio
import websockets

from themes.colors import *
from themes.fonts import *


dotenv.load_dotenv()
WEBSOCKET_SERVER=os.getenv('WEBSOCKET_SERVER')
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("./themes/dark-blue.json") 
        

class App(ctk.CTk, AsyncCTk):
    def __init__(self):
        super().__init__()
        self.title("LakshApp - Stay Focused and Motivated")
        self.resizable(False, False)
        #self.iconbitmap('./images/lakshapp.ico')
        self.width = 1100
        self.height = 620
        self.geometry(f"{1100}x{620}")
        self.grid_columnconfigure((1,2,3), weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.total_message = 0
        self.role = None
        
        
        ############################################### PYGAME MUSIC ###############################################
         
         
         
        self.music = pygame.mixer
        self.music.init()
        self.paused = False
        self.trumpetsound = self.music.Sound('./sounds/trumpets.mp3')
        self.trumpetsound.set_volume(0.1)
        self.levelsound = self.music.Sound('./sounds/level.mp3')
        self.levelsound.set_volume(0.1)
        
         
        ############################################### DATABASE ###############################################
        
        
        
        with open("./data/quotes.json","r") as f:
            self.quotes = json.load(f)
        self.quote_no = (random.randint(0, len(self.quotes)) - 1)
        
        self.db = Database('./data/database.db')
        self.db.create_table()
        
        
        
        ############################################### SIDEBAR ###############################################
        
        
        
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=18, fg_color="gray8")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(15,7.5),pady=15, columnspan=1)
        self.sidebar_frame.grid_columnconfigure((0,1), weight=1)
        self.sidebar_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="LakshApp", font=UBUNTU(size=28), text_color=LIGHT_BLUE, justify="center")
        self.logo_label.grid(row=0, column=0, padx=40, pady=(100,60),columnspan=2, rowspan=1, sticky="ew")
        
        
        
        ############################################### TABS BUTTONS ###############################################
        
        
        
        self.hometab = ctk.CTkButton(master=self.sidebar_frame, text=" Home ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_home, font=UBUNTU())
        self.hometab.grid(padx=40, pady=8, row=1, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.todotab = ctk.CTkButton(master=self.sidebar_frame, text=" To-Do ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_todo, font=UBUNTU())
        self.todotab.grid(padx=40, pady=8, row=2, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.statstab = ctk.CTkButton(master=self.sidebar_frame, text=" My Progress ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_stats, font=UBUNTU())
        self.statstab.grid(padx=40, pady=8, row=3, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.sessionstab = ctk.CTkButton(master=self.sidebar_frame, text=" Live Sessions ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_sessions, font=UBUNTU())
        self.sessionstab.grid(padx=40, pady=8, row=4, column=0,columnspan=2, rowspan=1, sticky="ew")
        
        
        self.switch_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=20, fg_color="gray4")
        self.switch_frame.grid(row=5, column=0, sticky="nsew", padx=40,pady=(8,100), columnspan=2)
        self.switch_frame.grid_columnconfigure(0, weight=1)
        self.switch_frame.grid_rowconfigure(0, weight=1)
        
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self.switch_frame, text="Ambient Mode", onvalue="on", offvalue="off", variable=self.switch_var, command=self.switch_event, switch_height=15, switch_width=40, font=UBUNTU(size=14))
        self.switch.grid(row=0, column=0, pady=10, padx=10, sticky="ew", columnspan=1)
        
        
        
        ############################################### MAINFRAME ###############################################
        
        
        
        self.mainframe = ctk.CTkFrame(self, corner_radius=18, fg_color="gray8")
        self.mainframe.grid(column=1, row=0, sticky="nsew", padx=(7.5,15), pady=15,columnspan=3, rowspan=4)
        self.mainframe.grid_columnconfigure((0,1), weight=1)
        self.mainframe.grid_rowconfigure((0,1,2,3), weight=1)
        
        
        
        ############################################### TABVIEW ###############################################
        
        
        
        self.tab_view = ctk.CTkTabview(master=self.mainframe, corner_radius=18, fg_color="gray8")
        self.tab_view.grid(padx=0, pady=0,  sticky="nsew",column=0, row=0, columnspan=2, rowspan=4)
        
        self.home = self.tab_view.add("HOME")
        self.todo = self.tab_view.add("TO-DO")
        self.stats = self.tab_view.add("STATS")
        self.sessions = self.tab_view.add("SESSIONS")
        
        self.tab_view.set("HOME")
        self.hometab.configure(fg_color=THEME_BLUE)
        
        self.tab_view._segmented_button.grid_forget()
        
        self.tabsbutton = [self.hometab, self.todotab, self.statstab, self.sessionstab]
        
        
        
############################################### HOMETAB ###############################################
        
        
        self.home.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.home.grid_rowconfigure((0,1),weight=1)
        
        #self.github = ctk.CTkButton(master=self.sidebar_frame, command=self.test)
        #self.github.grid(padx=(10,5), pady=(10,140), row=4, column=0,columnspan=1, rowspan=1, sticky="ns")
        
        #self.developer = ctk.CTkButton(master=self.sidebar_frame, command=self.test)
        #self.developer.grid(padx=(5,10), pady=(10,140), row=4, column=1,columnspan=1, rowspan=1, sticky="ns")
        
        
        
       ############################################### QUOTES FRAME ###############################################
        
        
        
        self.quotes_frame = ctk.CTkFrame(master=self.home, fg_color="gray4", corner_radius=22)
        self.quotes_frame.grid(row=0, column=0, padx=0, pady=(5,0), sticky="nsew", columnspan=8)
        self.quotes_frame.grid_columnconfigure((0,1), weight=1)
        self.quotes_frame.grid_rowconfigure(0, weight=1)
        
        
        
        ############################################### QUOTES ###############################################
        
        
        
        self.quotes_label = ctk.CTkLabel(self.quotes_frame, text=f"“{self.quotes[self.quote_no]['text']}”", font=HELVETICA(weight="bold"), fg_color="transparent", wraplength=780, justify="center")
        self.quotes_label.grid(row=0, column=0, pady=(60,5), padx=20, sticky="nsew", columnspan=2)
        self.quotes_author_label = ctk.CTkLabel(self.quotes_frame, text=f"{self.quotes[self.quote_no]['author']}", font=HELVETICA(size=20, weight="normal"), fg_color="transparent")
        self.quotes_author_label.grid(row=1, column=0, pady=(0,0), padx=120, columnspan=8, sticky="nsew")
        
        self.change_quote_btn = ctk.CTkButton(self.quotes_frame, text="Refresh Quotes", command=self.change_quote_event, font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE,height=30)
        self.change_quote_btn.grid(row=2, column=0, pady=(40,40), padx=120, columnspan=2)
        
        
        
        ############################################### ENTRY ###############################################
        
        
        
        values = []
        for val in self.db.get_total_tasks():
            if val['project'] not in values:
                values.append(val['project'])
        if values == []:
            values.append("Default Project")

        self.home_projectselector = ctk.CTkOptionMenu(self.home, fg_color="black", button_color="gray12", dropdown_hover_color="gray13", corner_radius=8, font=UBUNTU(), dropdown_font=UBUNTU(), dynamic_resizing=False, anchor="w")
        self.home_projectselector.grid(row=3, column=0, pady=(20,0), padx=35, sticky="ew", columnspan=3)
        self.home_projectselector.set("Default Project")
        self.home_projectselector_dropdown = CTkScrollableDropdown(self.home_projectselector, values=values, alpha=0.9, justify="left")
        
        self.entry_todo = ctk.CTkEntry(self.home, placeholder_text="What are you planning to complete today? Start grinding champ!", font=UBUNTU(size=18, weight="normal"), corner_radius=50, height=60)
        self.entry_todo.grid(row=4, column=0, pady=(20,5), padx=(20,0),  sticky="ew", columnspan=7)
        self.add_todo = ctk.CTkButton(self.home, text="+", command=self.add_todo_event, font=UBUNTU(size=40, weight="normal"), corner_radius=100, fg_color="black", width=5, border_width=2, border_color="gray20", hover_color="gray20")
        self.add_todo.grid(row=4, column=0, pady=(20,0), padx=(10,20), columnspan=8, sticky="e")
        
        
        
        ############################################### PROGRESS ###############################################
        
        
        
        self.progressbar = ctk.CTkProgressBar(self.home, orientation="horizontal", height=15)
        self.progressbar.set(self.percent())
        self.progressbar.grid(row=5, column=0, pady=(10,5), padx=(45,35), sticky="ew", columnspan=8)
        
        self.progresslabel = ctk.CTkLabel(self.home, text=f"↪ Your Progress ({self.db.get_completed_tasks_count()}/{self.db.get_total_tasks_count()} completed)", font=UBUNTU(size=18, weight="normal"), justify="right")
        self.progresslabel.grid(row=6, column=0, pady=0, padx=25, sticky="e", columnspan=8)
        
        

        
        
############################################### TO-DO TAB ###############################################
        


        self.todo.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.todo.grid_rowconfigure((0,1),weight=1)
        
        self.scrollable_checkbox_frame = ToDoFrame(self.todo, db=self.db)
        
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=70, pady=(30, 0), sticky="ew", columnspan=8)
        self.scrollable_checkbox_frame.bind_all("<Button-4>", lambda e: self.scrollable_checkbox_frame._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_checkbox_frame.bind_all("<Button-5>", lambda e: self.scrollable_checkbox_frame._parent_canvas.yview("scroll", 1, "units"))

        self.button = ctk.CTkButton(self.todo, text="🗹 | Mark as Completed", command=self.mark_as_done)
        self.button.grid(row=1, column=0, padx=70, pady=(20,0), sticky="ew", columnspan=8)        
        
        self.button = ctk.CTkButton(self.todo, text="𐄂 | Delete all Tasks", command=self.delete_tasks, fg_color=THEME_RED, hover_color=RED)
        self.button.grid(row=2, column=0, padx=70, pady=(10,50), sticky="ew", columnspan=8) 
        
        
        self.add_button = ctk.CTkButton(self.todo, text="+", fg_color="gray4", width=60, font=UBUNTU(size=30), height=60, border_width=2, border_color="gray20", hover_color="gray20")
        self.add_button.place(relx=1, rely=1, anchor="se")
        

############################################### STATS TAB ###############################################


        self.stats.grid_columnconfigure((0,1),weight=1)
        self.stats.grid_rowconfigure(1,weight=1)
        
        
        self.stats_label = ctk.CTkLabel(self.stats, text=f"HERE's WHAT I ACHIEVED!", font=UBUNTU(size=30), fg_color="transparent", wraplength=780, justify="center")
        self.stats_label.grid(row=0, column=0, pady=(20,5), padx=60, sticky="new", columnspan=2)
        dates = self.db.get_total_tasks()
        if dates == []:
            values = {}
        else:
            values = {}
            for val in dates:
                date_tuple = (val['day'], val['month'], val['year'])
                if date_tuple not in values:
                    values[date_tuple] = 10
            self.calendar = CTkCalendarStat(self.stats, values, border_width=0, border_color=WHITE,
                                fg_color=NAVY_BLUE_DARK, title_bar_border_width=2, title_bar_border_color="gray80",
                                title_bar_fg_color=NAVY_BLUE, calendar_fg_color=NAVY_BLUE, corner_radius=30,
                                title_bar_corner_radius=10, calendar_corner_radius=10, calendar_border_color=WHITE,
                                calendar_border_width=0, calendar_label_pad=5, data_colors=["blue", "green", RED]
                    )
            self.calendar.grid(row=1, column=0, pady=(60,60), padx=60, sticky="new", columnspan=2)

        
        
############################################### SESSIONS TAB ###############################################


        self.sessions.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.sessions.grid_rowconfigure((0,1,2,3,4,5,6),weight=1)


        self.sessions_progressbutton = ctk.CTkButton(self.sessions, text="Start Session", command=self.start_sessions_timer, font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE)
        self.sessions_progressbutton.grid(row=0, column=0, pady=0, padx=(10, 0), sticky="ew", columnspan=6, rowspan=1)
        
        
        self.sessions_leavebutton = ctk.CTkButton(self.sessions, text="⍇ Leave Room", command=self.leavesession, font=UBUNTU(size=15), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED, hover_color=RED)
        self.sessions_leavebutton.grid(row=0, column=0, pady=0, padx=(0, 10), sticky="e", columnspan=8, rowspan=1)
            
        
        
        self.sessions_progressbar = ctk.CTkProgressBar(self.sessions, orientation="horizontal", height=15)
        self.sessions_progressbar.set(0)
        self.sessions_progressbar.grid(row=2, column=0, pady=(0,0), padx=15, sticky="ew", columnspan=8, rowspan=1)
        
        
        if self.role == 'member':
            self.sessions_progressbutton.destroy()
            self.sessions_progressbutton = ctk.CTkButton(self.sessions, state="disabled", text="The host can start a session", font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE)
            self.sessions_progressbutton.grid(row=0, column=0, pady=0, padx=(10, 0), sticky="ew", columnspan=6, rowspan=1)
        
        
        self.sessions_frame = ctk.CTkScrollableFrame(self.sessions, corner_radius=18, fg_color="gray4")
        self.sessions_frame.grid(row=3, column=0, sticky="nsew", padx=15,pady=(10,15), columnspan=8, rowspan=3)
        self.sessions_frame.grid_columnconfigure((0,1), weight=1)
        
        self.sessions_frame.bind_all("<Button-4>", lambda e: self.sessions_frame._parent_canvas.yview("scroll", -1, "units"))
        self.sessions_frame.bind_all("<Button-5>", lambda e: self.sessions_frame._parent_canvas.yview("scroll", 1, "units"))
        
        self.send_area = ctk.CTkEntry(self.sessions, placeholder_text="Say Hello to your session partner!", font=UBUNTU(size=18, weight="normal"), corner_radius=50, height=60)
        self.send_area.grid(row=6, column=0, pady=(0,8), padx=(15,15),  sticky="sew", columnspan=7, rowspan=1)
        self.send_button = ctk.CTkButton(self.sessions, text="➤", command=self.add_own_message, font=UBUNTU(size=30, weight="normal"), corner_radius=100, fg_color="transparent", width=2, height=60, hover_color="gray4")
        self.send_button.grid(row=6, column=0, pady=(0,8), padx=(15,15), columnspan=8, sticky="se", rowspan=1)
        
        
            
############################################### FUNCTIONS ###############################################


        self.socket = None
    
    
    def switch_event(self):
        sw = self.switch_var.get()
        if sw == "on":
            self.play()
        if sw == "off":
            self.paused = True
            self.music.music.pause()
    
    def play_youtube(self):
        dialog = ctk.CTkInputDialog(text="Search the perfect ambience on YouTube.", title="LakshApp")
        inp = dialog.get_input()
        
    def play(self):
        if not self.paused:   
            file_path = filedialog.askopenfilename(title="Select an ambient song", filetypes=(("Audio Files", ".wav .ogg .mp3"),   ("All Files", "*.*")))
            if file_path:
                self.music.music.load(file_path)
                self.music.music.play(-1, fade_ms=2000)
            else:
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Select a valid format to play music (mp3/ogg/wav).", sound=True, option_1="Okay")
                self.switch.deselect()
        else:
            self.music.music.unpause()



    def change_quote_event(self):
        if self.quote_no == (len(self.quotes)-1):
            self.quote_no = 0
        else:
            self.quote_no += 1
        self.quotes_label.configure(text=f"“{self.quotes[self.quote_no]['text']}”")
        self.quotes_author_label.configure(text=f"“{self.quotes[self.quote_no]['author']}”")
        
    def increment_progress_bar(self):
        self.progressbar.step()

    def percent(self):
        if self.db.get_total_tasks_count() == 0:
            return 0
        return (self.db.get_completed_tasks_count()/self.db.get_total_tasks_count())
        
        
    @async_handler
    async def mark_as_done(self):
        checkboxes = self.scrollable_checkbox_frame.get()
        if checkboxes == []:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="info", message="Please select a task first.", sound=True, option_1="Cool")
        else:
            dialog = ctk.CTkInputDialog(text="Type 'done' to confirm the completion of tasks.", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'done':
                    for check in checkboxes:
                        check.configure(state=tkinter.DISABLED)
                        today = datetime.date.today()
                        self.db.update_todo_status(int(check.cget("text").split("|")[0]), True)
                    self.progressbar.set(self.percent())
                    self.update_progresslabel()
                    self.trumpetsound.play()
                
                    
    @async_handler            
    async def delete_tasks(self):
        checkboxes = self.scrollable_checkbox_frame.checkboxes
        if checkboxes == [] or not checkboxes:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="info", message="The To-Do list is empty. Add your first To-Do now!", sound=True, option_1="Cool")
        else:
            dialog = ctk.CTkInputDialog(text="Type 'delete' to confirm the deletion of tasks.", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'delete':
                    for i in checkboxes:
                        i.destroy()
                    self.scrollable_checkbox_frame.checkboxes = []
                    self.db.delete_all_todos()
                    self.progressbar.set(0)
                    self.update_progresslabel()
                    CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="Successfully deleted all To-Dos!", sound=True, option_1="Less Gooo!!!")
        
    
    @async_handler
    async def add_todo_event(self, asyncmode=True):
        event = self.entry_todo.get()
        if event == "":
            return
        today = datetime.date.today()
        id = self.db.add_todo(event, "PROJECT", False, today.day, today.month, today.year)
        self.progressbar.set(self.percent())
        self.update_progresslabel()
        
        checkboxes = self.scrollable_checkbox_frame.checkboxes
        checkbox = ctk.CTkCheckBox(self.scrollable_checkbox_frame, text=f"{id} | {event} | PROJECT", hover=True)
        checkbox.grid(row=len(checkboxes), column=0, padx=50, pady=(10, 10), sticky="ew", columnspan=2)
        checkboxes.append(checkbox)
        
    
        CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The task has been added to your To-Do List.\nGo to To-Do Tab to view more!", sound=True, option_1="There we go!")
        self.entry_todo.delete(0, "end")
        self.levelsound.play()
    
    
    
    def update_progresslabel(self):
        self.progresslabel.configure(text=f"↪ Your Progress ({self.db.get_completed_tasks_count()}/{self.db.get_total_tasks_count()} completed)")
        



############################################### KEYBINDS ###############################################



app = App()


def enter(event):
    if app.tab_view.get() == 'HOME':
        app.add_todo_event()
    if app.tab_view.get() == 'SESSIONS':
        app.add_own_message()

def ctrla(event):
    app.select_all()
    
app.bind('<Return>', enter)
app.bind('<Control-a>', ctrla)

app.protocol("WM_DELETE_WINDOW", app.close_confirmation)

app.async_mainloop()
