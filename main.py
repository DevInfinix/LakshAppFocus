"""
Advanced TO-DOs integrated with Lice Sessions for Focus and Productivity
Author: DevInfinix
License: Apache-2.0
"""

import customtkinter as ctk
import tkinter
from tkinter import filedialog
from modules.CTkDataVisualizingWidgets import * #https://github.com/ZikPin/CTkDataVisualizingWidgets
from CTkMessagebox import CTkMessagebox
from async_tkinter_loop import async_handler
from async_tkinter_loop.mixins import AsyncCTk

import pyperclip
import pygame
import aiofiles
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
        
         
        ############################################### DATA ###############################################
        
        
        
        with open("./data/quotes.json","r") as f:
            self.quotes = json.load(f)
        with open("./data/donetasks.json","r") as f:
            self.donetasks = json.load(f)
        self.quote_no = (random.randint(0, len(self.quotes)) - 1)
        
        
        
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
        self.quotes_label.grid(row=0, column=0, pady=(60,5), padx=20, sticky="new", columnspan=2)
        self.quotes_author_label = ctk.CTkLabel(self.quotes_frame, text=f"{self.quotes[self.quote_no]['author']}", font=HELVETICA(size=20, weight="normal"), fg_color="transparent")
        self.quotes_author_label.grid(row=1, column=0, pady=(0,0), padx=120, columnspan=8, sticky="new")
        
        self.change_quote_btn = ctk.CTkButton(self.quotes_frame, text="Refresh Quotes", command=self.change_quote_event, font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE,height=30)
        self.change_quote_btn.grid(row=2, column=0, pady=(50,60), padx=120, columnspan=2)
        
        
        
        ############################################### ENTRY ###############################################
        
        
        
        self.entry_todo = ctk.CTkEntry(self.home, placeholder_text="What are you planning to complete today? Start grinding champ!", font=UBUNTU(size=18, weight="normal"), corner_radius=50, height=60)
        self.entry_todo.grid(row=3, column=0, pady=(60,0), padx=(20,0),  sticky="ew", columnspan=7)
        self.add_todo = ctk.CTkButton(self.home, text="+", command=self.add_todo_event, font=UBUNTU(size=40, weight="normal"), corner_radius=100, fg_color="black", width=5)
        self.add_todo.grid(row=3, column=0, pady=(60,0), padx=(2,20), columnspan=8, sticky="e")
        
        
        
        ############################################### PROGRESS ###############################################
        
        
        
        self.progressbar = ctk.CTkProgressBar(self.home, orientation="horizontal", height=15)
        self.progressbar.set(self.percent())
        self.progressbar.grid(row=4, column=0, pady=(20,5), padx=(45,25), sticky="ew", columnspan=8)
        self.progresslabel = ctk.CTkLabel(self.home, text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)", font=UBUNTU(size=18, weight="normal"), justify="right")
        self.progresslabel.grid(row=5, column=0, pady=0, padx=25, sticky="e", columnspan=8)
        
        

        
        
