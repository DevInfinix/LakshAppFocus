import customtkinter
import json
import random
import tkinter
import pygame
from os import environ
from tkinter import filedialog
from modules.date_visualizer import CTkCalendarStat #https://github.com/ZikPin/CTkDataVisualizingWidgets
import datetime
import asyncio
import websockets
from async_tkinter_loop import async_handler
from async_tkinter_loop.mixins import AsyncCTk


WEBSOCKET_SERVER="ws://localhost:8080"
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("./themes/dark-blue.json") 


def save_config(config):
    with open("./data/donetasks.json", "w") as f:
        json.dump(config, f, indent=4)
        

class App(customtkinter.CTk, AsyncCTk):
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
        self.normal_font = customtkinter.CTkFont(family="Ubuntu", size=18, weight="normal")
        self.btnfont=customtkinter.CTkFont(family="Ubuntu", size=16, weight="bold")
        self.total_message = 0
        
        
        ############################################### PYGAME MUSIC ###############################################
         
         
         
        self.music = pygame.mixer
        self.music.init()
        self.paused = False
        
        
         
        ############################################### DATA ###############################################
        
        
        
        with open("./data/quotes.json","r") as f:
            self.quotes = json.load(f)
        with open("./data/donetasks.json","r") as f:
            self.donetasks = json.load(f)
        self.quote_no = (random.randint(0, len(self.quotes)) - 1)
        
        
        
        ############################################### SIDEBAR ###############################################
        
        
        
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=18, fg_color="gray8")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(15,7.5),pady=15, columnspan=1)
        self.sidebar_frame.grid_columnconfigure((0,1), weight=1)
        self.sidebar_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="LakshApp", font=customtkinter.CTkFont(family="Ubuntu", size=28, weight="bold"), text_color="#91b1cc", justify="center")
        self.logo_label.grid(row=0, column=0, padx=40, pady=(100,60),columnspan=2, rowspan=1, sticky="ew")
        
        
        
        ############################################### TABS BUTTONS ###############################################
        
        
        
        self.hometab = customtkinter.CTkButton(master=self.sidebar_frame, text=" Home ", hover_color="#21568B", corner_radius=20, border_color="#21568B", border_width=2,fg_color="gray13", command=self.set_home, font=self.btnfont)
        self.hometab.grid(padx=40, pady=8, row=1, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.todotab = customtkinter.CTkButton(master=self.sidebar_frame, text=" To-Do ", hover_color="#21568B", corner_radius=20, border_color="#21568B", border_width=2,fg_color="gray13", command=self.set_todo, font=self.btnfont)
        self.todotab.grid(padx=40, pady=8, row=2, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.statstab = customtkinter.CTkButton(master=self.sidebar_frame, text=" My Progress ", hover_color="#21568B", corner_radius=20, border_color="#21568B", border_width=2,fg_color="gray13", command=self.set_stats, font=self.btnfont)
        self.statstab.grid(padx=40, pady=8, row=3, column=0,columnspan=2, rowspan=1, sticky="ew")
        self.sessionstab = customtkinter.CTkButton(master=self.sidebar_frame, text=" Live Sessions ", hover_color="#21568B", corner_radius=20, border_color="#21568B", border_width=2,fg_color="gray13", command=self.set_sessions, font=self.btnfont)
        self.sessionstab.grid(padx=40, pady=8, row=4, column=0,columnspan=2, rowspan=1, sticky="ew")
        
        
        self.switch_frame = customtkinter.CTkFrame(self.sidebar_frame, corner_radius=20, fg_color="gray4")
        self.switch_frame.grid(row=5, column=0, sticky="nsew", padx=40,pady=(8,100), columnspan=2)
        self.switch_frame.grid_columnconfigure(0, weight=1)
        self.switch_frame.grid_rowconfigure(0, weight=1)
        
        self.switch_var = customtkinter.StringVar(value="off")
        self.switch = customtkinter.CTkSwitch(self.switch_frame, text="Ambient Mode", onvalue="on", offvalue="off", variable=self.switch_var, command=self.switch_event, switch_height=15, switch_width=40, font=customtkinter.CTkFont(family="Ubuntu", size=14, weight="bold"))
        self.switch.grid(row=0, column=0, pady=10, padx=10, sticky="ew", columnspan=1)
        
        
        
        ############################################### MAINFRAME ###############################################
        
        
        
        self.mainframe = customtkinter.CTkFrame(self, corner_radius=18, fg_color="gray8")
        self.mainframe.grid(column=1, row=0, sticky="nsew", padx=(7.5,15), pady=15,columnspan=3, rowspan=4)
        self.mainframe.grid_columnconfigure((0,1), weight=1)
        self.mainframe.grid_rowconfigure((0,1,2,3), weight=1)
        
        
        
        ############################################### TABVIEW ###############################################
        
        
        
        self.tab_view = customtkinter.CTkTabview(master=self.mainframe, corner_radius=18, fg_color="gray8")
        self.tab_view.grid(padx=0, pady=0,  sticky="nsew",column=0, row=1, columnspan=2, rowspan=3)
        #self.tab_view.grid_columnconfigure((0,1,2,3),weight=1)
        #self.tab_view.grid_rowconfigure((0,1,2),weight=1)
        
        self.home = self.tab_view.add("HOME")
        self.todo = self.tab_view.add("TO-DO")
        self.stats = self.tab_view.add("STATS")
        self.sessions = self.tab_view.add("SESSIONS")
        
        self.home.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.home.grid_rowconfigure((0,1),weight=1)
        self.todo.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.todo.grid_rowconfigure((0,1),weight=1)
        self.stats.grid_columnconfigure((0,1),weight=1)
        self.stats.grid_rowconfigure(1,weight=1)
        self.sessions.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
        self.sessions.grid_rowconfigure((0,1,2,3),weight=1)
        
        self.tab_view.set("HOME")
        self.hometab.configure(fg_color="#21568B")
        
        self.tab_view._segmented_button.grid_forget()
        
        self.tabsbutton = [self.hometab, self.todotab, self.statstab, self.sessionstab]
        
        
        
############################################### HOMETAB ###############################################
        
        
        
        
        
        #self.github = customtkinter.CTkButton(master=self.sidebar_frame, command=self.test)
        #self.github.grid(padx=(10,5), pady=(10,140), row=4, column=0,columnspan=1, rowspan=1, sticky="ns")
        
        #self.developer = customtkinter.CTkButton(master=self.sidebar_frame, command=self.test)
        #self.developer.grid(padx=(5,10), pady=(10,140), row=4, column=1,columnspan=1, rowspan=1, sticky="ns")
        
        
        
       ############################################### QUOTES FRAME ###############################################
        
        
        
        self.quotes_frame = customtkinter.CTkFrame(master=self.home, fg_color="gray4", corner_radius=22)
        self.quotes_frame.grid(row=0, column=0, padx=0, pady=(5,0), sticky="nsew", columnspan=8)
        self.quotes_frame.grid_columnconfigure((0,1), weight=1)
        self.quotes_frame.grid_rowconfigure(0, weight=1)
        
        
        
        ############################################### QUOTES ###############################################
        
        
        
        self.quotes_label = customtkinter.CTkLabel(self.quotes_frame, text=f"“{self.quotes[self.quote_no]['text']}”", font=customtkinter.CTkFont(family="Helvetica", size=30, weight="bold", slant="italic"), fg_color="transparent", wraplength=780, justify="center")
        self.quotes_label.grid(row=0, column=0, pady=(60,5), padx=20, sticky="new", columnspan=2)
        self.quotes_author_label = customtkinter.CTkLabel(self.quotes_frame, text=f"{self.quotes[self.quote_no]['author']}", font=customtkinter.CTkFont(family="Helvetica", size=20, weight="normal", slant="italic"), fg_color="transparent")
        self.quotes_author_label.grid(row=1, column=0, pady=(0,0), padx=120, columnspan=8, sticky="new")
        
        self.change_quote_btn = customtkinter.CTkButton(self.quotes_frame, text="Refresh Quotes", command=self.change_quote_event, font=customtkinter.CTkFont(family="Ubuntu", size=15, weight="bold"), corner_radius=8, border_color="#21568B", border_width=2,fg_color="gray13", hover_color="#21568B",height=30)
        self.change_quote_btn.grid(row=2, column=0, pady=(50,60), padx=120, columnspan=2)
        
        
        
        ############################################### ENTRY ###############################################
        
        
        
        self.entry_todo = customtkinter.CTkEntry(self.home, placeholder_text="What are you planning to complete today? Start grinding champ!", font=self.normal_font, corner_radius=50, height=60)
        self.entry_todo.grid(row=3, column=0, pady=(60,0), padx=(50,10),  sticky="ew", columnspan=7)
        self.add_todo = customtkinter.CTkButton(self.home, text="+", command=self.add_todo_event, font=customtkinter.CTkFont(family="Ubuntu", size=40), corner_radius=100, fg_color="black", width=5)
        self.add_todo.grid(row=3, column=0, pady=(60,0), padx=(2.5,50), columnspan=8, sticky="e")
        
        
        
        ############################################### PROGRESS ###############################################
        
        
        
        self.progressbar = customtkinter.CTkProgressBar(self.home, orientation="horizontal", height=15)
        self.progressbar.set(self.percent())
        self.progressbar.grid(row=4, column=0, pady=(20,5), padx=(80,130), sticky="ew", columnspan=8)
        self.progresslabel = customtkinter.CTkLabel(self.home, text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)", font=self.normal_font, justify="right")
        self.progresslabel.grid(row=5, column=0, pady=0, padx=10, sticky="e", columnspan=8)
        
        

        
        
############################################### TO-DO TAB ###############################################
        

        
        values = self.donetasks["pendingtasks"]
        self.scrollable_checkbox_frame = ToDoFrame(self.todo, values=values, donetasks=self.donetasks)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=70, pady=(30, 0), sticky="ew", columnspan=8)

        self.button = customtkinter.CTkButton(self.todo, text="🗹 | Mark as Completed", command=self.mark_as_done)
        self.button.grid(row=1, column=0, padx=70, pady=(20,0), sticky="ew", columnspan=8)        
        
        self.button = customtkinter.CTkButton(self.todo, text="𐄂 | Delete all Tasks", command=self.delete_tasks, fg_color="#731a1a", hover_color="red")
        self.button.grid(row=2, column=0, padx=70, pady=(10,50), sticky="ew", columnspan=8) 
        
        

############################################### STATS TAB ###############################################


        
        self.stats_label = customtkinter.CTkLabel(self.stats, text=f"HERE's WHAT I ACHIEVED!", font=customtkinter.CTkFont(family="Ubuntu", size=30, weight="bold"), fg_color="transparent", wraplength=780, justify="center")
        self.stats_label.grid(row=0, column=0, pady=(20,5), padx=60, sticky="new", columnspan=2)
        dates = self.donetasks['dates']
        if dates == []:
            values = {}
        else:
            values = {tuple(val): 10 for val in dates}
            self.calendar = CTkCalendarStat(self.stats, values, border_width=0, border_color="white",
                                fg_color="#020317", title_bar_border_width=2, title_bar_border_color="gray80",
                                title_bar_fg_color="#020F43", calendar_fg_color="#020F43", corner_radius=30,
                                title_bar_corner_radius=10, calendar_corner_radius=10, calendar_border_color="white",
                                calendar_border_width=0, calendar_label_pad=5, data_colors=["blue", "green", "red"]
                    )
            self.calendar.grid(row=1, column=0, pady=(60,60), padx=60, sticky="new", columnspan=2)

        
        
############################################### SESSIONS TAB ###############################################



        self.sessions_frame = customtkinter.CTkScrollableFrame(self.sessions, corner_radius=18, fg_color="gray4")
        self.sessions_frame.grid(row=0, column=0, sticky="nsew", padx=15,pady=(0,20), columnspan=8, rowspan=3)
        self.sessions_frame.grid_columnconfigure((0,1), weight=1)
        
        self.send_area = customtkinter.CTkEntry(self.sessions, placeholder_text="Hello bhai kaisa hein bhai!", font=self.normal_font, corner_radius=50, height=60)
        self.send_area.grid(row=3, column=0, pady=(0,20), padx=(50,10),  sticky="ew", columnspan=7, rowspan=1)
        self.send_button = customtkinter.CTkButton(self.sessions, text="+", command=self.add_own_message, font=customtkinter.CTkFont(family="Ubuntu", size=40), corner_radius=100, fg_color="black", width=5)
        self.send_button.grid(row=3, column=0, pady=(0,20), padx=(2.5,50), columnspan=8, sticky="e", rowspan=1)
            
        
        
        self.message_window = None
        self.socket = None
            
############################################### FUNCTIONS ###############################################
    
    
    
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
                self.show_message_dialogue("Select a valid format\nto play music (mp3/ogg).")
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
        
        
        
    def mark_as_done(self):
        checkboxes = self.scrollable_checkbox_frame.get()
        #for i in self.scrollable_checkbox_frame.checkboxes:
            #print(i.cget("text"), i.get(), self.donetasks['pendingtasks'])
        if checkboxes == []:
            self.show_message_dialogue("Please select a task first.")
        else:
            dialog = customtkinter.CTkInputDialog(text="Type 'done' to confirm the completion of tasks.", title="LakshApp")
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
                    save_config(self.donetasks)
                    self.progressbar.set(self.percent())
                    self.progresslabel.configure(text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)")
                    effect2 = self.music.Sound('./sounds/trumpets.mp3')
                    effect2.set_volume(0.1)
                    effect2.play()
                    
                
    def delete_tasks(self):
        checkboxes = self.scrollable_checkbox_frame.checkboxes
        if checkboxes == [] or not checkboxes:
            self.show_message_dialogue("The To-Do list is empty.\nAdd your first To-Do!")
        else:
            dialog = customtkinter.CTkInputDialog(text="Type 'delete' to confirm the deletion of tasks.", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'delete':
                    for i in checkboxes:
                        i.destroy()
                    self.scrollable_checkbox_frame.checkboxes = []
                    self.donetasks["pendingtasks"] = {}
                    self.donetasks["count"] = 0
                    self.donetasks["total"] = 0
                    save_config(self.donetasks)
                    self.progressbar.set(0)
                    self.progresslabel.configure(text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)")
                    self.show_message_dialogue("Successfully deleted all To-Dos!")
        
        
    def add_todo_event(self):
        event = self.entry_todo.get()
        if event == "":
            return
        elif event in self.donetasks["pendingtasks"]:
            self.show_message_dialogue("A task with the same title\nis already pending/completed.")
            return
        self.donetasks["total"] += 1
        self.donetasks["pendingtasks"][event] = 0
        save_config(self.donetasks)
        self.progressbar.set(self.percent())
        self.progresslabel.configure(text=f"↪ Your Progress ({self.donetasks['count']}/{self.donetasks['total']} completed)")
        
        
        checkboxes = self.scrollable_checkbox_frame.checkboxes
        checkbox = customtkinter.CTkCheckBox(self.scrollable_checkbox_frame, text=event, hover=True)
        checkbox.grid(row=len(checkboxes), column=0, padx=50, pady=(10, 10), sticky="ew", columnspan=2)
        checkboxes.append(checkbox)
        
    
        self.show_message_dialogue("The task has been added to your To-Do List.\nGo to To-Do Tab to view more!")
        
        effect1 = self.music.Sound('./sounds/level.mp3')
        effect1.set_volume(0.1)
        effect1.play()
    
    
    
    def show_message_dialogue(self, message):
        if self.message_window is None or not self.message_window.winfo_exists():
            self.message_window = MessageDialogue(message)
            self.message_window.title = "LakshApp" # create window if its None or destroyed
        else:
            self.message_window.title = "LakshApp"
            self.message_window.focus()
        
    def set_current_tab(self, current_tab):
        for tab in self.tabsbutton:
            if current_tab == tab:
                tab.configure(fg_color="#21568B")
            else:
                tab.configure(fg_color="gray13")
        
    def set_home(self):
        #print(self.tab_view.get())
        self.tab_view.set("HOME")
        self.set_current_tab(self.hometab)
        
    def set_todo(self):
        #print(self.tab_view.get())
        self.tab_view.set("TO-DO")
        self.set_current_tab(self.todotab)
        
    def set_stats(self):
        self.refresh_cache()
        dates = self.donetasks['dates']
        if dates == []:
            self.show_message_dialogue("You haven't completed any tasks yet.\nStart completing now!")
        else:
            values = {tuple(val): 10 for val in dates}
            self.calendar.destroy()
            self.calendar = CTkCalendarStat(self.stats, values, border_width=0, border_color="white",
                                fg_color="#020317", title_bar_border_width=2, title_bar_border_color="gray80",
                                title_bar_fg_color="#020F43", calendar_fg_color="#020F43", corner_radius=30,
                                title_bar_corner_radius=10, calendar_corner_radius=10, calendar_border_color="white",
                                calendar_border_width=0, calendar_label_pad=5, data_colors=["blue", "green", "red"]
                    )
            self.calendar.grid(row=1, column=0, pady=(60,60), padx=60, sticky="new", columnspan=2)
            #print(self.tab_view.get())
            self.tab_view.set("STATS")
            self.set_current_tab(self.statstab)
        
    @async_handler
    async def set_sessions(self):
        if not self.socket:
            dialog = customtkinter.CTkInputDialog(text="Type 'start' to start or 'join'\nto join a live session.", title="LakshApp")
            inp = dialog.get_input()
            if inp:
                if inp.lower() == 'start':
                    dialog2 = customtkinter.CTkInputDialog(text="Enter your username\nfor the live session.", title="LakshApp")
                    inp2 = dialog2.get_input()
                    if inp2:
                        if inp2 != '':
                            self.own_username = inp2
                            await self.start_server(WEBSOCKET_SERVER, inp2)
                if inp.lower() == 'join':
                    dialog2 = customtkinter.CTkInputDialog(text="Enter the code for the live session.", title="LakshApp")
                    inp2 = dialog2.get_input()
                    if inp2:
                        if inp2 != '':
                            self.server_code = inp2
                            
                            dialog3 = customtkinter.CTkInputDialog(text="Enter your username\nfor the live session.", title="LakshApp")
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
            # move cursor to the end
            self.entry_todo.icursor('end')
            #stop propagation
            return 'break'
        if self.tab_view.get() == 'SESSIONS':
            self.send_area.select_range(0, 'end')
            self.send_area.icursor('end')
            return 'break'
    
    def refresh_cache(self):
        with open("./data/donetasks.json","r") as f:
            self.donetasks = json.load(f)
            

    
    
    @async_handler
    async def add_own_message(self):
        message = self.send_area.get()
        if message == '':
            return
        message_frame = customtkinter.CTkFrame(self.sessions_frame, corner_radius=18, fg_color="#14375e")
        message_frame.grid(row=self.total_message, column=0, sticky="new", padx=5,pady=5, columnspan=2, rowspan=1)
        message_frame.grid_columnconfigure((0,1), weight=1)
        
        message_label = customtkinter.CTkLabel(message_frame, text=f"[You]: {message}", font=customtkinter.CTkFont(family="Ubuntu", size=18, weight="bold"), fg_color="transparent", wraplength=680, justify="left")
        message_label.grid(row=0, column=0, pady=5, padx=15, sticky="nw", columnspan=2)
            
        self.total_message += 1
        
        data = {
            'from': 'client',
            'type': 'message',
            'message': message,
            'user': self.own_username
        }
        await self.socket.send(json.dumps(data))
        self.send_area.delete(0, "end")
        
        
    def add_other_message(self, user, message):
        message_frame = customtkinter.CTkFrame(self.sessions_frame, corner_radius=18, fg_color="#325882")
        if user == 'System':
            message_frame.configure(fg_color="purple")
        message_frame.grid(row=self.total_message, column=0, sticky="new", padx=5,pady=5, columnspan=2, rowspan=1)
        message_frame.grid_columnconfigure((0,1), weight=1)
        
        message_label = customtkinter.CTkLabel(message_frame, text=f"[{user}]: {message}", font=customtkinter.CTkFont(family="Ubuntu", size=18, weight="bold"), fg_color="transparent", wraplength=680, justify="left")
        message_label.grid(row=0, column=0, pady=5, padx=15, sticky="nw", columnspan=2)
            
        self.total_message += 1
    
    
    
    async def start_server(self, server_address, username):
        async with websockets.connect(server_address) as socket:
            event = {
                'from': 'client',
                'type': 'start',
                'user': username
            }
            await asyncio.sleep(1)
            await socket.send(json.dumps(event))
            await asyncio.gather(self.receive_message(socket, 'host', username))
         
       
    async def join_server(self, server_address, code, username):
        async with websockets.connect(server_address) as socket:
            event = {
                'from': 'client',
                'type': 'join',
                'code': code,
                'user': username
            }
            await asyncio.sleep(1)
            await socket.send(json.dumps(event)) 
            await asyncio.gather(self.receive_message(socket, 'member', username))
                
                
    async def receive_message(self, socket, role, username):
        async for message in socket:
            event = json.loads(message)
            if event['type'] == 'error':
                if event['errortype'] == 'SessionNotFound':
                    print(event['message']) 
                    self.show_message_dialogue(event['message'])
                    self.set_home()
                    break
                if event['errortype'] == 'RoomFull':
                    print(event['message'])
                    self.show_message_dialogue(event['message'])
                    self.set_home()
                    break
            if event['type'] == 'started':
                self.tab_view.set("SESSIONS")
                self.set_current_tab(self.sessionstab)
                await asyncio.sleep(2)
                print(f"Your code is: [{event['code']}]")
                self.add_other_message(user='System', message=f"Your room's code is: [{event['code']}]")
                self.socket = socket
            if event['type'] == 'joined':
                self.tab_view.set("SESSIONS")
                self.set_current_tab(self.sessionstab)
                await asyncio.sleep(2)
                print(f"You joined {event['code']}")
                self.add_other_message(user='System', message=f"You joined {event['code']}")
                self.socket = socket
            if event['type'] == 'message':
                print(event['message'])
                if event['user'] != username:
                    self.add_other_message(user=event['user'], message=event['message'])
            if event['type'] == 'disconnected':
                if event['from'] == 'server':
                    if event['role'] == 'host':
                        print('The host has been disconnected')
                        self.show_message_dialogue('The host has been disconnected')
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
                            self.show_message_dialogue('You have been disconnected')
                            await asyncio.sleep(1)
                            self.tab_view.set("HOME")
                            self.set_current_tab(self.hometab)
                            return
                        else:
                            self.show_message_dialogue('The participant has been disconnected')
                            
                

############################################### TO-DO FRAME ###############################################



class ToDoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, values, donetasks):
        super().__init__(master, label_text="⇲ MY TO-DO LIST", label_fg_color="#33414d", border_width=2, border_color="black", corner_radius=18, fg_color="gray4", label_font=customtkinter.CTkFont(family="Ubuntu", size=16, weight="bold"))
        
        self.donetasks = donetasks
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(list(self.values.keys())):
            state = tkinter.DISABLED if (self.values.get(value) == 1) else tkinter.NORMAL
            checkbox = customtkinter.CTkCheckBox(self, text=value, hover=True, state=state, onvalue="on", offvalue="off", command=self.add_temp_check())
            if self.values.get(value) == 1:
                checkbox.select()
            checkbox.grid(row=i, column=0, padx=50, pady=(10, 10), sticky="ew", columnspan=2)
            self.checkboxes.append(checkbox)
        
    def add_temp_check(self):
        pass
        
    def get(self):
        if self.checkboxes == [] or not self.checkboxes:
            print("no checkboxes fount", self.checkboxes)
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if (checkbox.get() == "on" or checkbox.get() == "1" or checkbox.get() == 1) and self.donetasks["pendingtasks"][checkbox.cget('text')] == 0:
                checked_checkboxes.append(checkbox)
        return checked_checkboxes
        
        
        
############################################### MESSAGE DIALOGUE ###############################################
         
         
         
class MessageDialogue(customtkinter.CTkToplevel):
    def __init__(self, message):
        super().__init__()
        self.geometry("300x100")

        self.label = customtkinter.CTkLabel(self, text=f"{message}")
        self.label.pack(padx=20, pady=20)



############################################### KEYBINDS ###############################################



app = App()

def enter(event):
    if app.tab_view.get() == 'TO-DO':
        app.add_todo_event()
    if app.tab_view.get() == 'SESSIONS':
        app.add_own_message()

def ctrla(event):
    app.select_all()
    
app.bind('<Return>', enter)
app.bind('<Control-a>', ctrla)

app.async_mainloop()