##
#by: robertproducts

from ensurepip import version
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.font import BOLD
import pygame.mixer as sfx

import random
import os
import sys
import subprocess

import webbrowser
import datetime
import json

sfx.init()
sys.setrecursionlimit(999999)
del sys

class data:
    def get(src: str = "data/data.json") -> dict:
        with open(src, "r", encoding="utf-8") as f:
            return json.load(f)

    def push(src: dict, path: str = "data/data.json") -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(src, f)

    def theme():
        return data.get("resources/themes/"+data.get()["theme"])

    def locale():
        return data.get("resources/locales/"+data.get()["locale"])

    def achievement(ach_id: str):
        if not(data.get("data/achievements.json")[ach_id]):
            msgbox.showinfo(data.locale()["achievements"]["title"],
                data.locale()["achievements"]["body"]+": "+data.locale()["achievements"][ach_id]+"!")
            tmp = data.get("data/achievements.json")
            tmp[ach_id] = True
            data.push(tmp, "data/achievements.json")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CodeBasics")
        self.resizable(False, False)
        self.attributes("-topmost", data.get()["topmost"])
        self.geometry(f'{data.get()["geometry"][0]}'
                      f'x{data.get()["geometry"][1]}'
                      f'+{self.winfo_screenwidth() // 2 - data.get()["geometry"][0] // 2}'
                      f'+{self.winfo_screenheight() // 2 - data.get()["geometry"][1] // 2 - 50}')
        
        if data.get()["fullscreen"]:
            self.geometry(f'{self.winfo_screenwidth()}'
                          f'x{self.winfo_screenheight()}+0+0')
            self.overrideredirect(True)
        
        self.tasks = [
            "python::50",
            "python::25",
            "python::10",
            "python::75"
            ]

        if os.path.exists("data/task.txt"):
            with open("data/task.txt", "r", encoding="utf-8") as f:
                self.task = f.read().split("::")
        else:
            self.task = random.choice(self.tasks).split("::")
            with open("data/task.txt", "w", encoding="utf-8") as f:
                f.write(self.task[0]+"::"+self.task[1])

        tmp = data.get()
        tmp["enters"] += 1
        data.push(tmp)
        if data.get()["enters"] == 50:
            data.achievement("enters_50")
        
        self.iconbitmap(data.get()["icon"])
        sfx.music.load(f"resources/sounds/menu{random.randint(1, 3)}.mp3")
        sfx.music.play(loops=-1, fade_ms=50)
        Menu(self).place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
    