############################################### TO-DO TAB ###############################################
        

        self.todo.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.todo.grid_rowconfigure((0,1),weight=1)
        
        
        values = self.donetasks["pendingtasks"]
        self.scrollable_checkbox_frame = ToDoFrame(self.todo, values=values)
        
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=70, pady=(30, 0), sticky="ew", columnspan=8)
        self.scrollable_checkbox_frame.bind_all("<Button-4>", lambda e: self.scrollable_checkbox_frame._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_checkbox_frame.bind_all("<Button-5>", lambda e: self.scrollable_checkbox_frame._parent_canvas.yview("scroll", 1, "units"))

        self.button = ctk.CTkButton(self.todo, text="🗹 | Mark as Completed", command=self.mark_as_done)
        self.button.grid(row=1, column=0, padx=70, pady=(20,0), sticky="ew", columnspan=8)        
        
        self.button = ctk.CTkButton(self.todo, text="𐄂 | Delete all Tasks", command=self.delete_tasks, fg_color=THEME_RED, hover_color=RED)
        self.button.grid(row=2, column=0, padx=70, pady=(10,50), sticky="ew", columnspan=8) 
        
        

############################################### STATS TAB ###############################################


        self.stats.grid_columnconfigure((0,1),weight=1)
        self.stats.grid_rowconfigure(1,weight=1)
        
        
        self.stats_label = ctk.CTkLabel(self.stats, text=f"HERE's WHAT I ACHIEVED!", font=UBUNTU(size=30), fg_color="transparent", wraplength=780, justify="center")
        self.stats_label.grid(row=0, column=0, pady=(20,5), padx=60, sticky="new", columnspan=2)
        dates = self.donetasks['dates']
        if dates == []:
            values = {}
        else:
            values = {tuple(val): 10 for val in dates}
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
        if self.donetasks["pendingtasks"] == {}:
            return 0
        return (self.donetasks["count"]/self.donetasks["total"])
        
        
    @async_handler
    async def mark_as_done(self):
        await self.refresh_cache()
        checkboxes = self.scrollable_checkbox_frame.get(self.donetasks)
        if checkboxes == []:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="info", message="Please select a task first.", sound=True, option_1="Cool")
        else:
            dialog = ctk.CTkInputDialog(text="Type 'done' to confirm the completion of tasks.", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'done':
                    for check in checkboxes:
                        self.donetasks["pendingtasks"][check.cget("text")] = 1
                        self.donetasks["count"] += 1
                        check.configure(state=tkinter.DISABLED)
                        dates = self.donetasks["dates"]
                        today = [datetime.date.today().day,datetime.date.today().month,datetime.date.today().year]
                        if not today in dates: 
                            self.donetasks["dates"].append(today)
                    await self.save_config(self.donetasks)
                    self.progressbar.set(self.percent())
                    self.progresslabel.configure(text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)")
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
                    self.donetasks["pendingtasks"] = {}
                    self.donetasks["count"] = 0
                    self.donetasks["total"] = 0
                    await self.save_config(self.donetasks)
                    self.progressbar.set(0)
                    self.progresslabel.configure(text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)")
                    CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="Successfully deleted all To-Dos!", sound=True, option_1="Less Gooo!!!")
        
    
    @async_handler
    async def add_todo_event(self, asyncmode=True):
        event = self.entry_todo.get()
        if event == "":
            return
        elif event in self.donetasks["pendingtasks"]:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="A task with the same title is already pending/completed.", sound=True, option_1="Oh Shit!")
            return
        self.donetasks["total"] += 1
        self.donetasks["pendingtasks"][event] = 0
        await self.save_config(self.donetasks)
        self.progressbar.set(self.percent())
        self.progresslabel.configure(text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)")
        
        
        checkboxes = self.scrollable_checkbox_frame.checkboxes
        checkbox = ctk.CTkCheckBox(self.scrollable_checkbox_frame, text=event, hover=True)
        checkbox.grid(row=len(checkboxes), column=0, padx=50, pady=(10, 10), sticky="ew", columnspan=2)
        checkboxes.append(checkbox)
        
    
        CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The task has been added to your To-Do List.\nGo to To-Do Tab to view more!", sound=True, option_1="There we go!")
        self.entry_todo.delete(0, "end")
        self.levelsound.play()
    
    
        
    def set_current_tab(self, current_tab):
        for tab in self.tabsbutton:
            if current_tab == tab:
                tab.configure(fg_color=THEME_BLUE)
            else:
                tab.configure(fg_color="gray13")
        
    def set_home(self):
        self.tab_view.set("HOME")
        self.set_current_tab(self.hometab)
        
    def set_todo(self):
        self.tab_view.set("TO-DO")
        self.set_current_tab(self.todotab)
        
    @async_handler
    async def set_stats(self):
        await self.refresh_cache()
        dates = self.donetasks['dates']
        if dates == []:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="You haven't completed any tasks yet.\nStart completing now!", sound=True, option_1="Oh shit!")
        else:
            values = {tuple(val): 10 for val in dates}
            self.calendar.destroy()
            self.calendar = CTkCalendarStat(self.stats, values, border_width=0, border_color=WHITE,
                                fg_color=NAVY_BLUE, title_bar_border_width=2, title_bar_border_color="gray80",
                                title_bar_fg_color=NAVY_BLUE, calendar_fg_color=NAVY_BLUE, corner_radius=30,
                                title_bar_corner_radius=10, calendar_corner_radius=10, calendar_border_color=WHITE,
                                calendar_border_width=0, calendar_label_pad=5, data_colors=["blue", "green", RED]
                    )
            self.calendar.grid(row=1, column=0, pady=(60,60), padx=60, sticky="new", columnspan=2)
            self.tab_view.set("STATS")
            self.set_current_tab(self.statstab)
            
        
    @async_handler
    async def set_sessions(self):
        if not self.socket:
            dialog = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="info", message="Select 'Start' to host a session. If you have a valid session code, select 'Join'.", sound=True, option_1="Join", option_2="Start")
            inp = dialog.get()
            if inp:
                if inp.lower() == 'start':
                    dialog2 = ctk.CTkInputDialog(text="Enter your username\nfor the live session.", title="LakshApp")
                    inp2 = dialog2.get_input()
                    if inp2:
                        if inp2 != '':
                            self.own_username = inp2
                            await self.start_server(WEBSOCKET_SERVER, inp2)
                if inp.lower() == 'join':
                    dialog2 = ctk.CTkInputDialog(text="Enter the code for the live session.", title="LakshApp")
                    inp2 = dialog2.get_input()
                    if inp2:
                        if inp2 != '':
                            self.server_code = inp2
                            
                            dialog3 = ctk.CTkInputDialog(text="Enter your username\nfor the live session.", title="LakshApp")
                            inp3 = dialog3.get_input()
                            if inp3:
                                if inp3 != '':
                                    self.own_username = inp3
                                    await self.join_server(WEBSOCKET_SERVER, inp2, inp3)
        else:
            self.tab_view.set("SESSIONS")
            self.set_current_tab(self.sessionstab)
                
            
        
    def select_all(self):
        if self.tab_view.get() == 'TO-DO':
            self.entry_todo.select_range(0, 'end')
            self.entry_todo.icursor('end')
            return 'break'
        if self.tab_view.get() == 'SESSIONS':
            self.send_area.select_range(0, 'end')
            self.send_area.icursor('end')
            return 'break'
        
    
    async def refresh_cache(self):
        async with aiofiles.open("./data/donetasks.json","r") as f:
            self.donetasks = json.loads(await f.read())
    
    async def save_config(self, config):
        async with aiofiles.open("./data/donetasks.json", "w") as f:
            await f.write(json.dumps(config, indent=4))
            
            
    @async_handler
    async def leavesession(self):
        d = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="Done for the day? Hope to see you soon!\n[Attention: Ending the session will result in the loss of all your progress during the session.]", sound=True, option_1="I'm done", option_2="I'm staying")
        if d.get() == "I'm done":
            await self.close_socket()

    
    
    @async_handler
    async def add_own_message(self):
        message = self.send_area.get()
        if message == '':
            self.send_area.focus()
            return
        message_frame = ctk.CTkFrame(self.sessions_frame, corner_radius=18, fg_color="gray13")
        message_frame.grid(row=self.total_message, column=0, sticky="new", padx=5,pady=5, columnspan=2, rowspan=1)
        message_frame.grid_columnconfigure((0,1), weight=1)
        
        message_label = ctk.CTkLabel(message_frame, text=f"[You]: {message}", font=UBUNTU(size=18, weight="normal"), fg_color="transparent", wraplength=680, justify="left", state="disabled")
        message_label.grid(row=0, column=0, pady=5, padx=15, sticky="nw", columnspan=2)
        
        self.sessions_frame.after(10, self.sessions_frame._parent_canvas.yview_moveto, 1.0)
        
        self.total_message += 1
        
        data = {
            'from': 'client',
            'type': 'message',
            'message': message,
            'user': self.own_username
        }
        try:
            await self.socket.send(json.dumps(data))
        except:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Server disconnected. Please check your internet connection.", sound=True, option_1="Ah sad!")
            await self.close_socket()
        self.send_area.delete(0, "end")
        
        
    def add_other_message(self, user, message):
        message_frame = ctk.CTkFrame(self.sessions_frame, corner_radius=18, fg_color="gray22")
        if user == 'System':
            message_frame.configure(fg_color=THEME_BLUE)
        message_frame.grid(row=self.total_message, column=0, sticky="new", padx=5,pady=5, columnspan=2, rowspan=1)
        message_frame.grid_columnconfigure((0,1), weight=1)
        
        message_label = ctk.CTkLabel(message_frame, text=f"[{user}]: {message}", font=UBUNTU(size=18, weight="normal"), fg_color="transparent", wraplength=680, justify="left", state="disabled")
        message_label.grid(row=0, column=0, pady=5, padx=15, sticky="nw", columnspan=2)
            
        self.total_message += 1
        
        self.sessions_frame.after(10, self.sessions_frame._parent_canvas.yview_moveto, 1.0)
    
    
    async def close_socket(self):
        try:
            await self.socket.close()
        except:
            pass
        self.socket = None
        self.set_home()
        
    
    @async_handler
    async def start_sessions_timer(self):
        d = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="info", message="Select duration of session", sound=True, options=['30 Minutes', '45 Minutes', '1 Hour'])
        if d.get() in ['30 Minutes', '45 Minutes', '1 Hour']:
            event = {
                'type': 'startsession',
                'from': 'client',
                'duration': d.get()
            }
            try:
                await self.socket.send(json.dumps(event))
            except:
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Server disconnected. Please check your internet connection.", sound=True, option_1="Ah sad!")
                await self.close_socket()
        
    
    @async_handler
    async def stop_sessions_timer(self):
        dialog = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="Do you want to end this session?", sound=True, options=["I'm done", "Don't end it yet"])
        if dialog.get() == "I'm done":
            event = {
                'type': 'stopsession',
                'from': 'client'
            }
            try:
                await self.socket.send(json.dumps(event))
            except:
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Server disconnected. Please check your internet connection.", sound=True, option_1="Ah sad!")
                await self.close_socket()
        elif dialog.get() == "Don't end it yet":
            pass
    
    async def start_server(self, server_address, username):
        try:
            async with websockets.connect(server_address) as socket:
                event = {
                    'from': 'client',
                    'type': 'start',
                    'user': username
                }
                await asyncio.sleep(0)
                await socket.send(json.dumps(event))
                self.role = 'host'
                await asyncio.gather(self.receive_message(socket, 'host', username))
        except:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Server disconnected. Please check your internet connection.", sound=True, option_1="Ah sad!")
            await self.close_socket()
         
       
    async def join_server(self, server_address, code, username):
        try:
            async with websockets.connect(server_address) as socket:
                event = {
                    'from': 'client',
                    'type': 'join',
                    'code': code,
                    'user': username
                }
                await asyncio.sleep(1)
                await socket.send(json.dumps(event)) 
                self.role = 'member'
                await asyncio.gather(self.receive_message(socket, 'member', username))
        except:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Server disconnected. Please check your internet connection.", sound=True, option_1="Ah sad!")
            await self.close_socket()
                
                
    async def receive_message(self, socket, role, username):
        async for message in socket:
            event = json.loads(message)
            if event['type'] == 'error':
                if event['errortype'] == 'SessionNotFound':
                    CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message=event['message'], sound=True, option_1="Oh shit!")
                    self.set_home()
                    break
                if event['errortype'] == 'RoomFull':
                    CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message=event['message'], sound=True, option_1="Oh shit!")
                    self.set_home()
                    break
            if event['type'] == 'started':
                self.tab_view.set("SESSIONS")
                self.set_current_tab(self.sessionstab)
                await asyncio.sleep(1)
                print(f"Your code is: [{event['code']}]")
                pyperclip.copy(event['code'])
                self.add_other_message(user='System', message=f"Your room's code is: [{event['code']}] | The code has been copied to your clipboard.")
                self.socket = socket
            if event['type'] == 'joined':
                self.tab_view.set("SESSIONS")
                self.set_current_tab(self.sessionstab)
                await asyncio.sleep(1)
                print(f"You joined {event['code']}")
                pyperclip.copy(event['code'])
                self.add_other_message(user='System', message=f"You joined {event['code']} | The code has been copied to your clipboard.")
                self.socket = socket
                self.sessions_progressbutton.configure(state="disabled", text="The host can start a session")
            if event['type'] == 'message':
                if event['user'] != username:
                    self.add_other_message(user=event['user'], message=event['message'])
            if event['type'] == 'startsessionconfirmed':
                duration = event['duration']
                time = self.convert_time(duration)
                self.sessions_progressbar_task = asyncio.create_task(self.update_sessions_progressbar(10))
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message=f'Session started for {duration}!\nKeep Grinding!', sound=True, option_1="Let's do this!")
                self.levelsound.play()
                if self.role == 'member':
                    self.sessions_progressbutton.configure(fg_color=THEME_RED, hover_color=RED, border_color=RED, state="disabled", text="Session started by the host")
                else:
                    self.sessions_progressbutton.configure(fg_color=THEME_RED, hover_color=RED, border_color=RED, text="Stop Session", command=self.stop_sessions_timer)
                
            if event['type'] == 'stopsessionconfirmed':
                self.sessions_progressbar_task.cancel()
                await asyncio.sleep(1)
                self.sessions_progressbar.set(0)
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message=f'Session stopped by the host!\nSee you soon!', sound=True, option_1="Lost it!")
                if self.role == 'member':
                    self.sessions_progressbutton.configure(hover_color=THEME_BLUE, fg_color="gray13", state="disabled", text="The host can start a session", border_color=THEME_BLUE)
                else:
                    self.sessions_progressbutton.configure(hover_color=THEME_BLUE, fg_color="gray13", text="Start Session", command=self.start_sessions_timer, border_color=THEME_BLUE)
                
            if event['type'] == 'disconnected':
                if event['from'] == 'server':
                    if event['role'] == 'host':
                        print('The host has been disconnected')
                        CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message='The host has been disconnected', sound=True, option_1="Oh shit!")
                        await asyncio.sleep(1)
                        self.tab_view.set("HOME")
                        self.set_current_tab(self.hometab)
                        self.socket = None
                        if role == 'host':
                            return
                        else:
                            break
                    elif event['role'] == 'member':
                        print('Participant disconnected')
                        if role == 'member':
                            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message='You have been disconnected', sound=True, option_1="Oh Shit!")
                            await asyncio.sleep(1)
                            self.tab_view.set("HOME")
                            self.set_current_tab(self.hometab)
                            return
                        else:
                            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message='The participant has been disconnected', sound=True, option_1="Oh shit!")
                                    

    async def update_sessions_progressbar(self, time):
        cur = 1
        while True:
            if cur/time == 1:
                self.sessions_progressbar.set(0)
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message=f'Session completed! Well done comrade!', sound=True, option_1="Less gooo!")
                self.trumpetsound.play()
                if self.role == 'member':
                    self.sessions_progressbutton.configure(hover_color=THEME_BLUE, fg_color="gray13", state="disabled", text="The host can start a session", border_color=THEME_BLUE)
                else:
                    self.sessions_progressbutton.configure(hover_color=THEME_BLUE, fg_color="gray13", text="Start Session", command=self.start_sessions_timer, border_color=THEME_BLUE)
                return
            self.sessions_progressbar.set(cur/time)
            cur += 1
            await asyncio.sleep(1)
            
        
        
    def convert_time(self, time):
        time = time.lower()
        if 'minute' in time:
            return int(int(time.split(' ')[0])*60)
        if 'hour' in time:
            return int(int(time.split(' ')[0])*3600)
    
    
    
    @async_handler
    async def close_confirmation(self):
        dialog = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="Done for the day? Hope to see you soon!", sound=True, option_1="Exit", option_2="Keep Grinding")
        if dialog.get() == "Exit":
            if self.socket:
                try:
                    await self.socket.close()
                except:
                    pass
            self.destroy()
        else:
            pass
        
        

