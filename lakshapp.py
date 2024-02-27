"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.1
"""

__version__="1.0.1"

import logging
from modules import AppData
logfile = AppData("lakshapp", "lakshapp-logs.txt")
logging.basicConfig(level=logging.INFO, format="[LakshApp Logs] %(asctime)s - %(levelname)s - %(message)s", filename=logfile.get_file_path())

try:
    import customtkinter as ctk
    # import tkinter
    from tkinter import filedialog
    import tkinter.ttk as ttk
    from async_tkinter_loop import async_handler
    from async_tkinter_loop.mixins import AsyncCTk
    from modules import *
    from themes import *

    from PIL import Image
    import pyperclip
    import json
    import random
    import textwrap

    from os import environ
    import plyer
except ImportError as e:
    logging.critical(f"Couldn't Import Modules: {e}", exc_info=True)
    print(colorama.Fore.RED + "ImportError: Check logs for more info.")
    exit(1)

colorama.init(autoreset=True)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

WEBSOCKET_SERVER='ws://infinix-v4.duckdns.org:8080'

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(resource_path("themes/dark-blue.json")) 


class App(ctk.CTk, AsyncCTk):
    def __init__(self):
        super().__init__()
        logging.info('SplashScreen initialized...')
        self.title("LakshApp - Stay Focused and Motivated")
        self.resizable(True, True)
        #self.iconbitmap('./images/lakshapp.ico')
        self.width = 1100
        self.height = 620
        place_x = (self.winfo_screenwidth()//2) - (self.width//2)
        place_y = (self.winfo_screenheight()//2) - (self.height//2)
        self.geometry(f"{self.width}x{self.height}+{place_x}+{place_y}")
        self.minsize(1100,620)
        self.grid_columnconfigure((1,2,3), weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.version = __version__
    
        
        
        ############################################### DATABASE ###############################################
    
        
        self.db = Database('database.db')
        self.db.create_todo_table()
        
        
############################################### SPLASH SCREEN ###############################################


        self.splashapp.destroy()
        self.deiconify()
        self.lift()
        logging.info('LakshApp is Running!')
        
        
        
############################################### FUNCTIONS ###############################################

    
    
    def fullscreen(self):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
        elif not self.attributes("-fullscreen"):
            self.attributes("-fullscreen", True)
            
    def hover_cursor_on(self, event):
        event.widget.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        event.widget.configure(cursor="")
        
    def select_all(self):
        if self.mainframe.tab_view.get() == 'HOME':
            self.home.entry_todo.select_range(0, 'end')
            self.home.entry_todo.icursor('end')
            return 'break'
        if self.mainframe.tab_view.get() == 'SESSIONS':
            self.sessions.send_area.select_range(0, 'end')
            self.sessions.send_area.icursor('end')
            return 'break'
    
    def toggle_edit_sidepanel(self, project):
        if project in self.todo.project_sidepanels:
            sidepanel = self.todo.project_sidepanels[project]
            sidepanel.animate()
        
    def convert_time(self, time):
        time = time.lower()
        if 'minute' in time:
            return int(int(time.split(' ')[0])*60)
        if 'hour' in time:
            return int(int(time.split(' ')[0])*3600)
        





############################################### MAINFRAME ###############################################



class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=18, fg_color="gray8")
        self.master = master
        self.grid(column=1, row=0, sticky="nsew", padx=(7.5,15), pady=15,columnspan=3, rowspan=4)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)
        
        self.load_tabview()
        
    
    def load_tabview(self):
        self.tab_view = ctk.CTkTabview(master=self, corner_radius=18, fg_color="gray8")
        self.tab_view.grid(padx=0, pady=0,  sticky="nsew",column=0, row=0, columnspan=2, rowspan=4)

        self.master.home = HomeTab(self.master, self.tab_view.add("HOME"))
        self.master.todo = ToDoTab(self.master, self.tab_view.add("TO-DO"))
        self.master.pomodoro = PomodoroTab(self.master, self.tab_view.add("POMODORO"))
        self.master.stats = StatsTab(self.master, self.tab_view.add("STATS"))
        self.master.sessions = SessionsTab(self.master, self.tab_view.add("SESSIONS"))
        
        self.tab_view.set("HOME")
        self.master.sidebar.hometab.configure(fg_color=THEME_BLUE)
        
        self.tab_view._segmented_button.grid_forget()
        
        
        
############################################### HOMETAB ###############################################



class HomeTab():
    def __init__(self, master, parent_tabview):
        self.master = master
        self.db = self.master.db
        
        self.home = parent_tabview
        
        self.home.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.home.grid_rowconfigure((0,1),weight=1)
        
        self.load_quotes()
        self.load_quotes_frame()
        self.load_quotes_label()
        self.load_home_selector()
        self.load_home_entry()
        self.load_progressbar()
        
        #self.github = CursorButton(master=self.sidebar_frame, command=self.test)
        #self.github.grid(padx=(10,5), pady=(10,140), row=4, column=0,columnspan=1, rowspan=1, sticky="ns")
        
        #self.developer = CursorButton(master=self.sidebar_frame, command=self.test)
        #self.developer.grid(padx=(5,10), pady=(10,140), row=4, column=1,columnspan=1, rowspan=1, sticky="ns")
        
    def load_quotes(self):
        with open(resource_path("data/quotes.json"),"r") as f:
            self.quotes = json.load(f)
        self.quote_no = (random.randint(0, len(self.quotes)) - 1)
        
    def change_quote_event(self):
        if self.quote_no == (len(self.quotes)-1):
            self.quote_no = 0
        else:
            self.quote_no += 1
        self.quotes_label.configure(text=f"“{self.quotes[self.quote_no]['text']}”")
        self.quotes_author_label.configure(text=f"“{self.quotes[self.quote_no]['author']}”")
        
    def load_quotes_frame(self):
        self.quotes_frame = ctk.CTkFrame(master=self.home, fg_color="gray4", corner_radius=22)
        self.quotes_frame.grid(row=0, column=0, padx=0, pady=(5,0), sticky="nsew", columnspan=8)
        self.quotes_frame.grid_columnconfigure((0,1), weight=1)
        self.quotes_frame.grid_rowconfigure(0, weight=1)


    def load_quotes_label(self):
        self.quotes_label = ctk.CTkLabel(self.quotes_frame, text=f"“{textwrap.fill(self.quotes[self.quote_no]['text'], width=45)}”", font=LOBSTERTWO(size=26, weight="bold"), fg_color="transparent", wraplength=780, justify="center")
        self.quotes_label.grid(row=0, column=0, pady=(60,5), padx=20, sticky="nsew", columnspan=2)
        self.quotes_author_label = ctk.CTkLabel(self.quotes_frame, text=f"{self.quotes[self.quote_no]['author']}", font=LOBSTERTWO(size=20, weight="normal"), fg_color="transparent")
        self.quotes_author_label.grid(row=1, column=0, pady=(0,0), padx=120, columnspan=8, sticky="nsew")
        
        self.change_quote_btn = CursorButton(self.quotes_frame, text="Refresh Quotes", image=RELOAD_IMG, command=self.change_quote_event, font=LOBSTERTWO(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE,height=30)
        self.change_quote_btn.grid(row=2, column=0, pady=(40,40), padx=120, columnspan=2)
        
        
    def load_home_selector(self):
        self.home_projectselector = ctk.CTkOptionMenu(self.home, fg_color="black", button_color="gray12", dropdown_hover_color="gray13", corner_radius=8, font=LOBSTER(), dropdown_font=LOBSTER(), dynamic_resizing=False, anchor="w")
        self.home_projectselector.grid(row=3, column=0, pady=(20,0), padx=(30,0), sticky="ew", columnspan=2)
        self.home_projectselector_dropdown = CTkScrollableDropdown(self.home_projectselector, alpha=0.9, justify="left", command=self.projectselector_event)
        
        self.home_listselector = ctk.CTkOptionMenu(self.home, fg_color="black", button_color="gray12", dropdown_hover_color="gray13", corner_radius=8, font=LOBSTER(), dropdown_font=LOBSTER(), dynamic_resizing=False, anchor="w")
        self.home_listselector.grid(row=3, column=2, pady=(20,0), padx=(10,0), sticky="ew", columnspan=2)
        self.home_listselector_dropdown = CTkScrollableDropdown(self.home_listselector, alpha=0.9, justify="left")
        
        self.load_home_selector_dropdown()
        
    def load_home_selector_dropdown(self):
        ####### Project #######
        projectvalues = self.db.get_total_projects()
        if projectvalues == []:
            projectvalues.append("Default Project")
            
        defaultproject = projectvalues[0]
        
        self.home_projectselector.set(defaultproject)
        self.home_projectselector_dropdown.configure(values=projectvalues)
        
        ####### List #######
        dbget = self.db.search_todo_by_project(defaultproject)
        listvalues = []
        for x in dbget:
            if not x['list'] in listvalues:
                listvalues.append(x['list'])
        
        defaultlist = listvalues[0]
        
        self.home_listselector.set(defaultlist)
        self.home_listselector_dropdown.configure(values=listvalues)
        
        
    def load_home_entry(self):
        self.entry_todo = ctk.CTkEntry(self.home, placeholder_text="What are you planning to complete today? Start grinding champ!", font=LOBSTER(size=18, weight="normal"), corner_radius=50, height=60)
        self.entry_todo.grid(row=4, column=0, pady=(20,5), padx=(20,0),  sticky="ew", columnspan=7)
        
        ADD_IMG.configure(size=(50,50))
        self.add_todo_button = ctk.CTkButton(self.home, text="", image=ADD_IMG, command=self.add_todo_event, font=LOBSTER(size=40, weight="normal"), corner_radius=100, fg_color="transparent", width=3, hover=False)
        self.add_todo_button.grid(row=4, column=0, pady=(20,0), padx=(10,20), columnspan=8, sticky="e")
        self.add_todo_button.bind("<Enter>", self.hover_cursor_on)
        self.add_todo_button.bind("<Leave>", self.hover_cursor_off)
        

    def load_progressbar(self):
        self.progressbar = HomeProgressBar(self.home, self.master, self.db)
    
    def hover_cursor_on(self, event):
        event.widget.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        event.widget.configure(cursor="")
    
    @async_handler
    async def add_todo_event(self):
        event = self.entry_todo.get()
        if not event.strip():
            return
        today = datetime.date.today()
        project = self.home_projectselector.get()
        mylist = self.home_listselector.get()
        db_return = self.db.add_todo(event, mylist, project, False, "HIGH", today.day, today.month, today.year)
        self.progressbar.update()
        
        self.master.todo.search_projectframe(project).search_listframe(mylist).create_todo(self.db.search_todo_by_id(db_return))
        self.master.todo.project_sidepanels[project] = EditSidepanel(self.master, self.master.todo, self.db, 1.04, 0.7, project)
            
        showsuccess("The task has been added to your To-Do List.\nGo to To-Do Tab to view more!")
        self.entry_todo.delete(0, "end")
        self.master.levelsound.play()
        
        
    def projectselector_event(self, choice):
        db = self.db.search_todo_by_project(choice)
        if db != []:
            values = []
            for x in db:
                if not x['list'] in values:
                    values.append(x['list'])
            self.home_listselector_dropdown.configure(values=values)
            self.home_listselector.set(db[0]['list'])
            self.home_projectselector.set(choice)
    
        
        
        
############################################### TO-DOTAB ###############################################



class ToDoTab():
    def __init__(self, master, parent_tabview):
        self.master = master
        self.db = self.master.db
        
        self.todo = parent_tabview
        
        self.todo.grid_columnconfigure((0),weight=1)
        self.todo.grid_rowconfigure((0),weight=1)

        self.todoxyframe = ctk.CTkScrollableFrame(self.todo, fg_color="transparent")
        self.todoxyframe.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.todoxyframe.grid_rowconfigure((0,1),weight=1)
        self.todoxyframe.grid(column=0, row=0, sticky="nsew")
        self.scrollable_checkbox_frame = None
        self.project_rows = 0
        self.project_columns = 0
        self.project_sidepanels = {}
        self.project_main_frame_list = []
        self.project_frame_list = []
        
        self.load_project_frames()
        self.load_sidepanels()
        
        
    def get_projects(self):
        projects = self.db.get_total_tasks()
        totals = []
        for project in projects:
            if project['project'] not in totals:
                totals.append(project['project'])
        return totals
        
    def search_projectframe(self, project):
        for x in self.project_frame_list:
            if x.projectname == project:
                return x
        return False
                
            
            
    def load_sidepanels(self):
        create_sidepanel = CreateSidepanel(self.master, self, self.db, 1.04, 0.7)
        create_floating_button = CursorButton(self.todo, text="+", fg_color="gray4", width=60, font=LOBSTER(size=30), height=60, border_width=2, border_color="gray20", hover_color="gray20", corner_radius=15, command=create_sidepanel.animate)
        create_floating_button.place(relx=1, rely=1, anchor="se")
        self.current_sidepanel = None
        
        
    def delete_project_frame(self, frame, project):
        if len(self.db.get_total_projects()) <= 1:
            c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="There must be at least 1 Project. Edit this project or create a new one!", sound=True, option_1="Oh shit!")
            c.get()
            return
        dialog = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="Hey hey! Do you really wish to delete the project?", sound=True, option_1="Nevermind!", option_2="Delete")
        inp = dialog.get()
        if inp:
            if inp.lower() == 'delete':
                main_frame_index = self.project_main_frame_list.index(frame)
                previous_frame = None
                next_frame = None
                if not main_frame_index == 0:
                    previous_frame = self.project_main_frame_list[main_frame_index - 1]
                if not main_frame_index == len(self.project_main_frame_list) - 1:
                    next_frame = self.project_main_frame_list[main_frame_index + 1]
                info = frame.grid_info()
                frame.grid_forget()
                if info['column'] == 0:
                    if next_frame != None:
                        if info['columnspan'] == 4:
                            next_frame.grid_forget()
                            next_frame.grid(row=info['row'], column=0, padx=10, pady=(10,0), sticky="nsew", columnspan=8)
                        else:
                            for fr in self.project_main_frame_list:
                                frinfo = fr.grid_info()
                                if self.project_main_frame_list.index(fr) > main_frame_index:
                                    fr.grid_forget()
                                    fr.grid(row=frinfo['row']-1, column=frinfo['column'], padx=10, pady=(10,0), sticky="nsew", columnspan=frinfo['columnspan'])
                elif info['column'] == 4:
                    if previous_frame != None:
                        previous_frame.grid_forget()
                        previous_frame.grid(row=info['row'], column=0, padx=10, pady=(10,0), sticky="nsew", columnspan=8)
                self.db.delete_project(project)
                self.project_main_frame_list.remove(frame)
                c = showsuccess("The project has been successfully deleted!")
                c.get()
                self.master.home.load_home_selector_dropdown()
        
        
    def delete_list_frame(self, frame, mylist_list, projectname):
        main_frame_index = mylist_list.index(frame)
        previous_frame = None
        next_frame = None
        if not main_frame_index == 0:
            previous_frame = mylist_list[main_frame_index - 1]
        if not main_frame_index == len(mylist_list) - 1:
            next_frame = mylist_list[main_frame_index + 1]
        info = frame.grid_info()
        
        frame.grid_forget()
        if info['column'] == 0:
            if next_frame != None:
                if info['columnspan'] == 4:
                    next_frame.grid_forget()
                    next_frame.grid(row=info['row'], column=0, padx=10, pady=10, sticky="ew", columnspan=8)
                else:
                    for fr in mylist_list:
                        frinfo = fr.grid_info()
                        if mylist_list.index(fr) > main_frame_index:
                            fr.grid_forget()
                            fr.grid(row=frinfo['row']-1, column=frinfo['column'], padx=10, pady=10, sticky="ew", columnspan=frinfo['columnspan'])
        elif info['column'] == 4:
            if previous_frame != None:
                previous_frame.grid_forget()
                previous_frame.grid(row=info['row'], column=0, padx=10, pady=10, sticky="ew", columnspan=8)

        self.db.delete_list(projectname, frame.listname)
        mylist_list.remove(frame)
        c = showsuccess("The List has been successfully deleted!")
        c.get()
        
        
        
class FlipClock():
    def __init__(self, master, pomodoro, time_limit):
        self.master = master
        self.pomodoro = pomodoro
        self.db = self.pomodoro.db
        time_limit = datetime.timedelta(seconds=int(time_limit))
        self.time_limit = time_limit
        self.remaining_time = time_limit

    def update_display(self):
        minutes, seconds = str(self.remaining_time.seconds // 60), str(self.remaining_time.seconds % 60)
        if len(minutes) == 1:
            minutes = "0" + minutes
        if len(seconds) == 1:
            seconds = "0" + seconds
        self.pomodoro.minutes.configure(text=f"{minutes}")
        self.pomodoro.seconds.configure(text=f"{seconds}")

    def start_timer(self):
        self.master.after(1000, self.tick)

    def tick(self):
        self.remaining_time -= datetime.timedelta(seconds=1)
        if self.remaining_time < datetime.timedelta(seconds=0):
            settings = self.db.get_pomodoro_settings()
            if not settings['automatic']:
                self.db.add_pomodoro()
                self.pomodoro.pomodoro_count_label.configure(text=f"{self.db.get_today_pomodoros()} pomodoros completed today")
                self.pomodoro.current_state = next(self.pomodoro.states)
                self.pomodoro.status.configure(image=next(self.pomodoro.statuses))
                self.pomodoro.pomodoro_completed = True
                self.pomodoro.pomodoro_playing = False
                
                if settings["notifications"]:
                    notify("Pomodoro Completed", f"Well Done. Keep grinding!")
        else:
            self.update_display()
            self.start_timer()
            
            
            
############################################### STATSTAB ###############################################



class StatsTab():
    def __init__(self, master, parent_tabview):
        self.master = master
        self.db = self.master.db
        
        self.stats = parent_tabview
        
        self.stats.grid_columnconfigure((0,1,2,3),weight=1)
        self.stats.grid_rowconfigure((0,1,2,3),weight=1)
        self.load_progressbar()
        self.load_calendar()
            
    def load_progressbar(self):
        meterframe = ctk.CTkFrame(self.stats, fg_color=NAVY_BLUE, corner_radius=30)
        meterframe.grid_columnconfigure((0,1,2,3), weight=1)
        # meterframe.grid_propagate(False)
        meterframe.grid(row=1, column=2, pady=(20,5), padx=5, columnspan=2, sticky="nsew")
        meter = CTkMeter(meterframe, refresh_animation=True, hover_effect=True, padding=5, background=NAVY_BLUE,
                foreground=WHITE, troughcolor='#b6b6de', font='Lobster 16 bold',
                indicatorcolor=THEME_BLUE, command=lambda: print('ok'))
        meter.grid(row=0, column=0, pady=5, sticky="nsew", columnspan=1)
        meter.set(160)  # Value must be between 0 and 360
        meter.textvariable.set(f'{int((meter.arcvariable.get() / 360) * 100)}%',)
        
        ctk.CTkLabel(meterframe, text="Total Tasks", font=LOBSTER(18)).grid(row=0, column=1, columnspan=2, sticky="nsew")
        
        meterframe2 = ctk.CTkFrame(self.stats, fg_color=NAVY_BLUE, corner_radius=30)
        # meterframe.grid_propagate(False)
        meterframe2.grid(row=2, column=2, pady=(5,5), padx=5, columnspan=2, sticky="nsew")
        meter2 = CTkMeter(meterframe2, refresh_animation=True, hover_effect=True, padding=5, background=NAVY_BLUE,
                foreground=WHITE, troughcolor='#b6b6de', font='Lobster 16 bold',
                indicatorcolor=THEME_BLUE, command=lambda: print('ok'))
        meter2.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        meter2.set(214)  # Value must be between 0 and 360

        meter2.textvariable.set(f'{int((meter2.arcvariable.get() / 360) * 100)}%') 
        
        meterframe3 = ctk.CTkFrame(self.stats, fg_color=NAVY_BLUE, corner_radius=30)
        # meterframe.grid_propagate(False)
        meterframe3.grid(row=3, column=2, pady=(5,5), padx=5, columnspan=2, sticky="nsew")
        meter3 = CTkMeter(meterframe3, refresh_animation=True, hover_effect=True, padding=5, background=NAVY_BLUE,
                foreground=WHITE, troughcolor='#b6b6de', font='Lobster 16 bold',
                indicatorcolor=THEME_BLUE, command=lambda: print('ok'))
        meter3.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        meter3.set(90)  # Value must be between 0 and 360

        meter3.textvariable.set(f'{int((meter3.arcvariable.get() / 360) * 100)}%') 
        
            
            
        
class CreateSidepanel(Sidepanel):
    def __init__(self, master, todo, db, start_pos, end_pos):
        super().__init__(master, todo, db, start_pos, end_pos, "CREATE A NEW WORKSPACE")

        self.master = master
        self.db = db
        self.todo = todo

        self.load_createproject_frame()
        self.load_buttons(self.create_project_event, 30)

    def load_createproject_frame(self):
        self.createproject_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.createproject_frame.grid_columnconfigure((0,1,2,3),weight=1)
        self.createproject_frame.grid(column=0, row=0, sticky="nsew", columnspan=4, padx=10, pady=5)
        ctk.CTkLabel(self.createproject_frame, text="- There must be at least one List and a Task inside it\nto create a new project.\n- To create a List in an existing project,\nenter the exact project title.\n- To create a Task,\nenter the exact Project and List titles.", font=LOBSTER(16, 'normal'), justify="left").grid(column=0, row=0, sticky="w", padx=20, pady=(10,20), columnspan=4)
        
        ttk.Separator(self.createproject_frame).grid(column=0, row=1, columnspan=4, sticky="ew")
        
        ctk.CTkLabel(self.createproject_frame, text="New/Existing Project Title:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=2, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=4)
        self.createproject_frame_projectentry = ctk.CTkEntry(self.createproject_frame, placeholder_text="Social Media Detox", font=LOBSTER(size=16, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.createproject_frame_projectentry.grid(column=0, row=3, sticky="ew", padx=5, pady=(5,0), columnspan=4)
        
        ctk.CTkLabel(self.createproject_frame, text="New/Existing List Title:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=4, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=4)
        self.createproject_frame_listentry = ctk.CTkEntry(self.createproject_frame, placeholder_text="No Instagram", font=LOBSTER(size=16, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.createproject_frame_listentry.grid(column=0, row=5, sticky="ew", padx=5, pady=(5,0), columnspan=4)
        
        ctk.CTkLabel(self.createproject_frame, text="New To-Do Title:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=6, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=4)
        self.createproject_frame_taskentry = ctk.CTkEntry(self.createproject_frame, placeholder_text="Day 1", font=LOBSTER(size=16, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.createproject_frame_taskentry.grid(column=0, row=7, sticky="ew", padx=5, pady=(5,0), columnspan=4)
        
    
    def create_project_event(self):
        project = self.createproject_frame_projectentry.get()
        mylist = self.createproject_frame_listentry.get()
        task = self.createproject_frame_taskentry.get()
        
        for i in [project, mylist, task]:
            if not i.strip():
                return
        today = datetime.date.today()
        db_return = self.db.add_todo(task, mylist, project, False, "HIGH", today.day, today.month, today.year)
        
        existing_projectframe = self.todo.search_projectframe(project)
        if existing_projectframe:
            existing_listframe = existing_projectframe.search_listframe(mylist)
            if existing_listframe:
                existing_listframe.create_todo(self.db.search_todo_by_id(db_return))
            else:
                if existing_projectframe.columns == 8:
                    existing_projectframe.rows += 1
                    existing_projectframe.columns = 0
                if existing_projectframe.mylist_list[-1].todocolumnspan == "small":
                    todo_frame = ToDoFrame(self.master, existing_projectframe, self.db, mylist, project, projectcolumnspan=existing_projectframe.columnspan, todocolumnspan="big")
                    todo_frame.grid(row=existing_projectframe.rows, column=existing_projectframe.columns, padx=10, pady=10, sticky="ew", columnspan=8)
                else:
                    existing_projectframe.mylist_list[-1].grid_forget()
                    existing_projectframe.mylist_list[-1].grid(row=existing_projectframe.rows, column=0, padx=10, pady=10, sticky="ew", columnspan=4)
                    todo_frame = ToDoFrame(self.master, existing_projectframe, self.db, mylist, project, projectcolumnspan=existing_projectframe.columnspan, todocolumnspan="small")
                    todo_frame.grid(row=existing_projectframe.rows, column=existing_projectframe.columns, padx=10, pady=10, sticky="ew", columnspan=4)
                existing_projectframe.columns += 4
                existing_projectframe.mylist_list.append(todo_frame)
        else:
            last_project_main_frame = self.todo.project_main_frame_list[-1]
            project_main_frame = ctk.CTkFrame(self.master.todo.todoxyframe, fg_color="transparent")
            project_main_frame.grid_columnconfigure((0,1,2,3),weight=1)
            project_edit_button = CursorButton(project_main_frame, text=f"Edit", image=EDIT_IMG, font=LOBSTER(size=14), corner_radius=8, border_color=THEME_LIGHT_BLUE, border_width=2,fg_color=THEME_BLUE, hover_color=THEME_LIGHT_BLUE, command=lambda p=project: self.master.toggle_edit_sidepanel(p))
            project_delete_button = CursorButton(project_main_frame, text=f"Delete", image=DELETE_IMG, font=LOBSTER(size=14), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED, hover_color=RED, command=lambda p=project_main_frame, n=project: self.todo.delete_project_frame(p, n))
            
            if self.master.todo.project_columns == 8:
                self.master.todo.project_rows += 1
                self.master.todo.project_columns = 0
                    
            if self.master.todo.project_frame_list[-1].columnspan == "big":
                last_project_main_frame.grid_forget()
                last_project_main_frame.grid(row=self.master.todo.project_rows, column=0, padx=10, pady=(10,0), sticky="nsew", columnspan=4)
                project_main_frame.grid(row=self.master.todo.project_rows, column=4, padx=10, pady=(10,0), sticky="nsew", columnspan=4)
                
                project_frame = ProjectFrame(self, project_main_frame, self.db, project, "small")
                project_edit_button.grid(row=1, column=0, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
                project_delete_button.grid(row=1, column=2, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
            else:
                project_main_frame.grid(row=self.master.todo.project_rows, column=0, padx=10, pady=(10,0), sticky="nsew", columnspan=8)
                project_frame = ProjectFrame(self, project_main_frame, self.db, project, "big")
            self.master.todo.project_columns += 4
                
            project_edit_button.grid(row=1, column=0, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
            project_delete_button.grid(row=1, column=2, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
            
            project_frame.grid(column=0, row=0, columnspan=4, sticky="nsew")
            self.todo.project_main_frame_list.append(project_main_frame)
            self.master.todo.project_frame_list.append(project_frame)

        showsuccess("The task has been added to your To-Do List!")
        self.clear_entries([self.createproject_frame_projectentry, self.createproject_frame_listentry, self.createproject_frame_taskentry])
        self.master.levelsound.play()
        self.animate()

        self.master.home.progressbar.update()
        self.master.home.load_home_selector_dropdown()
        if project in self.todo.project_sidepanels:
            del self.todo.project_sidepanels[project]
        self.todo.project_sidepanels[project] = EditSidepanel(self.master, self.todo, self.db, 1.04, 0.7, project)
        self.master.after(500, self.todo.project_sidepanels[project].load_editproject_frame)
        
        
        
class EditSidepanel(Sidepanel):
    def __init__(self, master, todo, db, start_pos, end_pos, projectname):
        super().__init__(master, todo, db, start_pos, end_pos, f"EDIT {projectname}")
        
        self.master = master
        self.todo = todo
        self.projectname = projectname
        self.removed_tasks = {}
        self.removed_lists = []
        self.editproject_frame_listentries = {}
        self.projectframe = self.todo.search_projectframe(self.projectname)
        self.all_entries = []
        self.permanently_removed = []
        self.components = {}
        self.load_buttons(self.edit_project_event, 30, "up")
        
    def load_editproject_frame(self):
        self.editproject_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.editproject_frame.grid(column=0, row=1, sticky="nsew", columnspan=4, padx=10, pady=5)
        self.editproject_frame.grid_columnconfigure((0,1,2,3), weight=1)
        ctk.CTkLabel(self.editproject_frame, text="- Rename Project and its list(s).\n- Leave the textbox empty for no changes.", font=LOBSTER(16, 'normal'), justify="left").grid(column=0, row=0, sticky="w", padx=20, pady=(0,15), columnspan=4)
        
        ttk.Separator(self.editproject_frame).grid(column=0, row=1, columnspan=4, sticky="ew")
        
        ctk.CTkLabel(self.editproject_frame, text="Rename Project:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=2, sticky="nsew", padx=(5,0), pady=(15,5), columnspan=4)
        self.editproject_frame_projectentry = ctk.CTkEntry(self.editproject_frame, placeholder_text=f"{self.projectname}", font=LOBSTER(size=16, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.editproject_frame_projectentry.grid(column=0, row=3, sticky="ew", padx=(5,5), pady=(5,20), columnspan=4)
        
        self.all_entries.append(self.editproject_frame_projectentry)
        sep = ttk.Separator(self.editproject_frame).grid(column=0, row=4, columnspan=4, sticky="ew")
        
        j = 5
        
        mylists = self.projectframe.mylist_list
        
        for i, mylist in enumerate(mylists):
            self.components[mylist.listname] = []
            
            label = ctk.CTkLabel(self.editproject_frame, text=f"{SUB}{mylist.listname}:", font=LOBSTER(18))
            label.grid(column=0, row=j, sticky="nsw", padx=(5,0), pady=(15,5), columnspan=4)
            
            btn = ctk.CTkButton(self.editproject_frame, command=lambda l=mylist, lab=label: self.temp_remove_list(l, lab), text=f"", image=DELETE_IMG, font=LOBSTER(size=16), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED,   hover_color=RED, width=5)
            btn.grid(column=0, row=j, sticky="e", padx=(10,0), pady=(5,5), columnspan=4)
            
            editproject_frame_listentry = ctk.CTkEntry(self.editproject_frame, placeholder_text=f"A cool new name for the list...", font=LOBSTER(size=16, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
            editproject_frame_listentry.grid(column=0, row=j+1, sticky="ew", padx=(5,5), pady=(5,5), columnspan=4)
            
            self.all_entries.append(editproject_frame_listentry)
            self.editproject_frame_listentries[mylist.listname] = editproject_frame_listentry
            j += 2
            values = self.db.search_todo_by_list(mylist.listname, self.projectname)
            
            for val in values:
                seclabel = ctk.CTkLabel(self.editproject_frame, text=f"{SUBSUB}{textwrap.fill(val['task_name'],30)}", font=LOBSTER(16, "bold"), justify="left", anchor="w")
                seclabel.grid(column=0, row=j, sticky="nsew", padx=(5,10), pady=(5,5), columnspan=4)
                secbtn = ctk.CTkButton(self.editproject_frame, command=lambda t=val['id'], l=seclabel, m=mylist: self.temp_remove_task(t, l, m), text=f"{CROSS}", font=LOBSTER(size=16), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED,   hover_color=RED, width=5)
                secbtn.grid(column=0, row=j, sticky="e", padx=(10,0), pady=(5,5), columnspan=4)
                
                self.components[mylist.listname].extend([seclabel, secbtn])
                 
                j += 1
            if not i == len(mylists) - 1:
                secsep = ttk.Separator(self.editproject_frame)
                secsep.grid(column=0, row=j, columnspan=4, sticky="ew", pady=(10,5))
                self.components[mylist.listname].append(secsep)
                j+=1
                
            self.components[mylist.listname].extend([label, btn, editproject_frame_listentry])
        
    def temp_remove_task(self, task, label, mylist):
        if len(mylist.checkboxes) <= 1:
            c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="There must be at least 1 Task in each List.", sound=True, option_1="Oh shit!")
            c.get()
            return
        if task in self.permanently_removed:
            return
        if not task in self.removed_tasks:
            label.cget("font").configure(overstrike=True)
            self.removed_tasks[task] = mylist
            self.master.levelsound.play()
        else:
            label.cget("font").configure(overstrike=False)
            del self.removed_tasks[task]
        
    def temp_remove_list(self, mylist, label):
        if len(self.projectframe.mylist_list) <= 1:
            c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="There must be at least 1 List in each Project.", sound=True, option_1="Oh shit!")
            c.get()
            return
        if mylist in self.permanently_removed:
            return
        if not mylist in self.removed_lists:
            label.cget("font").configure(overstrike=True)
            self.removed_lists.append(mylist)
        else:
            label.cget("font").configure(overstrike=False)
            self.removed_lists.remove(mylist)
    
    def edit_project_event(self):
        renamed_project = self.editproject_frame_projectentry.get()
        
        if self.removed_lists != []:
            dialog = ctk.CTkInputDialog(text="Type 'delete' to confirm the deletion of list(s).", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'delete':
                    for i in self.removed_lists:
                        self.todo.delete_list_frame(i, self.projectframe.mylist_list, self.projectname)
                        self.permanently_removed.append(i)
                        self.delete_items(self.components[i.listname])
                    del self.components[i.listname]
                    self.removed_lists = []
                    
        if self.removed_tasks != {}:
            dialog = ctk.CTkInputDialog(text="Type 'delete' to confirm the deletion of task(s).", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'delete':
                    for i in self.removed_tasks:
                        if self.db.check_todo_by_id(i):
                            self.db.delete_todo(i)
                            for j in self.removed_tasks[i].checkboxes:
                                if j.task_id == i:
                                    j.grid_forget()
                                    self.removed_tasks[i].checkboxes.remove(j)
                        self.permanently_removed.append(i)
                    self.removed_tasks = {}
                    c = showsuccess("The task(s) were removed from your To-Do List!")
                    c.get()

        list_updated_boolean = False
        for i in self.editproject_frame_listentries:
            if self.editproject_frame_listentries[i].get().strip():
                list_updated_boolean = True
                get = self.editproject_frame_listentries[i].get()
                self.db.update_list_name(self.projectname, i, get)
                self.editproject_frame_listentries[i].configure(placeholder_text=get)
                self.projectframe.search_listframe(i).configure(label_text=f"⇲ {get}")
        if list_updated_boolean:
            showsuccess("Congrats! Your List(s) were successfully renamed!", "Sounds cool!")
                
        if renamed_project.strip():
            self.db.update_project_name(self.projectname, renamed_project)
            self.projectframe.configure(label_text=renamed_project)
            self.projectname = renamed_project
            self.editproject_frame_projectentry.configure(placeholder_text=renamed_project)
            showsuccess(f"Congrats! Your Project is renamed to '{renamed_project}'", "Sounds cool!")
        
        self.clear_entries(self.all_entries)
        self.master.home.progressbar.update()
        self.master.home.load_home_selector_dropdown()
        
        
    def delete_items(self, items):
        for i in items:
            try:
                i.grid_forget()
            except:
                pass
        
    

class PomodoroSidepanel(Sidepanel):
    def __init__(self, master, pomodoro, db, start_pos, end_pos):
        super().__init__(master, None, db, start_pos, end_pos, "Pomodoro Settings")

        self.master = master
        self.db = db
        self.pomodoro = pomodoro
        self.pomodorosettings = self.db.get_pomodoro_settings()

        self.load_pomodoro_settings_frame()
        self.load_buttons(self.save_pomodoro_settings, 60)

    def load_pomodoro_settings_frame(self):
        settings = self.pomodorosettings
        self.pomodoro_settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pomodoro_settings_frame.grid_columnconfigure((0,1,2,3),weight=1)
        self.pomodoro_settings_frame.grid(column=0, row=0, sticky="nsew", columnspan=4, padx=10, pady=5)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Pomodoro Length:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=2, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.focus_length_entry = SpinBox(self.pomodoro_settings_frame, start_value=settings['focuslength'], min_value=5, max_value=59, scroll_value=1, variable=self.pomodoro.set_focus_length, font=UBUNTU(size=16), corner_radius=10, height=30)
        self.focus_length_entry.grid(column=3, row=2, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Short Break Length:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=3, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.shortbreak_length_entry = SpinBox(self.pomodoro_settings_frame, start_value=settings['shortbreaklength'], min_value=2, max_value=30, scroll_value=1, variable=self.pomodoro.set_shortbreak_length, font=UBUNTU(size=16), corner_radius=10, height=30)
        self.shortbreak_length_entry.grid(column=3, row=3, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Long Break Length:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=4, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.longbreak_length_entry = SpinBox(self.pomodoro_settings_frame, start_value=settings['longbreaklength'], min_value=5, max_value=45, scroll_value=1, variable=self.pomodoro.set_longbreak_length, font=UBUNTU(size=16), corner_radius=10, height=30)
        self.longbreak_length_entry.grid(column=3, row=4, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Pomodoros Until Short Break:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=5, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.pomodoros_until_shortbreak_entry = SpinBox(self.pomodoro_settings_frame, start_value=settings['pomodorosuntilshortbreak'], min_value=2, max_value=8, scroll_value=1, variable=self.pomodoro.set_pomodoros_until_shortbreak, font=UBUNTU(size=16), corner_radius=10, height=30)
        self.pomodoros_until_shortbreak_entry.grid(column=3, row=5, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Pomodoros Until Long Break:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=6, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.pomodoros_until_longbreak_entry = SpinBox(self.pomodoro_settings_frame, start_value=settings['pomodorosuntillongbreak'], min_value=4, max_value=16, scroll_value=1, variable=self.pomodoro.set_pomodoros_until_longbreak, font=UBUNTU(size=16), corner_radius=10, height=30)
        self.pomodoros_until_longbreak_entry.grid(column=3, row=6, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Automatic Pomodoro/breaks:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=7, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.automatic = ctk.CTkSwitch(self.pomodoro_settings_frame, text="", onvalue="on", offvalue="off", variable=self.pomodoro.set_automatic, switch_height=15, switch_width=40, font=UBUNTU(size=16))
        if settings['automatic']:
            self.automatic.select()
        self.automatic.grid(column=3, row=7, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
        ctk.CTkLabel(self.pomodoro_settings_frame, text="Progress Notifications:", font=LOBSTER(18), justify="left", anchor="w").grid(column=0, row=8, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=3)
        self.notifications = ctk.CTkSwitch(self.pomodoro_settings_frame, text="", onvalue="on", offvalue="off", variable=self.pomodoro.set_notifications, switch_height=15, switch_width=40, font=UBUNTU(size=16))
        if settings['notifications']:
            self.notifications.select()
        self.notifications.grid(column=3, row=8, sticky="nse", padx=(5,5), pady=(20,5), columnspan=1)
        
    def save_pomodoro_settings(self):
        if not self.pomodoro.pomodoro_completed:
            showerror("Pomodoro is running! Complete the current pomodoro then change the settings.")
            return
        if self.shortbreak_length_entry.get() > self.longbreak_length_entry.get():
            showerror("Long Break length should be more than Short Break length.")
            return
        if self.pomodoros_until_shortbreak_entry.get() > self.pomodoros_until_longbreak_entry.get():
            showerror("Required Pomodoros for Long Break should be more than that for Short Break")
            return
        self.db.update_pomodoro_settings(self.focus_length_entry.get(), self.shortbreak_length_entry.get(), self.longbreak_length_entry.get(), self.pomodoros_until_shortbreak_entry.get(), self.pomodoros_until_longbreak_entry.get(), self.pomodoro.set_automatic.get(), self.pomodoro.set_notifications.get())
        showsuccess("Pomodoro settings have been successfully applied!")



############################################### TO-DO FRAME ###############################################



class ToDoFrame(ctk.CTkScrollableFrame):
    def __init__(self, root, master, db, listname="MY TO-DO LIST", projectname="Default Project", projectcolumnspan="big", todocolumnspan="big"):
        super().__init__(master, label_text=f"⇲ {listname}", label_fg_color=DULL_BLUE, border_width=1, border_color=WHITE, corner_radius=8, fg_color=NAVY_BLUE, label_font=LOBSTER(size=16))
        
        self.root = root
        self.master = master
        self.db = db
        self.checkboxes = []
        self.listname = listname
        self.projectname = projectname
        self.projectcolumnspan = projectcolumnspan
        self.todocolumnspan = todocolumnspan
        
        self.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        
        self.load_lists()

        self.click = False
        
    def load_lists(self):
        values = self.db.search_todo_by_list(self.listname, self.projectname)
        for i, val in enumerate(values):
            checkbox = ctk.CTkCheckBox(self, text=f"{self.wrap(val['task_name'])}", hover=True, onvalue="on", offvalue="off", font=LOBSTER(16, "normal"), command=self.mark_as_done_checkbox)

            if val['status']:
                checkbox.cget("font").configure(overstrike=True, slant="italic")
                checkbox.select()
            
            checkbox.task_id = val['id']
            checkbox.grid(row=i, column=0, padx=5, pady=5, sticky="ew", columnspan=8)
            self.checkboxes.append(checkbox)
        
    def create_todo(self, val):
        checkbox = ctk.CTkCheckBox(self, text=f"{self.wrap(val['task_name'])}", hover=True, onvalue="on", offvalue="off", font=LOBSTER(16, "normal"), command=self.mark_as_done_checkbox)
        checkbox.task_id = val['id']
        checkbox.grid(row=len(self.checkboxes)+1, column=0, padx=5, pady=5, sticky="ew", columnspan=8)
        self.checkboxes.append(checkbox)
    
    def mark_as_done_checkbox(self):
        for checkbox in self.winfo_children():
            if checkbox.get() == "on" and checkbox.cget("font").cget("overstrike") == False:
                checkbox.cget("font").configure(overstrike=True, slant="italic")
                self.db.update_todo_status(checkbox.task_id, True)
                self.root.home.progressbar.update()
            elif checkbox.get() == "off" and checkbox.cget("font").cget("overstrike") == True:
                checkbox.cget("font").configure(overstrike=False, slant="roman")
                self.db.update_todo_status(checkbox.task_id, False)
                self.root.home.progressbar.update()
                
    def wrap(self, text):
        if self.projectcolumnspan == "big":
            if self.todocolumnspan == "big":
                width = 85
            else:
                width = 32
        else:
            if self.todocolumnspan == "big":
                width = 32
            else:
                width = 15
            
        return textwrap.fill(text, width=width)
    
    

############################################### PYGAME MUSIC ###############################################    
    
    
    
class Music():
    def __init__(self, master, music_switch_img):
        self.master = master
        self.music = pygame.mixer
        self.music.init()
        self.paused = False
        self.master.trumpetsound = self.music.Sound(resource_path(resource_path('sounds/trumpets.mp3')))
        self.master.trumpetsound.set_volume(0.1)
        self.master.levelsound = self.music.Sound(resource_path(resource_path('sounds/level.mp3')))
        self.master.levelsound.set_volume(0.1)
        self.music_switch_img = music_switch_img
        
        
    def music_switch_event(self):
        if not hasattr(self, "music_switch_var"):
            self.music_switch_var = True
            self.music_switch_img.configure(dark_image=Image.open(resource_path("images/Configuration/switch-on.png")))
            self.play()
            return
        if self.music_switch_var:
            self.music_switch_var = False
            self.music_switch_img.configure(dark_image=Image.open(resource_path("images/Configuration/switch-off.png")))
            self.paused = True
            self.music.music.pause()
            return
        if not self.music_switch_var:
            self.music_switch_var = True
            self.music_switch_img.configure(dark_image=Image.open(resource_path("images/Configuration/switch-on.png")))
            self.play()
            return
            
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
                showerror("Select a valid format to play music (mp3/ogg/wav).", "Okay")
                self.music_switch_img.configure(dark_image=Image.open(resource_path("images/Configuration/switch-off.png")))
                del self.music_switch_var
        else:
            self.music.music.unpause()
            
            
            
############################################### CTkButton Frame ###############################################



class CursorButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.bind("<Enter>", self.hover_cursor_on)
        self.bind("<Leave>", self.hover_cursor_off)

    def hover_cursor_on(self, event):
        event.widget.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        event.widget.configure(cursor="")
        


############################################### ImageButton ###############################################



class ImageButton(ctk.CTkButton):
    def __init__(self, master, image_path, command, image_height=50, image_width=50, **kwargs):
        super().__init__(master, **kwargs)
        self.image = ctk.CTkImage(dark_image=Image.open(image_path), size=(image_width, image_height))
        self.button = ctk.CTkButton(self.master, text="", image=self.image, command=command, font=LOBSTER(size=40, weight="normal"), corner_radius=20, fg_color="transparent", width=3, hover=False)



############################################### SpinBox ###############################################



class SpinBox(CTkSpinbox.CTkSpinbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=1, border_color="gray20", button_color="transparent", button_hover_color="gray6", button_border_width=1, button_border_color="gray8", **kwargs)
        
        
        
############################################### KEYBINDS ###############################################


    
app = App()

    
def enter(event):
    if app.mainframe.tab_view.get() == 'HOME':
        app.home.add_todo_event()
    if app.mainframe.tab_view.get() == 'SESSIONS':
        app.sessions.add_own_message()

def ctrla(event):
    app.select_all()
    
app.bind('<Return>', enter)
app.bind('<Control-a>', ctrla)

app.protocol("WM_DELETE_WINDOW", app.close_confirmation)

if __name__=="__main__":
    print(colorama.Fore.CYAN + ASCII)
    app.async_mainloop()
