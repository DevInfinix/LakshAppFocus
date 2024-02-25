"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.0
"""

__version__="1.0.0"

import logging
from modules import AppData
logfile = AppData("lakshapp", "lakshapp-logs.txt")
logging.basicConfig(level=logging.INFO, format="[LakshApp Logs] %(asctime)s - %(levelname)s - %(message)s", filename=logfile.get_file_path())

try:
    import customtkinter as ctk
    # import tkinter
    from tkinter import filedialog
    import tkinter.ttk as ttk
    from CTkMessagebox import CTkMessagebox
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
    import colorama
    import datetime
    import asyncio
    import websockets
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
        self.withdraw()
        logging.info('LakshApp initialized...')
        self.splashapp = SplashApp(self)
        self.splashapp.attributes('-topmost', True)
        logging.info('SplashScreen initialized...')
        self.title("LakshApp - Stay Focused and Motivated")
        self.resizable(False, False)
        #self.iconbitmap('./images/lakshapp.ico')
        self.width = 1100
        self.height = 620
        place_x = (self.winfo_screenwidth()//2) - (self.width//2)
        place_y = (self.winfo_screenheight()//2) - (self.height//2)
        self.geometry(f"{self.width}x{self.height}+{place_x}+{place_y}")
        self.grid_columnconfigure((1,2,3), weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.total_message = 0
        self.role = None
        self.version = __version__
        
        
        ############################################### DATABASE ###############################################
    
        
        self.db = Database('database.db')
        self.db.create_table()
        
        
        ############################################### SIDEBAR INITIALIZE ###############################################
        
        
        self.sidebar = Sidebar(self)
        self.mainframe = MainFrame(self)
        self.stats = self.mainframe.stats
        self.sessions = self.mainframe.sessions



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


        self.sessions_progressbutton = CursorButton(self.sessions, text="Start Session", command=self.start_sessions_timer, font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE)
        self.sessions_progressbutton.grid(row=0, column=0, pady=0, padx=(10, 0), sticky="ew", columnspan=6, rowspan=1)
        
        
        self.sessions_leavebutton = CursorButton(self.sessions, text="⍇ Leave Room", command=self.leavesession, font=UBUNTU(size=15), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED, hover_color=RED)
        self.sessions_leavebutton.grid(row=0, column=0, pady=0, padx=(0, 10), sticky="e", columnspan=8, rowspan=1)
            
        
        
        self.sessions_progressbar = ctk.CTkProgressBar(self.sessions, orientation="horizontal", height=15)
        self.sessions_progressbar.set(0)
        self.sessions_progressbar.grid(row=2, column=0, pady=(0,0), padx=15, sticky="ew", columnspan=8, rowspan=1)
        
        
        if self.role == 'member':
            self.sessions_progressbutton.destroy()
            self.sessions_progressbutton = CursorButton(self.sessions, state="disabled", text="The host can start a session", font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE)
            self.sessions_progressbutton.grid(row=0, column=0, pady=0, padx=(10, 0), sticky="ew", columnspan=6, rowspan=1)
        
        
        self.sessions_frame = ctk.CTkScrollableFrame(self.sessions, corner_radius=18, fg_color="gray4")
        self.sessions_frame.grid(row=3, column=0, sticky="nsew", padx=15,pady=(10,15), columnspan=8, rowspan=3)
        self.sessions_frame.grid_columnconfigure((0,1), weight=1)
        
        self.sessions_frame.bind_all("<Button-4>", lambda e: self.sessions_frame._parent_canvas.yview("scroll", -1, "units"))
        self.sessions_frame.bind_all("<Button-5>", lambda e: self.sessions_frame._parent_canvas.yview("scroll", 1, "units"))
        
        self.send_area = ctk.CTkEntry(self.sessions, placeholder_text="Say Hello to your session partner!", font=UBUNTU(size=18, weight="normal"), corner_radius=50, height=60)
        self.send_area.grid(row=6, column=0, pady=(0,8), padx=(15,15),  sticky="sew", columnspan=7, rowspan=1)
        self.send_button = CursorButton(self.sessions, text="➤", command=self.add_own_message, font=UBUNTU(size=30, weight="normal"), corner_radius=100, fg_color="transparent", width=2, height=60, hover_color="gray4")
        self.send_button.grid(row=6, column=0, pady=(0,8), padx=(15,15), columnspan=8, sticky="se", rowspan=1)
        
        
        
############################################### SPLASH SCREEN ###############################################


        self.splashapp.destroy()
        self.deiconify()
        self.lift()
        logging.info('LakshApp is Running!')
        
            
############################################### FUNCTIONS ###############################################


        self.socket = None
    
    def hover_cursor_on(self, event):
        self.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        self.configure(cursor="")
    
        
    def select_all(self):
        if self.mainframe.tab_view.get() == 'HOME':
            self.entry_todo.select_range(0, 'end')
            self.entry_todo.icursor('end')
            return 'break'
        if self.mainframe.tab_view.get() == 'SESSIONS':
            self.send_area.select_range(0, 'end')
            self.send_area.icursor('end')
            return 'break'
        
    
    def toggle_edit_sidepanel(self, project):
        if project in self.todo.project_sidepanels:
            sidepanel = self.todo.project_sidepanels[project]
            sidepanel.animate()
    
            
    @async_handler
    async def leavesession(self):
        d = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="warning", message="Done for the day? Hope to see you soon!\n[Attention: Ending the session will result in the loss of all your progress during the session.]", sound=True, option_1="I'm done", option_2="I'm staying")
        if d.get() == "I'm done":
            await self.close_socket()
    
    
    @async_handler
    async def add_own_message(self):
        message = self.send_area.get()
        if (message == '') or (not message.strip()):
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
                self.mainframe.tab_view.set("SESSIONS")
                self.sidebar.set_current_tab(self.sessionstab)
                await asyncio.sleep(1)
                logging.info(f"Your code is: [{event['code']}]")
                pyperclip.copy(event['code'])
                self.add_other_message(user='System', message=f"Your room's code is: [{event['code']}] | The code has been copied to your clipboard.")
                self.socket = socket
            if event['type'] == 'joined':
                self.mainframe.tab_view.set("SESSIONS")
                self.sidebar.set_current_tab(self.sessionstab)
                await asyncio.sleep(1)
                logging.info(f"You joined {event['code']}")
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
                self.sessions_progressbar_task = asyncio.create_task(self.update_sessions_progressbar(time))
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
                        logging.info('The host has been disconnected')
                        CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message='The host has been disconnected', sound=True, option_1="Oh shit!")
                        await asyncio.sleep(1)
                        self.mainframe.tab_view.set("HOME")
                        self.sidebar.set_current_tab(self.sidebar.hometab)
                        self.socket = None
                        if role == 'host':
                            return
                        else:
                            break
                    elif event['role'] == 'member':
                        logging.info('Participant disconnected')
                        if role == 'member':
                            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message='You have been disconnected', sound=True, option_1="Oh Shit!")
                            await asyncio.sleep(1)
                            self.mainframe.tab_view.set("HOME")
                            self.sidebar.set_current_tab(self.sidebar.hometab)
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
    
    
    async def close_socket(self):
        try:
            await self.socket.close()
        except:
            pass
        self.socket = None
        self.set_home()
        
        
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
        
        

############################################### PROJECT FRAME ###############################################



class ProjectFrame(ctk.CTkScrollableFrame):
    def __init__(self, root, base_frame, db, projectname, columnspan):
        super().__init__(base_frame, label_text=projectname, label_fg_color="gray8", border_width=3, border_color=BLACK, corner_radius=18, fg_color="gray13", label_font=UBUNTU(size=15))
        
        self.root = root
        self.db = db
        self.projectname = projectname
        self.columnspan = columnspan
        
        self.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        
        self.columns = 0
        self.rows = 0
        
        self.mylist_list = []
        
        self.load_projects()
        
    def load_projects(self):
        projects = self.db.search_todo_by_project(self.projectname)
        totals = []
        for mylist in projects:
            if mylist['list'] not in totals:
                totals.append(mylist['list'])

        for i, mylist in enumerate(totals):
            if self.columns == 8:
                self.rows += 1
                self.columns = 0
                
            if (i == len(totals) - 1) and (len(totals) % 2 != 0):
                todo_frame = ToDoFrame(self.root, self, self.db, mylist, self.projectname, projectcolumnspan=self.columnspan, todocolumnspan="big")
                todo_frame.grid(row=self.rows, column=0, padx=10, pady=10, sticky="ew", columnspan=8)
            else:
                todo_frame = ToDoFrame(self.root, self, self.db, mylist, self.projectname, projectcolumnspan=self.columnspan, todocolumnspan="small")
                todo_frame.grid(row=self.rows, column=self.columns, padx=10, pady=10, sticky="ew", columnspan=4)
            self.columns += 4
            self.mylist_list.append(todo_frame)
    
    def search_listframe(self, mylist):
        for x in self.mylist_list:
            if x.listname == mylist:
                return x
        return False



############################################### TO-DO FRAME ###############################################



class ToDoFrame(ctk.CTkScrollableFrame):
    def __init__(self, root, master, db, listname="MY TO-DO LIST", projectname="Default Project", projectcolumnspan="big", todocolumnspan="big"):
        super().__init__(master, label_text=f"⇲ {listname}", label_fg_color=DULL_BLUE, border_width=1, border_color=WHITE, corner_radius=8, fg_color=NAVY_BLUE, label_font=UBUNTU(size=15))
        
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
            checkbox = ctk.CTkCheckBox(self, text=f"{self.wrap(val['task_name'])}", hover=True, onvalue="on", offvalue="off", font=UBUNTU(12, "normal"), command=self.mark_as_done_checkbox)

            if val['status']:
                checkbox.cget("font").configure(overstrike=True, slant="italic")
                checkbox.select()
            
            checkbox.task_id = val['id']
            checkbox.grid(row=i, column=0, padx=5, pady=5, sticky="ew", columnspan=8)
            self.checkboxes.append(checkbox)
        
    def create_todo(self, val):
        checkbox = ctk.CTkCheckBox(self, text=f"{self.wrap(val['task_name'])}", hover=True, onvalue="on", offvalue="off", font=UBUNTU(12, "normal"), command=self.mark_as_done_checkbox)
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



############################################### SIDEBAR ###############################################
        
        
        
class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=18, fg_color="gray8")
        
        self.master = master
        self.db = self.master.db
        self.grid(row=0, column=0, sticky="nsew", padx=(15,7.5),pady=15, columnspan=1)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        self.load_logo()
        self.load_tabs_buttons()
        self.load_music()
        
        self.tabsbutton = [self.hometab, self.todotab, self.statstab, self.sessionstab]
        
    def load_logo(self):
        self.logo_label = ctk.CTkLabel(self, text="LakshApp", font=UBUNTU(size=28), text_color=LIGHT_BLUE, justify="center")
        self.logo_label.grid(row=0, column=0, padx=25, pady=(100,60),columnspan=2, rowspan=1, sticky="ew")
    
    def load_tabs_buttons(self):   
        self.hometab = CursorButton(master=self, text=" Home ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_home, font=UBUNTU())
        self.hometab.grid(padx=25, pady=8, row=1, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.todotab = CursorButton(master=self, text=" To-Do ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_todo, font=UBUNTU())
        self.todotab.grid(padx=25, pady=8, row=2, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.statstab = CursorButton(master=self, text=" My Progress ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_stats, font=UBUNTU())
        self.statstab.grid(padx=25, pady=8, row=3, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.sessionstab = CursorButton(master=self, text=" Live Sessions ", hover_color=THEME_BLUE, corner_radius=20, border_color=THEME_BLUE, border_width=2,fg_color="gray13", command=self.set_sessions, font=UBUNTU())
        self.sessionstab.grid(padx=25, pady=8, row=4, column=0,columnspan=2, rowspan=1, sticky="ew")
    
    
    def load_music(self):
        self.music_switch_img = ctk.CTkImage(dark_image=Image.open(resource_path("images/Configuration/switch-off.png")))
        self.music = Music(self.master, self.music_switch_img)
        self.music_switch = ctk.CTkButton(self, text="Ambient Mode", anchor="w", image=self.music_switch_img, command=self.music.music_switch_event, fg_color="gray4", hover=False, corner_radius=20, font=UBUNTU(size=14))
        self.music_switch.grid(row=5, column=0, sticky="nsew", padx=25,pady=(8,100), columnspan=2)
        
        self.music_switch.bind("<Enter>", self.hover_cursor_on)
        self.music_switch.bind("<Leave>", self.hover_cursor_off)

    def hover_cursor_on(self, event):
        self.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        self.configure(cursor="")

    def set_current_tab(self, current_tab):
        if hasattr(self.master.todo, "current_sidepanel"):
            if self.master.todo.current_sidepanel:
                if (not self.master.todo.current_sidepanel.is_closed):
                    self.master.todo.current_sidepanel.animate_backwards()
        for tab in self.tabsbutton:
            if current_tab == tab:
                tab.configure(fg_color=THEME_BLUE)
            else:
                tab.configure(fg_color="gray13")
        
    def set_home(self):
        self.master.mainframe.tab_view.set("HOME")
        self.set_current_tab(self.hometab)
        
    def set_todo(self):
        self.master.mainframe.tab_view.set("TO-DO")
        self.set_current_tab(self.todotab)
        
    @async_handler
    async def set_stats(self):
        dates = self.db.get_total_tasks()
        if dates == []:
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="You haven't completed any tasks yet.\nStart completing now!", sound=True, option_1="Oh shit!")
        else:
            values = {}
            for val in dates:
                date_tuple = (val['day'], val['month'], val['year'])
                if date_tuple not in values:
                    values[date_tuple] = 10
            if hasattr(self.master, "calendar"):
                self.master.calendar.destroy()
            self.master.calendar = CTkCalendarStat(self.master.stats, values, border_width=0, border_color=WHITE,
                                fg_color=NAVY_BLUE, title_bar_border_width=2, title_bar_border_color="gray80",
                                title_bar_fg_color=NAVY_BLUE, calendar_fg_color=NAVY_BLUE, corner_radius=30,
                                title_bar_corner_radius=10, calendar_corner_radius=10, calendar_border_color=WHITE,
                                calendar_border_width=0, calendar_label_pad=5, data_colors=["blue", "green", RED]
                    )
            self.master.calendar.grid(row=1, column=0, pady=(60,60), padx=60, sticky="new", columnspan=2)
            self.master.mainframe.tab_view.set("STATS")
            self.set_current_tab(self.statstab)
            
        
    @async_handler
    async def set_sessions(self):
        if not self.master.socket:
            dialog = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="info", message="Select 'Start' to host a session. If you have a valid session code, select 'Join'.", sound=True, option_1="Join", option_2="Start")
            inp = dialog.get()
            if inp:
                if inp.lower() == 'start':
                    dialog2 = ctk.CTkInputDialog(text="Enter your username\nfor the live session.", title="LakshApp")
                    inp2 = dialog2.get_input()
                    if inp2:
                        if inp2 != '':
                            self.master.own_username = inp2
                            await self.master.start_server(WEBSOCKET_SERVER, inp2)
                if inp.lower() == 'join':
                    dialog2 = ctk.CTkInputDialog(text="Enter the code for the live session.", title="LakshApp")
                    inp2 = dialog2.get_input()
                    if inp2:
                        if inp2 != '':
                            self.master.server_code = inp2
                            
                            dialog3 = ctk.CTkInputDialog(text="Enter your username\nfor the live session.", title="LakshApp")
                            inp3 = dialog3.get_input()
                            if inp3:
                                if inp3 != '':
                                    self.master.own_username = inp3
                                    await self.master.join_server(WEBSOCKET_SERVER, inp2, inp3)
        else:
            self.mainframe.tab_view.set("SESSIONS")
            self.set_current_tab(self.sessionstab)
            

    
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
                CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="cancel", message="Select a valid format to play music (mp3/ogg/wav).", sound=True, option_1="Okay")
                self.music_switch_img.configure(dark_image=Image.open(resource_path("images/Configuration/switch-off.png")))
                del self.music_switch_var
        else:
            self.music.music.unpause()



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
        
        home = self.tab_view.add("HOME")
        self.master.home = HomeTab(self.master, home)
        todo = self.tab_view.add("TO-DO")
        self.master.todo = ToDoTab(self.master, todo)
        self.stats = self.tab_view.add("STATS")
        self.sessions = self.tab_view.add("SESSIONS")
        
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
        self.quotes_label = ctk.CTkLabel(self.quotes_frame, text=f"“{textwrap.fill(self.quotes[self.quote_no]['text'], width=45)}”", font=HELVETICA(weight="bold"), fg_color="transparent", wraplength=780, justify="center")
        self.quotes_label.grid(row=0, column=0, pady=(60,5), padx=20, sticky="nsew", columnspan=2)
        self.quotes_author_label = ctk.CTkLabel(self.quotes_frame, text=f"{self.quotes[self.quote_no]['author']}", font=HELVETICA(size=20, weight="normal"), fg_color="transparent")
        self.quotes_author_label.grid(row=1, column=0, pady=(0,0), padx=120, columnspan=8, sticky="nsew")
        
        self.change_quote_btn = CursorButton(self.quotes_frame, text="Refresh Quotes", image=RELOAD_IMG, command=self.change_quote_event, font=UBUNTU(size=15), corner_radius=8, border_color=THEME_BLUE, border_width=2,fg_color="gray13", hover_color=THEME_BLUE,height=30)
        self.change_quote_btn.grid(row=2, column=0, pady=(40,40), padx=120, columnspan=2)
        
        
    def load_home_selector(self):
        self.home_projectselector = ctk.CTkOptionMenu(self.home, fg_color="black", button_color="gray12", dropdown_hover_color="gray13", corner_radius=8, font=UBUNTU(), dropdown_font=UBUNTU(), dynamic_resizing=False, anchor="w")
        self.home_projectselector.grid(row=3, column=0, pady=(20,0), padx=(30,0), sticky="ew", columnspan=2)
        self.home_projectselector_dropdown = CTkScrollableDropdown(self.home_projectselector, alpha=0.9, justify="left", command=self.projectselector_event)
        
        self.home_listselector = ctk.CTkOptionMenu(self.home, fg_color="black", button_color="gray12", dropdown_hover_color="gray13", corner_radius=8, font=UBUNTU(), dropdown_font=UBUNTU(), dynamic_resizing=False, anchor="w")
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
        self.entry_todo = ctk.CTkEntry(self.home, placeholder_text="What are you planning to complete today? Start grinding champ!", font=UBUNTU(size=18, weight="normal"), corner_radius=50, height=60)
        self.entry_todo.grid(row=4, column=0, pady=(20,5), padx=(20,0),  sticky="ew", columnspan=7)
        
        ADD_IMG.configure(size=(50,50))
        self.add_todo_button = ctk.CTkButton(self.home, text="", image=ADD_IMG, command=self.add_todo_event, font=UBUNTU(size=40, weight="normal"), corner_radius=100, fg_color="transparent", width=3, hover=False)
        self.add_todo_button.grid(row=4, column=0, pady=(20,0), padx=(10,20), columnspan=8, sticky="e")
        self.add_todo_button.bind("<Enter>", self.hover_cursor_on)
        self.add_todo_button.bind("<Leave>", self.hover_cursor_off)
        

    def load_progressbar(self):
        self.progressbar = HomeProgressBar(self.home, self.master, self.db)
    
    def hover_cursor_on(self, event):
        self.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        self.configure(cursor="")
    
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
            
        CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The task has been added to your To-Do List.\nGo to To-Do Tab to view more!", sound=True, option_1="There we go!")
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
    


class HomeProgressBar(ctk.CTkProgressBar):
    def __init__(self, master, root, db):
        super().__init__(master, orientation="horizontal", height=15)
        self.master = root
        self.db = db
        self.home = master
        self.set(self.percent())
        self.grid(row=5, column=0, pady=(10,5), padx=(45,35), sticky="ew", columnspan=8)
        
        self.load_progress_label()
        
    def load_progress_label(self):
        self.progresslabel = ctk.CTkLabel(self.home, text=f"↪ Your Progress ({self.db.get_completed_tasks_count()}/{self.db.get_total_tasks_count()} completed)", font=UBUNTU(size=18, weight="normal"), justify="right")
        self.progresslabel.grid(row=6, column=0, pady=0, padx=25, sticky="e", columnspan=8)

    def percent(self):
        if self.db.get_total_tasks_count() == 0:
            return 0
        return (self.db.get_completed_tasks_count()/self.db.get_total_tasks_count())
        
    def update(self):
        comp = self.db.get_completed_tasks_count()
        tot = self.db.get_total_tasks_count()
        self.set(comp/tot)
        self.progresslabel.configure(text=f"↪ Your Progress ({comp}/{tot} completed)")
        
        
        
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
                
    def load_project_frames(self):
        totals = self.get_projects()
        for i, project in enumerate(totals):
            project_main_frame = ctk.CTkFrame(self.todoxyframe, fg_color="transparent")
            project_main_frame.grid_columnconfigure((0,1,2,3),weight=1)
            
            project_edit_button = CursorButton(project_main_frame, text=f"Edit", image=EDIT_IMG, font=UBUNTU(size=12), corner_radius=8, border_color=THEME_LIGHT_BLUE, border_width=2,fg_color=THEME_BLUE, hover_color=THEME_LIGHT_BLUE, command=lambda p=project: self.master.toggle_edit_sidepanel(p))
            project_delete_button = CursorButton(project_main_frame, text=f"Delete", image=DELETE_IMG, font=UBUNTU(size=12), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED, hover_color=RED, command=lambda p=project_main_frame, n=project: self.delete_project_frame(p, n))
            
            if self.project_columns == 8:
                self.project_rows += 1
                self.project_columns = 0
                
            if (i == len(totals) - 1) and (len(totals) % 2 != 0):
                project_main_frame.grid(row=self.project_rows, column=self.project_columns, padx=10, pady=(10,0), sticky="nsew", columnspan=8)
                
                project_frame = ProjectFrame(self.master, project_main_frame, self.db, project, "big")
                project_frame.grid(column=0, row=0, columnspan=4, sticky="nsew")
                project_edit_button.grid(row=1, column=0, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
                project_delete_button.grid(row=1, column=2, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
            else:
                project_main_frame.grid(row=self.project_rows, column=self.project_columns, padx=10, pady=(10,0), sticky="nsew", columnspan=4)
                
                project_frame = ProjectFrame(self.master, project_main_frame, self.db, project, "small")
                project_frame.grid(column=0, row=0, columnspan=4, sticky="nsew")
                project_edit_button.grid(row=1, column=0, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
                project_delete_button.grid(row=1, column=2, pady=(10, 50), padx=5, sticky="sew", columnspan=2)
                
            self.project_columns += 4
            self.project_main_frame_list.append(project_main_frame)
            self.project_frame_list.append(project_frame)
            
            self.project_sidepanels[project] = EditSidepanel(self.master, self, self.db, 1.04, 0.7, project)
            self.master.after(500, self.project_sidepanels[project].load_editproject_frame)
            
            
    def load_sidepanels(self):
        create_sidepanel = CreateSidepanel(self.master, self, self.db, 1.04, 0.7)
        create_floating_button = CursorButton(self.todo, text="+", fg_color="gray4", width=60, font=UBUNTU(size=30), height=60, border_width=2, border_color="gray20", hover_color="gray20", corner_radius=15, command=create_sidepanel.animate)
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
                c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The project has been successfully deleted!", sound=True, option_1="There we go!")
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
        c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The List has been successfully deleted!", sound=True, option_1="There we go!")
        c.get()
        
        
        
############################################### SIDEPANEL ###############################################



class Sidepanel(ctk.CTkScrollableFrame): #Inspired from @Atlas (YouTube)
    def __init__(self, master, todotab, db, start_pos, end_pos, label):
        super().__init__(master, label_text=label, label_fg_color=DULL_BLUE, border_width=2, border_color=WHITE, corner_radius=8, fg_color="black", label_font=UBUNTU(size=18))
        
        self.master = master
        self.todo = todotab
        self.db = db
        self.checkboxes = []
        
        self.grid_columnconfigure((0,1,2,3),weight=1)
        
        self.start_pos = start_pos + 0.04
        self.end_pos = end_pos - 0.03
        self.width = abs(start_pos - end_pos)
        self.pos = self.start_pos
        self.is_closed = True
        self.place(relx = self.start_pos, rely = 0.05, relwidth = self.width, relheight = 0.95)

    def animate(self):
        if self.is_closed:
            self.animate_forward()
        else:
            self.animate_backwards()
            

    def animate_forward(self):
        if self.master.todo.current_sidepanel:
            if (not self.master.todo.current_sidepanel.is_closed):
                self.master.todo.current_sidepanel.animate_backwards()
                return
        if self.pos > self.end_pos:
            self.pos -= 0.03
            self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
            self.after(5, self.animate_forward)
        else:
            self.is_closed = False
            self.master.todo.current_sidepanel = self

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.03
            self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
            self.after(5, self.animate_backwards)
        else:
            self.is_closed = True
            self.master.todo.current_sidepanel = None
    
    
    def load_buttons(self, checkcommand, pady, place="down"):
        self.checkbutton = CursorButton(self, command=checkcommand, fg_color=THEME_BLUE, text_color="white", text=CHECK, border_width=2, hover_color=THEME_LIGHT_BLUE, border_color=THEME_LIGHT_BLUE, corner_radius=20)
        self.cancelbutton = CursorButton(self, command=self.animate, fg_color=THEME_RED, text_color="white", text=CROSS, border_width=2, hover_color=RED, border_color=RED, corner_radius=30)
        if place == "down":
            self.checkbutton.grid(column=0, row=1, columnspan=2, sticky="sew", padx=15, pady=(pady,0))
            self.cancelbutton.grid(column=2, row=1, columnspan=2, sticky="sew", padx=15, pady=(pady,0))
        else:
            self.checkbutton.grid(column=0, row=0, columnspan=2, sticky="new", padx=15, pady=(0,pady))
            self.cancelbutton.grid(column=2, row=0, columnspan=2, sticky="new", padx=15, pady=(0,pady))
        
    def clear_entries(self, entries):
        for i in entries:
            i.delete(0, "end")
            
            
        
class CreateSidepanel(Sidepanel):
    def __init__(self, master, todo, db, start_pos, end_pos):
        super().__init__(master, todo, db, start_pos, end_pos, "CREATE A NEW WORKSPACE")

        self.master = master
        self.db = db
        self.todo = todo

        self.load_createproject_frame()
        self.load_buttons(self.create_project_event, 50)

    def load_createproject_frame(self):
        self.createproject_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.createproject_frame.grid_columnconfigure((0,1,2,3),weight=1)
        self.createproject_frame.grid(column=0, row=0, sticky="nsew", columnspan=4, padx=10, pady=5)
        ctk.CTkLabel(self.createproject_frame, text="- There must be at least one List and a Task inside it\nto create a new project.\n- To create a List in an existing project,\nenter the exact project title.\n- To create a Task,\nenter the exact Project and List titles.", font=UBUNTU(12, 'normal'), justify="left").grid(column=0, row=0, sticky="w", padx=20, pady=(10,20), columnspan=4)
        
        ttk.Separator(self.createproject_frame).grid(column=0, row=1, columnspan=4, sticky="ew")
        
        ctk.CTkLabel(self.createproject_frame, text="New/Existing Project Title:", font=UBUNTU(13), justify="left", anchor="w").grid(column=0, row=2, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=4)
        self.createproject_frame_projectentry = ctk.CTkEntry(self.createproject_frame, placeholder_text="Social Media Detox", font=UBUNTU(size=12, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.createproject_frame_projectentry.grid(column=0, row=3, sticky="ew", padx=5, pady=(5,0), columnspan=4)
        
        ctk.CTkLabel(self.createproject_frame, text="New/Existing List Title:", font=UBUNTU(13), justify="left", anchor="w").grid(column=0, row=4, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=4)
        self.createproject_frame_listentry = ctk.CTkEntry(self.createproject_frame, placeholder_text="No Instagram", font=UBUNTU(size=12, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.createproject_frame_listentry.grid(column=0, row=5, sticky="ew", padx=5, pady=(5,0), columnspan=4)
        
        ctk.CTkLabel(self.createproject_frame, text="New To-Do Title:", font=UBUNTU(13), justify="left", anchor="w").grid(column=0, row=6, sticky="nsew", padx=(5,0), pady=(20,5), columnspan=4)
        self.createproject_frame_taskentry = ctk.CTkEntry(self.createproject_frame, placeholder_text="Day 1", font=UBUNTU(size=12, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
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
            project_edit_button = CursorButton(project_main_frame, text=f"Edit", image=EDIT_IMG, font=UBUNTU(size=12), corner_radius=8, border_color=THEME_LIGHT_BLUE, border_width=2,fg_color=THEME_BLUE, hover_color=THEME_LIGHT_BLUE, command=lambda p=project: self.master.toggle_edit_sidepanel(p))
            project_delete_button = CursorButton(project_main_frame, text=f"Delete", image=DELETE_IMG, font=UBUNTU(size=12), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED, hover_color=RED, command=lambda p=project_main_frame, n=project: self.todo.delete_project_frame(p, n))
            
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

        CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The task has been added to your To-Do List!", sound=True, option_1="There we go!")
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
        super().__init__(master, todo, db, start_pos, end_pos, f"EDIT {projectname.upper()}")
        
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
        ctk.CTkLabel(self.editproject_frame, text="- Rename Project and its list(s).\n- Leave the textbox empty for no changes.", font=UBUNTU(12, 'normal'), justify="left").grid(column=0, row=0, sticky="w", padx=20, pady=(0,15), columnspan=4)
        
        ttk.Separator(self.editproject_frame).grid(column=0, row=1, columnspan=4, sticky="ew")
        
        ctk.CTkLabel(self.editproject_frame, text="Rename Project:", font=UBUNTU(15), justify="left", anchor="w").grid(column=0, row=2, sticky="nsew", padx=(5,0), pady=(15,5), columnspan=4)
        self.editproject_frame_projectentry = ctk.CTkEntry(self.editproject_frame, placeholder_text=f"{self.projectname}", font=UBUNTU(size=12, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
        self.editproject_frame_projectentry.grid(column=0, row=3, sticky="ew", padx=(5,5), pady=(5,20), columnspan=4)
        
        self.all_entries.append(self.editproject_frame_projectentry)
        sep = ttk.Separator(self.editproject_frame).grid(column=0, row=4, columnspan=4, sticky="ew")
        
        j = 5
        
        mylists = self.projectframe.mylist_list
        
        for i, mylist in enumerate(mylists):
            self.components[mylist.listname] = []
            
            label = ctk.CTkLabel(self.editproject_frame, text=f"{SUB}{mylist.listname.upper()}:", font=UBUNTU(15))
            label.grid(column=0, row=j, sticky="nsw", padx=(5,0), pady=(15,5), columnspan=4)
            
            btn = ctk.CTkButton(self.editproject_frame, command=lambda l=mylist, lab=label: self.temp_remove_list(l, lab), text=f"", image=DELETE_IMG, font=UBUNTU(size=12), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED,   hover_color=RED, width=5)
            btn.grid(column=0, row=j, sticky="e", padx=(10,0), pady=(5,5), columnspan=4)
            
            editproject_frame_listentry = ctk.CTkEntry(self.editproject_frame, placeholder_text=f"A cool new name for the list...", font=UBUNTU(size=12, weight="normal"), corner_radius=10, height=30, fg_color=NAVY_BLUE, border_width=0)
            editproject_frame_listentry.grid(column=0, row=j+1, sticky="ew", padx=(5,5), pady=(5,5), columnspan=4)
            
            self.all_entries.append(editproject_frame_listentry)
            self.editproject_frame_listentries[mylist.listname] = editproject_frame_listentry
            j += 2
            values = self.db.search_todo_by_list(mylist.listname, self.projectname)
            
            for val in values:
                seclabel = ctk.CTkLabel(self.editproject_frame, text=f"{SUBSUB}{textwrap.fill(val['task_name'],30)}", font=UBUNTU(12, "bold"), justify="left", anchor="w")
                seclabel.grid(column=0, row=j, sticky="nsew", padx=(5,10), pady=(5,5), columnspan=4)
                secbtn = ctk.CTkButton(self.editproject_frame, command=lambda t=val['id'], l=seclabel, m=mylist: self.temp_remove_task(t, l, m), text=f"{CROSS}", font=UBUNTU(size=12), corner_radius=8, border_color=RED, border_width=2,fg_color=THEME_RED,   hover_color=RED, width=5)
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
                    c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message="The task(s) were removed from your To-Do List!", sound=True, option_1="There we go!")
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
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message=f"Congrats! Your List(s) were successfully renamed!", sound=True, option_1="Sounds cool!")
                
        if renamed_project.strip():
            self.db.update_project_name(self.projectname, renamed_project)
            self.projectframe.configure(label_text=renamed_project)
            self.projectname = renamed_project
            self.editproject_frame_projectentry.configure(placeholder_text=renamed_project)
            CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp", icon="check", message=f"Congrats! Your Project is renamed to '{renamed_project}'", sound=True, option_1="Sounds cool!")
        
        self.clear_entries(self.all_entries)
        self.master.home.progressbar.update()
        self.master.home.load_home_selector_dropdown()
        
        
    def delete_items(self, items):
        for i in items:
            try:
                i.grid_forget()
            except:
                pass
        
    

############################################### CTkButton Frame ###############################################



class CursorButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.hover_cursor_on)
        self.bind("<Leave>", self.hover_cursor_off)

    def hover_cursor_on(self, event):
        self.configure(cursor="hand2")

    def hover_cursor_off(self, event):
        self.configure(cursor="")
        


############################################### ImageButton ###############################################



class ImageButton(ctk.CTkButton):
    def __init__(self, master, image_path, command, image_height=50, image_width=50, **kwargs):
        super().__init__(master, **kwargs)
        self.image = ctk.CTkImage(dark_image=Image.open(image_path), size=(image_width, image_height))
        self.button = ctk.CTkButton(self.master, text="", image=self.image, command=command, font=UBUNTU(size=40, weight="normal"), corner_radius=20, fg_color="transparent", width=3, hover=False)



############################################### KEYBINDS ###############################################


    
app = App()

def show_missingfiles_error():
    c = CTkMessagebox(corner_radius=10, fade_in_duration=3, title="LakshApp - Missing Files", icon="cancel", message="Uh oh. Seems like there are some files that are missing.\nPlease re-install the application or check the required files manually.", sound=True, option_1="Ah shit!")
    c.get()
    
def enter(event):
    if app.mainframe.tab_view.get() == 'HOME':
        app.home.add_todo_event()
    if app.mainframe.tab_view.get() == 'SESSIONS':
        app.add_own_message()

def ctrla(event):
    app.select_all()
    
app.bind('<Return>', enter)
app.bind('<Control-a>', ctrla)

app.protocol("WM_DELETE_WINDOW", app.close_confirmation)

if __name__=="__main__":
    print(colorama.Fore.CYAN + ASCII)
    app.async_mainloop()