############################################### TO-DO FRAME ###############################################



class ToDoFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master, label_text="⇲ MY TO-DO LIST", label_fg_color=DULL_BLUE, border_width=2, border_color=BLACK, corner_radius=18, fg_color="gray4", label_font=UBUNTU(size=15))

        self.values = values
        self.checkboxes = []

        for i, value in enumerate(list(self.values.keys())):
            state = tkinter.DISABLED if (self.values.get(value) == 1) else tkinter.NORMAL
            checkbox = ctk.CTkCheckBox(self, text=value, hover=True, state=state, onvalue="on", offvalue="off", command=self.add_temp_check())
            if self.values.get(value) == 1:
                checkbox.select()
            checkbox.grid(row=i, column=0, padx=50, pady=(10, 10), sticky="ew", columnspan=2)
            self.checkboxes.append(checkbox)
        
    def add_temp_check(self):
        pass
        
    def get(self, donetasks):
        if self.checkboxes == [] or not self.checkboxes:
            print("no checkboxes fount", self.checkboxes)
        checked_checkboxes = []
        print(donetasks['pendingtasks'])
        for checkbox in self.checkboxes:
            if (checkbox.get() == "on" or checkbox.get() == "1" or checkbox.get() == 1) and donetasks["pendingtasks"][checkbox.cget('text')] == 0:
                checked_checkboxes.append(checkbox)
        return checked_checkboxes
    
        
        
############################################### MESSAGE DIALOGUE ###############################################
         
         
         
class MessageDialogue(ctk.CTkToplevel):
    def __init__(self, message):
        super().__init__()
        self.geometry("300x100")

        self.label = ctk.CTkLabel(self, text=f"{message}")
        self.label.pack(padx=20, pady=20)



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