class Menu(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=data.theme()["bg"])
        self.__widgets()
    
    def __widgets(self):
        self.titleLabel = tk.Label(self, text="CodeBasics", font=(data.theme()["font"], 48, BOLD),
                                   fg=data.theme()["col"], bg=data.theme()["bg"], justify="center")
        self.titleLabel.place(x=50, y=25, width=425)

        self.startButton = tk.Button(self, text=data.locale()["menu"]["startButton"],
                                     fg=data.theme()["col"], bg=data.theme()["obj"],
                                     activeforeground=data.theme()["col"],
                                     activebackground=data.theme()["obj:hov"],
                                     font=(data.theme()["font"], 20), cursor="hand2",
                                     command=self.__startButton_pressed)
        self.startButton.place(x=50, y=175, width=425, height=75)
        self.startButton.bind("<Enter>", lambda x:self.startButton.config(bg=data.theme()["obj:hov"]))
        self.startButton.bind("<Leave>", lambda x:self.startButton.config(bg=data.theme()["obj"]))

        self.settingsButton = tk.Button(self, text=data.locale()["menu"]["settingsButton"],
                                        fg=data.theme()["col"], bg=data.theme()["obj"],
                                        activeforeground=data.theme()["col"],
                                        activebackground=data.theme()["obj:hov"],
                                        font=(data.theme()["font"], 20), cursor="hand2",
                                        command=self.__settingsButton_pressed)
        self.settingsButton.place(x=50, y=255, width=425, height=75)
        self.settingsButton.bind("<Enter>", lambda x:self.settingsButton.config(bg=data.theme()["obj:hov"]))
        self.settingsButton.bind("<Leave>", lambda x:self.settingsButton.config(bg=data.theme()["obj"]))

        self.statisticsButton = tk.Button(self, text=data.locale()["menu"]["statisticsButton"],
                                          fg=data.theme()["col"], bg=data.theme()["obj"],
                                          activeforeground=data.theme()["col"],
                                          activebackground=data.theme()["obj:hov"],
                                          font=(data.theme()["font"], 20), cursor="hand2",
                                          command=self.__statisticsButton_pressed)
        self.statisticsButton.place(x=50, y=335, width=425, height=75)
        self.statisticsButton.bind("<Enter>", lambda x:self.statisticsButton.config(bg=data.theme()["obj:hov"]))
        self.statisticsButton.bind("<Leave>", lambda x:self.statisticsButton.config(bg=data.theme()["obj"]))

        self.exitButton = tk.Button(self, text=data.locale()["menu"]["exitButton"],
                                    fg=data.theme()["col"], bg=data.theme()["danger"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["danger:hov"],
                                    font=(data.theme()["font"], 20), cursor="hand2",
                                    command=self.__exitButton_pressed)
        self.exitButton.place(x=50, y=415, width=425, height=75)
        self.exitButton.bind("<Enter>", lambda x:self.exitButton.config(bg=data.theme()["danger:hov"]))
        self.exitButton.bind("<Leave>", lambda x:self.exitButton.config(bg=data.theme()["danger"]))

        self.pubLabel = tk.Label(self, text=f"RobertProducts {datetime.datetime.now().year}", fg=data.theme()["col"],
                                 bg=data.theme()["bg"], font=(data.theme()["font"], 14, "bold"))
        self.pubLabel.place(x=5, y=self.parent.winfo_height()-5, anchor="sw")

        self.versionLabel = tk.Label(self, text="v.2022.8.12", fg=data.theme()["col"],
                                     bg=data.theme()["bg"], font=(data.theme()["font"], 14, "bold"))
        self.versionLabel.place(x=self.parent.winfo_width() - 5, y=self.parent.winfo_height()-5, anchor="se")

        greeting = data.locale()["menu"]["goodnight"] if 23 <= datetime.datetime.now().hour < 6 else \
                   data.locale()["menu"]["goodmorning"] if 6 <= datetime.datetime.now().hour < 13 else \
                   data.locale()["menu"]["goodafternoon"] if 13 <= datetime.datetime.now().hour < 20 else \
                   data.locale()["menu"]["goodevening"]
        self.greetingLabel = tk.Label(self, text=f"{greeting},\n{os.getlogin()}!", fg=data.theme()["col"],
                                      bg=data.theme()["obj"], font=(data.theme()["font"], 26, "bold"),)
        self.greetingLabel.place(x=self.parent.winfo_width() - 25, y=25, anchor="ne",
                                 width=self.parent.winfo_width()//3, height=150)

        self.taskLabel = tk.Label(self, text=data.locale()["menu"]["taskLabel"].format(self.parent.task[1], self.parent.task[0]),
                                  fg=data.theme()["col"],
                                  bg=data.theme()["obj"], font=(data.theme()["font"], 20))
        self.taskLabel.place(x=self.parent.winfo_width() - 25, y=180, anchor="ne",
                             width=self.parent.winfo_width()//3, height=150)

        self.vkimg = tk.PhotoImage(file="resources/images/vk.png")
        self.tgimg = tk.PhotoImage(file="resources/images/telegram.png")

        self.vkButton = tk.Button(self, image=self.vkimg, compound="left",
                                  fg="#ffffff", bg="#0077ff",
                                  activeforeground="#ffffff",
                                  activebackground="#0077ff",
                                  font=(data.theme()["font"], 16),
                                  cursor="question_arrow",
                                  command=lambda: webbrowser.open("https://vk.com/robertproducts", new=2))
        self.vkButton.place(x=self.parent.winfo_width() - 105, y=415, anchor="ne",
                            width=75, height=75)
        
        self.tgButton = tk.Button(self, image=self.tgimg, compound="left",
                                  fg="#ffffff", bg="#24a4e2",
                                  activeforeground="#ffffff",
                                  activebackground="#24a4e2",
                                  font=(data.theme()["font"], 16),
                                  cursor="question_arrow",
                                  command=lambda: webbrowser.open("https://t.me/robertproducts", new=2))
        self.tgButton.place(x=self.parent.winfo_width() - 25, y=415, anchor="ne",
                            width=75, height=75)
        
        self.webButton = tk.Button(self, text="Сайт",
                                   fg=data.theme()["col"], bg=data.theme()["obj"],
                                   activeforeground=data.theme()["col"],
                                   activebackground=data.theme()["bg"],
                                   font=(data.theme()["font"], 16),
                                   cursor="question_arrow",
                                   command=lambda: webbrowser.open("https://robertproducts.netlify.app", new=2))
        self.webButton.place(x=self.parent.winfo_width() - 185, y=415, anchor="ne",
                            width=self.parent.winfo_width()//3 - 160, height=75)
        self.webButton.bind("<Enter>", lambda arg:self.webButton.config(bg=data.theme()["obj:hov"]))
        self.webButton.bind("<Leave>", lambda arg:self.webButton.config(bg=data.theme()["obj"]))

    def __startButton_pressed(self):
        self.destroy()
        SelectLang(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
        
    def __settingsButton_pressed(self):
        self.destroy()
        Settings(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())

    def __statisticsButton_pressed(self):
        self.destroy()
        Statistics(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())

    def __exitButton_pressed(self):
        self.parent.destroy()

class Settings(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=data.theme()["bg"])
        self.__widgets()
    
    def __widgets(self):
        self.titleLabel = tk.Label(self, text=data.locale()["settings"]["titleLabel"],
                                   font=(data.theme()["font"], 36, BOLD),
                                   fg=data.theme()["col"], bg=data.theme()["bg"])
        self.titleLabel.place(x=25, y=25, width=425)

        self.themeButton = tk.Button(self, text=data.locale()["settings"]["themeButton"]+": "+data.theme()["title"],
                                          fg=data.theme()["col"], bg=data.theme()["obj"],
                                          activeforeground=data.theme()["col"],
                                          activebackground=data.theme()["obj:hov"],
                                          font=(data.theme()["font"], 20), cursor="hand2",
                                          command=self.__themeButton_pressed)
        self.themeButton.place(x=50, y=175, width=425, height=75)
        self.themeButton.bind("<Enter>", lambda x:self.themeButton.config(bg=data.theme()["obj:hov"]))
        self.themeButton.bind("<Leave>", lambda x:self.themeButton.config(bg=data.theme()["obj"]))

        self.localeButton = tk.Button(self, text=data.locale()["settings"]["localeButton"]+": "+data.locale()["title"],
                                      fg=data.theme()["col"], bg=data.theme()["obj"],
                                      activeforeground=data.theme()["col"],
                                      activebackground=data.theme()["obj:hov"],
                                      font=(data.theme()["font"], 20), cursor="hand2",
                                      command=self.__localeButton_pressed)
        self.localeButton.place(x=50, y=255, width=425, height=75)
        self.localeButton.bind("<Enter>", lambda x:self.localeButton.config(bg=data.theme()["obj:hov"]))
        self.localeButton.bind("<Leave>", lambda x:self.localeButton.config(bg=data.theme()["obj"]))

        self.soundLabel = tk.Label(self, text=data.locale()["settings"]["soundLabel"]+":", fg=data.theme()["col"],
                                   bg=data.theme()["bg"], font=(data.theme()["font"], 24))
        self.soundLabel.place(x=50, y=335, height=75)

        self.soundSpinbox = tk.Spinbox(self, from_=0, to=100, fg=data.theme()["col"],
                                       bg=data.theme()["obj"], font=(data.theme()["font"], 24),
                                       insertbackground=data.theme()["col"],
                                       buttonbackground=data.theme()["obj:hov"], buttoncursor="hand2")
        self.soundSpinbox.place(x=475, y=335, width=200, height=75, anchor="ne")
        self.soundSpinbox.delete(0)
        self.soundSpinbox.insert(0, int(data.get()["volume"]*100))

        self.windowsizeLabel = tk.Label(self, text=data.locale()["settings"]["geometryLabel"]+":", fg=data.theme()["col"],
                                        bg=data.theme()["bg"], font=(data.theme()["font"], 24))
        self.windowsizeLabel.place(x=self.parent.winfo_width() - 460, anchor="ne", y=175, height=75)

        self.windowsizeWidthSpinbox = tk.Spinbox(self, from_=data.get()["geometry"][0] if data.get()["fullscreen"] else 1128, to=4096, fg=data.theme()["col"],
                                                 state="disabled" if data.get()["fullscreen"] else "normal",
                                                 disabledbackground=data.theme()["obj:hov"],
                                                 insertbackground=data.theme()["col"],
                                                 bg=data.theme()["obj"], font=(data.theme()["font"], 24),
                                                 buttonbackground=data.theme()["obj:hov"],
                                                 buttoncursor="hand2", cursor="arrow" if data.get()["fullscreen"] else "xterm")
        self.windowsizeWidthSpinbox.place(x=self.parent.winfo_width() - 255, anchor="ne", y=175, width=200, height=75)
        self.windowsizeWidthSpinbox.delete(0, "end")
        self.windowsizeWidthSpinbox.insert(0, int(data.get()["geometry"][0]))

        self.windowsizeHeightSpinbox = tk.Spinbox(self, from_=data.get()["geometry"][1] if data.get()["fullscreen"] else 648, to=2048, fg=data.theme()["col"],
                                                  state="disabled" if data.get()["fullscreen"] else "normal",
                                                  disabledbackground=data.theme()["obj:hov"],
                                                  insertbackground=data.theme()["col"],
                                                  bg=data.theme()["obj"], font=(data.theme()["font"], 24),
                                                  buttonbackground=data.theme()["obj:hov"],
                                                  buttoncursor="hand2", cursor="arrow" if data.get()["fullscreen"] else "xterm")
        self.windowsizeHeightSpinbox.place(x=self.parent.winfo_width() - 50, anchor="ne", y=175, width=200, height=75)
        self.windowsizeHeightSpinbox.delete(0, "end")
        self.windowsizeHeightSpinbox.insert(0, int(data.get()["geometry"][1]))

        self.fullscreenButton = tk.Button(self, text=data.locale()["settings"]["fullscreenButton"]+": "+(data.locale()["settings"]["on"] if data.get()["fullscreen"] else data.locale()["settings"]["off"]),
                                          fg=data.theme()["col"], bg=data.theme()["obj"],
                                          activeforeground=data.theme()["col"],
                                          activebackground=data.theme()["obj:hov"],
                                          cursor="hand2",
                                          command=self.__fullscreenButton_pressed,
                                          font=(data.theme()["font"], 16, "bold"))
        self.fullscreenButton.bind("<Enter>", lambda arg:self.fullscreenButton.config(bg=data.theme()["obj:hov"]))
        self.fullscreenButton.bind("<Leave>", lambda arg:self.fullscreenButton.config(bg=data.theme()["obj"]))
        self.fullscreenButton.place(x=self.parent.winfo_width() - 50, anchor="ne", y=255, width=405, height=75)

        self.topmostButton = tk.Button(self, text=data.locale()["settings"]["topmostButton"]+": "+(data.locale()["settings"]["on"] if data.get()["topmost"] else data.locale()["settings"]["off"]),
                                       fg=data.theme()["col"], bg=data.theme()["obj"],
                                       activeforeground=data.theme()["col"],
                                       activebackground=data.theme()["obj:hov"],
                                       cursor="hand2",
                                       command=self.__topmostButton_pressed,
                                       font=(data.theme()["font"], 16, "bold"))
        self.topmostButton.bind("<Enter>", lambda arg:self.topmostButton.config(bg=data.theme()["obj:hov"]))
        self.topmostButton.bind("<Leave>", lambda arg:self.topmostButton.config(bg=data.theme()["obj"]))
        self.topmostButton.place(x=self.parent.winfo_width() - 50, anchor="ne", y=335, width=405, height=75)

        self.forceButton = tk.Button(self, text=data.locale()["settings"]["forceButton"],
                                    fg=data.theme()["col"], bg=data.theme()["warning"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["warning:hov"],
                                    cursor="hand2",
                                    command=self.__forceButton_pressed,
                                    font=(data.theme()["font"], 16, "bold"))
        self.forceButton.bind("<Enter>", lambda arg:self.forceButton.config(bg=data.theme()["warning:hov"]))
        self.forceButton.bind("<Leave>", lambda arg:self.forceButton.config(bg=data.theme()["warning"]))
        self.forceButton.place(x=355, y=self.parent.winfo_height() - 25, width=325, height=75, anchor="sw")

        self.exitButton = tk.Button(self, text=data.locale()["settings"]["exitButton"],
                                    fg=data.theme()["col"], bg=data.theme()["danger"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["danger:hov"],
                                    font=(data.theme()["font"], 20), cursor="hand2",
                                    command=self.__exitButton_pressed)
        self.exitButton.place(x=25, y=self.parent.winfo_height() - 25, width=325, height=75, anchor="sw")
        self.exitButton.bind("<Enter>", lambda x:self.exitButton.config(bg=data.theme()["danger:hov"]))
        self.exitButton.bind("<Leave>", lambda x:self.exitButton.config(bg=data.theme()["danger"]))

    def __exitButton_pressed(self):
        destroy_window = False
        tmp = data.get()
        tmp["volume"] = int(float(self.soundSpinbox.get()))/100
        sfx.music.set_volume(tmp["volume"])
        if int(self.windowsizeWidthSpinbox.get()) < 1128 or int(self.windowsizeHeightSpinbox.get()) < 648:
            if not(msgbox.askokcancel(data.locale()["settings"]["veryLowGeometryAlertTitle"],
                                      data.locale()["settings"]["veryLowGeometryAlertBody"].format(int(self.windowsizeWidthSpinbox.get()), int(self.windowsizeHeightSpinbox.get())))):
                                      return
        tmp["geometry"] = [int(self.windowsizeWidthSpinbox.get()), int(self.windowsizeHeightSpinbox.get())]
        if tmp["geometry"] != data.get()["geometry"]: destroy_window = True
        data.push(tmp)
        self.destroy()
        global app
        if destroy_window:
            self.parent.destroy()
            app = App()
            for i in app.winfo_children():
                if i.winfo_class == "Frame": i.destroy()
        Menu(app).place(x=0, y=0, width=app.winfo_width(), height=app.winfo_height())

    def __themeButton_pressed(self):
        tmp = data.get()
        tmp["theme"] = os.listdir("resources/themes")[0] if os.listdir("resources/themes").index(tmp["theme"]) == len(os.listdir("resources/themes"))-1 else os.listdir("resources/themes")[os.listdir("resources/themes").index(tmp["theme"])+1]
        data.push(tmp)
        self.destroy()
        Settings(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())

    def __localeButton_pressed(self):
        tmp = data.get()
        tmp["locale"] = os.listdir("resources/locales")[0] if os.listdir("resources/locales").index(tmp["locale"]) == len(os.listdir("resources/locales"))-1 else os.listdir("resources/locales")[os.listdir("resources/locales").index(tmp["locale"])+1]
        data.push(tmp)
        self.destroy()
        Settings(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())

    def __forceButton_pressed(self):
        if not(msgbox.askyesno(data.locale()["settings"]["forceAllSettingsAlertTitle"],
                               data.locale()["settings"]["forceAllSettingsAlertBody"])):
            return
        data.push({"icon": "resources/images/main.ico", "theme": "0_default.json", "locale": "0_ru.json", "volume": 0.1, "geometry": [1280, 720], "fullscreen": False, "topmost": True, "enters": 0, "passed": 0, "tasks":0, "nothingthere": False})
        msgbox.showinfo(data.locale()["settings"]["forceAllSettingsAlertSuccessTitle"],
                        data.locale()["settings"]["forceAllSettingsAlertSuccessBody"])
        global app
        self.parent.destroy()
        app = App()
        for i in app.winfo_children():
            if i.winfo_class == "Frame": i.destroy()
        Settings(app).place(x=0, y=0, width=app.winfo_width(), height=app.winfo_height())

    def __fullscreenButton_pressed(self):
        tmp = data.get()
        tmp["fullscreen"] = not(tmp["fullscreen"])
        data.push(tmp)
        global app
        self.parent.destroy()
        app = App()
        for i in app.winfo_children():
            if i.winfo_class == "Frame": i.destroy()
        Settings(app).place(x=0, y=0, width=app.winfo_width(), height=app.winfo_height())
    
    def __topmostButton_pressed(self):
        tmp = data.get()
        tmp["topmost"] = not(tmp["topmost"])
        data.push(tmp)
        self.parent.attributes("-topmost", data.get()["topmost"])
        self.destroy()
        Settings(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())

class Statistics(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=data.theme()["bg"])
        self.__widgets()
    
    def __widgets(self):
        self.titleLabel = tk.Label(self, text=data.locale()["statistics"]["titleLabel"],
                                   font=(data.theme()["font"], 36, BOLD),
                                   fg=data.theme()["col"], bg=data.theme()["bg"])
        self.titleLabel.place(x=25, y=25, width=425)

        self.pythonLabel = tk.Label(self, text=f'Python - {data.locale()["statistics"]["last"]}: '
                                               f'{data.get("data/progress.json")["python"]["last"][0]}/'
                                               f'{data.get("data/progress.json")["python"]["last"][1]} ('
                                               f'{round(data.get("data/progress.json")["python"]["last"][0]/data.get("data/progress.json")["python"]["last"][1]*100, ndigits=1) if data.get("data/progress.json")["python"]["last"][1] != 0 else 0}%)\n          '
                                               f'{data.locale()["statistics"]["best"]}: '
                                               f'{data.get("data/progress.json")["python"]["best"][0]}/'
                                               f'{data.get("data/progress.json")["python"]["best"][1]} ('
                                               f'{round(data.get("data/progress.json")["python"]["last"][0]/data.get("data/progress.json")["python"]["last"][1]*100, ndigits=1) if data.get("data/progress.json")["python"]["best"][1] != 0 else 0}%)',
                                    fg=data.theme()["col"], bg=data.theme()["bg"], font=(data.theme()["font"], 20))
        self.pythonLabel.place(x=25, y=175)

        self.achievementsLabel = tk.Label(self, text=f'{data.locale()["statistics"]["achievements"]}: '
                                                     f'{len([i for i in data.get("data/achievements.json").values() if i])}/{len(data.get("data/achievements.json"))}',
                                          fg=data.theme()["col"], bg=data.theme()["bg"], font=(data.theme()["font"], 20))
        self.achievementsLabel.place(x=self.parent.winfo_width() - 100, y=175, anchor="ne", width=400)
        
        self.achievementsList = tk.Listbox(self, bg=data.theme()["obj"], fg=data.theme()["col"],
                                           font=(data.theme()["font"], 16), height=8, width=30,
                                           selectbackground=data.theme()["obj"], cursor="hand2")
        self.achievementsList.place(x=self.parent.winfo_width() - 100, y=250, anchor="ne", width=400)
        for i in [i for i in data.get("data/achievements.json").keys() if data.get("data/achievements.json")[i]]:
            self.achievementsList.insert(0, data.locale()["achievements"][i])

        self.forceButton = tk.Button(self, text=data.locale()["settings"]["forceButton"],
                                    fg=data.theme()["col"], bg=data.theme()["warning"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["warning:hov"],
                                    cursor="hand2",
                                    command=self.__forceButton_pressed,
                                    font=(data.theme()["font"], 16, "bold"))
        self.forceButton.bind("<Enter>", lambda arg:self.forceButton.config(bg=data.theme()["warning:hov"]))
        self.forceButton.bind("<Leave>", lambda arg:self.forceButton.config(bg=data.theme()["warning"]))
        self.forceButton.place(x=355, y=self.parent.winfo_height() - 25, width=325, height=75, anchor="sw")

        self.exitButton = tk.Button(self, text=data.locale()["settings"]["exitButton"],
                                    fg=data.theme()["col"], bg=data.theme()["danger"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["danger:hov"],
                                    font=(data.theme()["font"], 20), cursor="hand2",
                                    command=self.__exitButton_pressed)
        self.exitButton.place(x=25, y=self.parent.winfo_height() - 25, width=325, height=75, anchor="sw")
        self.exitButton.bind("<Enter>", lambda x:self.exitButton.config(bg=data.theme()["danger:hov"]))
        self.exitButton.bind("<Leave>", lambda x:self.exitButton.config(bg=data.theme()["danger"]))

    def __exitButton_pressed(self):
        self.destroy()
        Menu(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())

    def __forceButton_pressed(self):
        if not(msgbox.askyesno(data.locale()["settings"]["forceAllSettingsAlertTitle"],
                               data.locale()["settings"]["forceAllSettingsAlertBody"])):
            return
        data.push({
                    "python":{
                        "last":[0, 0],
                        "best":[0, 0]
                    }
                }, "data/progress.json")
        tmp = data.get()
        tmp["enters"] = tmp["passed"] = 0
        data.push(tmp)
        data.push({
                    "title":False,
                    "python_10":False,
                    "python_25":False,
                    "python_50":False,
                    "python_75":False,
                    "python_100":False,
                    "python_200":False,
                    "enters_50":False,
                    "passed_100":False,
                    "passed_200":False,
                    "passed_300":False,
                    "passed_400":False,
                    "passed_500":False
                }, "data/achievements.json")
        msgbox.showinfo(data.locale()["settings"]["forceAllSettingsAlertSuccessTitle"],
                        data.locale()["settings"]["forceAllSettingsAlertSuccessBody"])
        
        self.destroy()
        Statistics(self.parent).place(x=0, y=0, width=app.winfo_width(), height=app.winfo_height())

class SelectLang(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=data.theme()["bg"])
        self.__widgets()
    
    def __widgets(self):
        self.titleLabel = tk.Label(self, text=data.locale()["selectlang"]["titleLabel"],
                                   font=(data.theme()["font"], 36, BOLD),
                                   fg=data.theme()["col"], bg=data.theme()["bg"])
        self.titleLabel.place(x=self.parent.winfo_width()//2, y=25, height=75, anchor="n")

        self.exitButton = tk.Button(self, text=data.locale()["settings"]["exitButton"],
                                    fg=data.theme()["col"], bg=data.theme()["danger"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["danger:hov"],
                                    font=(data.theme()["font"], 20), cursor="hand2",
                                    command=self.__exitButton_pressed)
        self.exitButton.place(x=25, y=self.parent.winfo_height() - 25, width=325, height=75, anchor="sw")
        self.exitButton.bind("<Enter>", lambda x:self.exitButton.config(bg=data.theme()["danger:hov"]))
        self.exitButton.bind("<Leave>", lambda x:self.exitButton.config(bg=data.theme()["danger"]))
        
        self.python = tk.PhotoImage(file="resources/images/python.png")
        self.python = self.python.subsample(10, 10)
        self.pythonButton = tk.Button(self, text="  Python", image=self.python,
                                      compound="left",
                                      fg=data.theme()["col"], bg=data.theme()["obj"],
                                      activeforeground=data.theme()["col"],
                                      activebackground=data.theme()["obj:hov"],
                                      font=(data.theme()["font"], 20), cursor="hand2",
                                      command=self.__pythonButton_pressed)
        self.pythonButton.place(x=self.parent.winfo_width()//2, y=175, width=325, height=75, anchor="n")
        self.pythonButton.bind("<Enter>", lambda x:self.pythonButton.config(bg=data.theme()["obj:hov"]))
        self.pythonButton.bind("<Leave>", lambda x:self.pythonButton.config(bg=data.theme()["obj"]))

        self.python = tk.PhotoImage(file="resources/images/python.png")
        self.python = self.python.subsample(10, 10)

        self.cpp = tk.PhotoImage(file="resources/images/cpp.png")
        self.cpp = self.cpp.subsample(10, 10)

        self.java = tk.PhotoImage(file="resources/images/java.png")
        self.java = self.java.subsample(10, 10)

        self.pythonButton = tk.Button(self, text="  Python", image=self.python,
                                      compound="left",
                                      fg=data.theme()["col"], bg=data.theme()["obj"],
                                      activeforeground=data.theme()["col"],
                                      activebackground=data.theme()["obj:hov"],
                                      font=(data.theme()["font"], 20), cursor="hand2",
                                      command=self.__pythonButton_pressed)
        self.pythonButton.place(x=self.parent.winfo_width()//2, y=175, width=325, height=75, anchor="n")
        self.pythonButton.bind("<Enter>", lambda x:self.pythonButton.config(bg=data.theme()["obj:hov"]))
        self.pythonButton.bind("<Leave>", lambda x:self.pythonButton.config(bg=data.theme()["obj"]))

        self.cppButton = tk.Button(self, text="  C++", image=self.cpp,
                                      compound="left",
                                      fg=data.theme()["col"], bg=data.theme()["obj"],
                                      activeforeground=data.theme()["col"],
                                      activebackground=data.theme()["obj:hov"],
                                      font=(data.theme()["font"], 20), cursor="question_arrow",
                                      command=self.__cppButton_pressed)
        self.cppButton.place(x=self.parent.winfo_width()//2, y=255, width=325, height=75, anchor="n")
        self.cppButton.bind("<Enter>", lambda x:self.cppButton.config(bg=data.theme()["obj"]))
        self.cppButton.bind("<Leave>", lambda x:self.cppButton.config(bg=data.theme()["obj"]))

        self.javaButton = tk.Button(self, text="  Java", image=self.java,
                                      compound="left",
                                      fg=data.theme()["col"], bg=data.theme()["obj"],
                                      activeforeground=data.theme()["col"],
                                      activebackground=data.theme()["obj:hov"],
                                      font=(data.theme()["font"], 20), cursor="question_arrow",
                                      command=self.__javaButton_pressed)
        self.javaButton.place(x=self.parent.winfo_width()//2, y=335, width=325, height=75, anchor="n")
        self.javaButton.bind("<Enter>", lambda x:self.javaButton.config(bg=data.theme()["obj"]))
        self.javaButton.bind("<Leave>", lambda x:self.javaButton.config(bg=data.theme()["obj"]))

    def __exitButton_pressed(self):
        self.destroy()
        Menu(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
        
    def __pythonButton_pressed(self):
        self.destroy()
        Python(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
        
    def __cppButton_pressed(self):
        msgbox.showinfo(data.locale()["selectlang"]["langNotAllowedAlertTitle"],
                        data.locale()["selectlang"]["langNotAllowedAlertBody"])

    def __javaButton_pressed(self):
        msgbox.showinfo(data.locale()["selectlang"]["langNotAllowedAlertTitle"],
                        data.locale()["selectlang"]["langNotAllowedAlertBody"])

class Python(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=data.theme()["bg"])

        sfx.music.load("resources/sounds/python.mp3")
        sfx.music.play(loops=-1)

        self.right = 0
        self.level = 0
        self.problem = ""
        self.answer = ""
        self.test = ""

        self.__level_draw()
    
    def __level_draw(self):
        self.test = random.choice(os.listdir("resources/tests/python"))
        with open("resources/tests/python/"+self.test, "r", encoding="utf-8") as f:
            self.problem = f.read()

        out, err = subprocess.Popen(f'python3 resources/tests/python/{self.test}', shell=True, stdout=subprocess.PIPE).communicate()
        self.answer = str(str(out, 'utf-8').split("\n")[0][:-1])
    
        self.titleLabel = tk.Label(self, text=data.locale()["main"]["titleLabel"],
                                   font=(data.theme()["font"], 24, BOLD),
                                   fg=data.theme()["col"], bg=data.theme()["bg"])
        self.titleLabel.place(x=25, y=25, height=75)

        self.problemLabel = tk.Label(self, text=self.problem,
                                     font=(data.theme()["code"], 16, BOLD),
                                     fg=data.theme()["col"], bg=data.theme()["obj"],
                                     justify="left")
        self.problemLabel.place(x=75, y=175, width=self.parent.winfo_width()//2, height=5*self.parent.winfo_height()//8)
        
        self.answerEntry = tk.Entry(self, font=(data.theme()["code"], 24, BOLD),
                                    fg=data.theme()["col"], bg=data.theme()["obj:hov"],
                                    insertbackground=data.theme()["col"])
        self.answerEntry.place(x=self.parent.winfo_width() - 50, y=225,
                               width=self.parent.winfo_width() // 4, height=75, anchor="ne")
        self.answerEntry.focus()
        self.answerEntry.bind("<Return>", lambda x:self.__sendButton_pressed())
        self.answerEntry.bind("<Escape>", lambda x:self.__exitButton_pressed())

        self.sendButton = tk.Button(self, text=data.locale()["main"]["sendButton"],
                                    fg=data.theme()["col"], bg=data.theme()["success"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["success:hov"],
                                    font=(data.theme()["font"], 20), cursor="hand2",
                                    command=self.__sendButton_pressed)
        self.sendButton.place(x=self.parent.winfo_width() - 50, y=305, width=self.parent.winfo_width() // 4, height=75, anchor="ne")
        self.sendButton.bind("<Enter>", lambda x:self.sendButton.config(bg=data.theme()["success:hov"]))
        self.sendButton.bind("<Leave>", lambda x:self.sendButton.config(bg=data.theme()["success"]))

        self.exitButton = tk.Button(self, text=data.locale()["main"]["exitButton"],
                                    fg=data.theme()["col"], bg=data.theme()["danger"],
                                    activeforeground=data.theme()["col"],
                                    activebackground=data.theme()["danger:hov"],
                                    font=(data.theme()["font"], 20), cursor="hand2",
                                    command=self.__exitButton_pressed)
        self.exitButton.place(x=self.parent.winfo_width() - 50, y=385, width=self.parent.winfo_width() // 4, height=75, anchor="ne")
        self.exitButton.bind("<Enter>", lambda x:self.exitButton.config(bg=data.theme()["danger:hov"]))
        self.exitButton.bind("<Leave>", lambda x:self.exitButton.config(bg=data.theme()["danger"]))

        self.currentResultLabel = tk.Label(self, text=data.locale()["main"]["currentResultLabel"]+f": {self.right}/{self.level+1}",
                                           font=(data.theme()["font"], 16, BOLD),
                                           wraplength=self.parent.winfo_width() // 4,
                                           fg=data.theme()["col"], bg=data.theme()["bg"])
        self.currentResultLabel.place(x=self.parent.winfo_width() - 50, y=465, width=self.parent.winfo_width() // 4, height=75, anchor="ne")

    def __sendButton_pressed(self):
        if (str(self.answer) == str(self.answerEntry.get())) or \
            (data.get()["nothingthere"]):
            self.right += 1
            tmp = data.get()
            tmp["passed"] += 1
            data.push(tmp)
            if data.get()["passed"] == 100: data.achievement("passed_100")
            elif data.get()["passed"] == 200: data.achievement("passed_200")
            elif data.get()["passed"] == 300: data.achievement("passed_300")
            elif data.get()["passed"] == 400: data.achievement("passed_400")
            elif data.get()["passed"] == 500: data.achievement("passed_500")

        if self.right == 10: data.achievement("python_10")
        elif self.right == 25: data.achievement("python_25")
        elif self.right == 50: data.achievement("python_50")
        elif self.right == 75: data.achievement("python_75")
        elif self.right == 100: data.achievement("python_100")
        elif self.right == 200: data.achievement("python_200")
        self.level += 1

        if self.parent.task[0] == "python":
            if self.right >= int(self.parent.task[1]):
                msgbox.showinfo(data.locale()["main"]["taskPassedAlertTitle"],
                                data.locale()["main"]["taskPassedAlertBody"])
                tmp = data.get()
                tmp["tasks"] += 1
                data.push(tmp)

                foo = self.parent.tasks
                self.parent.task = random.choice(foo).split("::")
                with open("data/task.txt", "w", encoding="utf-8") as f:
                    f.write(self.parent.task[0]+"::"+self.parent.task[1])

        self.destroy()
        global app
        app.main = Python(self.parent)
        app.main.right = self.right
        app.main.level = self.level
        app.main.place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
        app.main.currentResultLabel.config(text=data.locale()["main"]["currentResultLabel"]+f": {self.right}/{self.level+1}")
        app.update()

    def __exitButton_pressed(self):
        if not msgbox.askokcancel(data.locale()["main"]["stopTestAlertTitle"], data.locale()["main"]["stopTestAlertBody"]):
            return
        
        tmp = data.get("data/progress.json")
        tmp["python"]["last"] = [self.right, self.level]
        best = False
        if (tmp["python"]["last"][1] != 0) and (tmp["python"]["best"][1] != 0):
            if (tmp["python"]["last"][0]/tmp["python"]["last"][1] > tmp["python"]["best"][0]/tmp["python"]["best"][1]) or \
                (tmp["python"]["last"][0]/tmp["python"]["last"][1] == tmp["python"]["best"][0]/tmp["python"]["best"][1] and tmp["python"]["last"][1] > tmp["python"]["best"][1]):
                tmp["python"]["best"] = tmp["python"]["last"]
                best = True
        elif (tmp["python"]["last"][1] != 0) and (tmp["python"]["best"][1] == 0):
             tmp["python"]["best"] = tmp["python"]["last"]
             best = True
        data.push(tmp, "data/progress.json")
        msgbox.showinfo(data.locale()["main"]["resultAlertTitle"], data.locale()["main"]["resultAlertBody"]+f': {tmp["python"]["last"][0]}/{tmp["python"]["last"][1]}')
        self.destroy()
        sfx.music.load(f"resources/sounds/menu{random.randint(1, 3)}.mp3")
        sfx.music.play(loops=-1)
        Menu(self.parent).place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height()) 

if __name__ == "__main__":
    app = App()
    sfx.music.set_volume(data.get()["volume"])
    app.mainloop()