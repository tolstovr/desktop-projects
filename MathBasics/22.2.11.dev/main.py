##
#coding: utf-8
#by: dev.EXE

import tkinter
import tkinter.font
import tkinter.messagebox
import tkinter.constants

import os
import os.path
import sys
import json
import random
import datetime
import webbrowser
import pygame

sys.setrecursionlimit(4096)
del sys

class error:
    class DataDownloadError(Exception):
        pass

    class DataDownloadLang(Exception):
        pass

    class ByeByeError(Exception):
        pass

    class DataUploadWarning(Warning):
        pass

class Data:
    def download_data() -> dict:
        try:
            with open("configuration.json", "r", encoding="utf-8") as data_src:
                return json.load(data_src)
        except:
            raise error.DataDownloadError("Cannot download data from configuration.json")
    
    def upload_data(src=dict) -> bool:
        try:
            with open("configuration.json", "w", encoding="utf-8") as data_file:
                json.dump(src, data_file)
                return True
        except:
            raise error.DataUploadWarning("Cannot upload data to configuration.json")
    
    def download_statistics() -> dict:
        try:
            with open("statistics.json", "r", encoding="utf-8") as data_src:
                return json.load(data_src)
        except:
            raise error.DataDownloadError("Cannot download statistics from configuration.json")
    
    def upload_statistics(src=dict) -> bool:
        try:
            with open("statistics.json", "w", encoding="utf-8") as data_file:
                json.dump(src, data_file)
                return True
        except:
            raise error.DataUploadWarning("Cannot upload statistics to configuration.json")
    
    def get_lang(lang=str) -> dict:
        try:
            with open("assets/locale/{}.json".format(lang), "r", encoding="utf-8") as lang_file:
                return json.load(lang_file)
        except:
            raise error.DataDownloadLang("Cannot download locale from {}.json".format(lang))
    
    def get_theme(theme=str) -> dict:
        try:
            with open("assets/themes/{}.json".format(theme), "r", encoding="utf-8") as theme_file:
                return json.load(theme_file)
        except:
            raise error.DataDownloadLang("Cannot download theme from {}.json".format(theme))
    
    def set_next_theme(root=tkinter.Tk):
        current = Data.download_data()["root"]["theme"]
        themes = os.listdir("assets/themes")
        for i in range(len(themes)):
            themes[i] = themes[i].split(".")[0]
        current_index = themes.index(current)
        if current_index < len(themes)-1:
            new_index = current_index + 1
        else:
            new_index = 0
        foo = Data.download_data()
        foo["root"]["theme"] = themes[new_index]
        Data.upload_data(src=foo)
        root.config(bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"])
    
    def set_next_lang():
        current = Data.download_data()["root"]["lang"]
        langs = os.listdir("assets/locale")
        for i in range(len(langs)):
            langs[i] = langs[i].split(".")[0]
        current_index = langs.index(current)
        if current_index < len(langs)-1:
            new_index = current_index + 1
        else:
            new_index = 0
        foo = Data.download_data()
        foo["root"]["lang"] = langs[new_index]
        Data.upload_data(src=foo)
    
    def greet() -> str:
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            return Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["good_morning"]
        elif 12 <= hour < 19:
            return Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["good_afternoon"]
        elif 12 <= hour < 19:
            return Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["good_evening"]
        else:
            return Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["good_night"]
    
    def reset_stats():
        foo = {
                  "infinity_mode":{
                      "last": [0, 0],
                      "best": [0, 0]
                  },
                  "quick_mode":{
                      "last": [0, 20],
                      "best": [0, 20]
                  }
              }
        try:
            with open("statistics.json", "w", encoding="utf-8") as stats_file:
                json.dump(foo, stats_file)
        except:
            raise error.DataUploadWarning("Cannot reset statistics")
        
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("MathBasics")
        self.geometry("{}x{}+{}+{}".format(Data.download_data()["geometry"][0],
                                           Data.download_data()["geometry"][1],
                                           Data.download_data()["geometry"][2],
                                           Data.download_data()["geometry"][3]))
        self.iconbitmap(Data.download_data()["root"]["icon"])
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.config(bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"])
        if Data.download_data()["root"]["sound"]:
            pygame.mixer.music.load("assets/music/menu/menu.mp3")
            pygame.mixer.music.play(loops=-1)
        Menu(parent=self).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

class Menu(tkinter.Frame):
    def __init__(self, parent=tkinter.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"])
        self.widgets()
    
    def widgets(self):
        self.titleLabel = tkinter.Label(self,
                                        text="MathBasics",
                                        fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                        font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 48, tkinter.font.BOLD))

        self.greetingLabel = tkinter.Label(self,
                                           text="{},\n{}".format(Data.greet(), os.getlogin()),
                                           fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                           bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                           font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 24, tkinter.font.BOLD))
    
        self.devexeLabel = tkinter.Label(self,
                                         text=f"dev.EXE {datetime.datetime.now().year}\nAll rights reserved!",
                                         fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                         bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                         justify=tkinter.LEFT,
                                         font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 12, tkinter.font.BOLD))

        self.versionLabel = tkinter.Label(self,
                                          text="v."+".".join(str(i) for i in Data.download_data()["root"]["version"]),
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          justify=tkinter.RIGHT,
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 12, tkinter.font.BOLD))

        self.statisticsLabel = tkinter.Button(self,
                                              relief=tkinter.FLAT,
                                              text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["statistics"].format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["infinity_mode"],
                                                                                                                                                   Data.download_statistics()["infinity_mode"]["last"][0],
                                                                                                                                                   Data.download_statistics()["infinity_mode"]["last"][1],
                                                                                                                                                   Data.download_statistics()["infinity_mode"]["best"][0],
                                                                                                                                                   Data.download_statistics()["infinity_mode"]["best"][1],
                                                                                                                                                   Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["labels"]["quick_mode"],
                                                                                                                                                   Data.download_statistics()["quick_mode"]["last"][0],
                                                                                                                                                   Data.download_statistics()["quick_mode"]["last"][1],
                                                                                                                                                   Data.download_statistics()["quick_mode"]["best"][0],
                                                                                                                                                   Data.download_statistics()["quick_mode"]["best"][1]),
                                              fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                              bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                              activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                              activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                              justify=tkinter.CENTER,
                                              font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 16, tkinter.font.BOLD),
                                              command=self.reset_stats)

        self.startButton = tkinter.Button(self,
                                          text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["start_button"],
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                          activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                          activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 24, tkinter.font.BOLD),
                                          command=self.start)

        self.aboutButton = tkinter.Button(self,
                                          text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["about_button"],
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                          activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                          activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                          command=self.about)
        
        self.langButton = tkinter.Button(self,
                                         text="{}: {}".format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["lang_button"], Data.get_lang(lang=Data.download_data()["root"]["lang"])["title"]),
                                         fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                         bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                         activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                         activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                         font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                         command=self.set_next_lang)
        
        self.themeButton = tkinter.Button(self,
                                          text="{}: {}".format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["theme_button"], Data.get_theme(theme=Data.download_data()["root"]["theme"])["title"]),
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                          activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                          activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                          command=self.set_next_theme)

        self.soundButton = tkinter.Button(self,
                                          text="{}: {}".format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["sound_button"], Data.download_data()["root"]["sound"]),
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                          activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                          activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                          command=self.sound)
        
        self.quitButton = tkinter.Button(self,
                                         text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["quit_button"],
                                         fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                         bg="#cc0000",
                                         activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                         activebackground="#dd0000",
                                         font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                         command=self.parent.destroy)

        self.titleLabel.place(x=25, y=25)
        self.greetingLabel.place(x=int(self.parent.geometry().split("x")[0])-25, y=25, anchor=tkinter.NE, width=500)
        self.devexeLabel.place(x=0, y=int(self.parent.geometry().split("x")[1].split("+")[0]), anchor=tkinter.SW)
        self.versionLabel.place(x=int(self.parent.geometry().split("x")[0]), y=int(self.parent.geometry().split("x")[1].split("+")[0]), anchor=tkinter.SE)
        self.soundButton.place(x=int(self.parent.geometry().split("x")[0])-25, y=225, anchor=tkinter.NE, width=500)
        self.statisticsLabel.place(x=int(self.parent.geometry().split("x")[0])-25, y=305, anchor=tkinter.NE, width=500)

        self.startButton.place(x=25, y=225, width=505, height=75)
        self.aboutButton.place(x=25, y=305, width=505, height=75)
        self.langButton.place(x=25, y=385, width=250, height=75)
        self.themeButton.place(x=280, y=385, width=250, height=75)
        self.quitButton.place(x=25, y=465, width=505, height=75)
    
    def start(self):
        self.destroy()
        Choose(parent=self.parent).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

    def about(self):
        self.destroy()
        About(parent=self.parent).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)
    
    def sound(self):
        foo = Data.download_data()
        foo["root"]["sound"] = not(foo["root"]["sound"])
        Data.upload_data(src=foo)
        if Data.download_data()["root"]["sound"]:
            pygame.mixer.music.load("assets/music/menu/menu.mp3")
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()
        self.destroy()
        Menu(parent=self.parent).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)        

    def set_next_lang(self):
        Data.set_next_lang()
        self.destroy()
        Menu(parent=self.parent).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

    def set_next_theme(self):
        Data.set_next_theme(root=self.parent)
        self.destroy()
        Menu(parent=self.parent).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)
    
    def reset_stats(self):
        if tkinter.messagebox.askyesno("MathBasics", Data.get_lang(lang=Data.download_data()["root"]["lang"])["warns"]["askResetStats"]):
            Data.reset_stats()
            tkinter.messagebox.showinfo("MathBasics", Data.get_lang(lang=Data.download_data()["root"]["lang"])["warns"]["sucResetStats"])
        self.destroy()
        Menu(parent=self.parent).pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

class Choose(tkinter.Frame):
    def __init__(self, parent=tkinter.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"])
        self.widgets()

    def widgets(self):
        self.titleLabel = tkinter.Label(self,
                                        text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["choose"]["labels"]["title"],
                                        fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                        font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 36, tkinter.font.BOLD))

        self.infinityButton = tkinter.Button(self,
                                             text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["choose"]["buttons"]["infinity_button"],
                                             font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                             fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                             bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                             activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                             activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                             command=self.infinity_mode, width=19)
        
        self.quickButton = tkinter.Button(self,
                                          text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["choose"]["buttons"]["quick_button"],
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                          activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                          activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          command=self.quick_mode, width=19)

        self.backBtn = tkinter.Button(self,
                                      text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["back_button"],
                                      font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                      fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                      bg="#ee0000",
                                      activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                      activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                      command=self.exit_choose)

        self.titleLabel.pack(fill=tkinter.X, side=tkinter.TOP, pady=25)
        self.infinityButton.pack(side=tkinter.TOP, pady=25)
        self.quickButton.pack(side=tkinter.TOP, pady=25)
        self.backBtn.place(x=1200, y=600, width=400, height=75, anchor=tkinter.SE)
    
    def exit_choose(self):
        self.destroy()
        Menu(parent=self.parent).pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    
    def infinity_mode(self):
        self.destroy()
        if Data.download_data()["root"]["sound"]:
            pygame.mixer.music.load("assets/music/main/inf.mp3")
            pygame.mixer.music.play(loops=-1)
        Infinity(self.parent, 0, 0)
    
    def quick_mode(self):
        self.destroy()
        if Data.download_data()["root"]["sound"]:
            pygame.mixer.music.load("assets/music/main/quick.mp3")
            pygame.mixer.music.play(loops=-1)
        Quick(self.parent, 0, 0)

class About(tkinter.Frame):
    def __init__(self, parent=tkinter.Tk):
        super().__init__()
        if Data.download_data()["root"]["sound"]:
            pygame.mixer.Sound("assets/music/_cogwheel_.mp3").play(loops=0)
            pygame.mixer.music.load("assets/music/about/about.mp3")
            pygame.mixer.music.play(loops=-1)
        self.parent = parent
        self.config(bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"])
        self.widgets()
    
    def widgets(self):
        self.titleLabel = tkinter.Label(self,
                                        text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["menu"]["buttons"]["about_button"],
                                        fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                        font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 48, tkinter.font.BOLD))

        self.devgroupLabel = tkinter.Label(self,
                                           text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["labels"]["devgroup"]+"\ndev.EXE",
                                           font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                           fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                           bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                           justify=tkinter.LEFT)
        
        self.solodevLabel = tkinter.Label(self,
                                          text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["labels"]["solodev"]+"\n@robertproducts",
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                          justify=tkinter.LEFT)

        self.musicText = tkinter.Label(self,
                                       text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["labels"]["music"]+": TobyFox",
                                       font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20),
                                       fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                       bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                       justify=tkinter.LEFT)
        
        self.versionLabel = tkinter.Label(self,
                                          text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["labels"]["version"].format("v."+".".join(str(i) for i in Data.download_data()["root"]["version"])),
                                          font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 14),
                                          fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                          bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"], justify = tkinter.LEFT)

        self.vkImage = tkinter.PhotoImage(file="assets/img/vk.gif")
        self.instaImage = tkinter.PhotoImage(file="assets/img/insta.gif")

        self.devgroupBtn = tkinter.Button(self,
                                     text="   {}".format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["insta_button"]),
                                     image = self.instaImage,
                                     compound=tkinter.LEFT,
                                     font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                     fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                     bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                     activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                     activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                     command=lambda: webbrowser.open("https://instagram.com/desktopexe", new=2))
        
        self.vkBtn = tkinter.Button(self,
                               text="   {}".format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["vk_button"]),
                               image = self.vkImage,
                               compound=tkinter.LEFT,
                               font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                               fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                               bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                               activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                               activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                               command=lambda: webbrowser.open("https://vk.com/robertproducts", new=2))

        self.instaBtn = tkinter.Button(self,
                                  text=" {}".format(Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["insta_button"]),
                                  image = self.instaImage,
                                  compound=tkinter.LEFT,
                                  font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                  fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                  bg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                                  activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                  activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                  command=lambda: webbrowser.open("https://instagram.com/robertproducts", new=2))
        
        self.backBtn = tkinter.Button(self,
                                 text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["back_button"],
                                 font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                 fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                 bg="#ee0000",
                                 activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                 activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                 command=self.exit_about)

        self.donBtn = tkinter.Button(self, 
                                text=Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["donation_button"],
                                font=(Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 20, tkinter.font.BOLD),
                                fg=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                bg="#cccc00",
                                activeforeground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                activebackground=Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                command=lambda: webbrowser.open("https://www.donationalerts.com/r/robertproducts", new=2))

        self.titleLabel.place(x=25, y=25)
        self.devgroupLabel.place(x=25, y=125)
        self.solodevLabel.place(x=25, y=225)
        self.versionLabel.place(x=125, y=500)

        self.devgroupBtn.place(x=1270, y=125, width=525, height=75, anchor=tkinter.NE)
        self.vkBtn.place(x=1270, y=215, width=260, height=75, anchor=tkinter.NE)
        self.instaBtn.place(x=1005, y=215, width=260, height=75, anchor=tkinter.NE)
        self.donBtn.place(x=1270, y=305, width=525, height=75, anchor=tkinter.NE)
        self.backBtn.place(x=1200, y=600, width=400, height=75, anchor=tkinter.SE)
        self.musicText.place(x=25, y=325)

    def exit_about(self):
        self.destroy()
        if Data.download_data()["root"]["sound"]:
            pygame.mixer.Sound("assets/music/_cogwheel_.mp3").play(loops=0)
            pygame.mixer.music.load("assets/music/menu/menu.mp3")
            pygame.mixer.music.play(loops=-1)
        Menu(parent=self.parent).pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

def Infinity(app, level, right):
    easyList = range(0, 10)
    averList = range(0, 25)
    proList = range(100, 500)
    hardList = range(500, 1000)
    impossibleList = range(5000, 10000)
    
    def genLevel(app, level, right, bg):
        for i in app.place_slaves():
            i.destroy()
        
        def check(rightanswer, useranswer, right):
            try:
                if rightanswer == int(useranswer):
                    right += 1
            except:
                pass
            genLevel(app, level, right, bg)
        
        def save_result(app, level, right, inMenu):
            foo = Data.download_statistics()
            app.protocol("WM_DELETE_WINDOW", app.destroy)
            foo["infinity_mode"]["last"] = [right, level]
            try:
                if round(foo["infinity_mode"]["last"][0]/foo["infinity_mode"]["last"][1], ndigits=2) > round(foo["infinity_mode"]["best"][0]/foo["infinity_mode"]["best"][1], ndigits=2):
                    foo["infinity_mode"]["best"] = foo["infinity_mode"]["last"]
                elif round(foo["infinity_mode"]["last"][0]/foo["infinity_mode"]["last"][1], ndigits=2) == round(foo["infinity_mode"]["best"][0]/foo["infinity_mode"]["best"][1], ndigits=2):
                    if foo["infinity_mode"]["last"][1] > foo["infinity_mode"]["best"][1]:
                        foo["infinity_mode"]["best"] = foo["infinity_mode"]["last"]
            except ZeroDivisionError:
                if foo["infinity_mode"]["best"][1] == 0:
                    foo["infinity_mode"]["best"] = foo["infinity_mode"]["last"]

            Data.upload_statistics(src=foo)
            if inMenu:
                for i in app.place_slaves():
                    i.destroy()
                if Data.download_data()["root"]["sound"]:
                    pygame.mixer.music.load("assets/music/menu/menu.mp3")
                    pygame.mixer.music.play(loops=-1)
                Menu(parent=app).pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
            else:
                lambda: app.destroy()
            
        level += 1
        if level <= 25:
            problem = f"{random.choice(easyList)}*{random.choice(easyList)}"
            hardness = Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["easy"]
            bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"]
        elif level > 25 and level <= 75:
            problem = f"{random.choice(averList)}*{random.choice(averList)}"
            hardness = Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["aver"]
            bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"]
        elif level > 75 and level <= 125:
            problem = f"{random.choice(proList)}*{random.choice(proList)}"
            hardness = Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["pro"]
            bg = "#dd9900"
        elif level > 125 and level <= 200:
            problem = f"{random.choice(hardList)}*{random.choice(hardList)}"
            hardness = Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["hard"]
            bg = "#dd0000"
        else:
            problem = f"{random.choice(impossibleList)}*{random.choice(impossibleList)}"
            hardness = Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["impossible"]
            bg = "#550000"
        rightanswer = eval(problem)
        
        problemLabel = tkinter.Label(app,
                                     text = f'{Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["problem"]} {level}: {problem} =',
                                     font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 36, tkinter.font.BOLD),
                                     fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                     bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                     justify = tkinter.LEFT)

        hardnessLabel = tkinter.Label(app,
                                      text = f'{Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["hardlevel"]}:\n{hardness}',
                                      font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 14, tkinter.font.BOLD),
                                      fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                      bg = bg)
        
        answerLabel = tkinter.Label(app,
                                    text = f'{Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["answer"]}:',
                                    font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 24, tkinter.font.BOLD),
                                    fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                    bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                    justify = tkinter.LEFT)
        
        answerEntry = tkinter.Entry(app,
                                    font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 24, tkinter.font.BOLD),
                                    fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                    bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                    justify = tkinter.RIGHT)
        def bind_check():
            check(rightanswer, str(answerEntry.get()), right)
        answerEntry.bind("<Return>", bind_check)
        
        currentResultLabel = tkinter.Label(app,
                                           text = f'{Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["currentlevel"]}:\n{right}/{level - 1}',
                                           font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 24, tkinter.font.BOLD),
                                           fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                           bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                           justify = tkinter.LEFT)
        
        saveandquitBtn = tkinter.Button(app,
                                        text = Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["back_button"],
                                        font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 16),
                                        fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        bg = "#dd0000",
                                        activeforeground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        activebackground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                        command = lambda: save_result(app, level-1, right, True))
        
        nextBtn = tkinter.Button(app,
                                 text = Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["buttons"]["send_button"],
                                 font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 16),
                                 fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                 bg = "#00dd00",
                                 activeforeground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["extra"],
                                 activebackground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                 command = lambda: check(rightanswer, str(answerEntry.get()), right))
        
        problemLabel.place(x = 25, y = 25)
        answerLabel.place(x = 25, y = 225)
        currentResultLabel.place(x = 25, y = 425)
        answerEntry.place(x = int(app.geometry().split("x")[0]) - 600, y = 225)
        
        hardnessLabel.place(x = int(app.geometry().split("x")[0]) - 500, y = 350, width = 400)

        nextBtn.place(x = int(app.geometry().split("x")[0]) - 400, y = int(app.geometry().split("x")[1].split("+")[0]) - 260, width = 225, height = 75)
        saveandquitBtn.place(x = int(app.geometry().split("x")[0]) - 400, y = int(app.geometry().split("x")[1].split("+")[0]) - 180, width = 225, height = 75)
        
        app.mainloop()
    genLevel(app, level, right, Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"])

def Quick(app, level, right):      
    easyList = range(0, 21)
    def genLevel(app, level, right, bg):
        for i in app.place_slaves():
            i.destroy()
        
        def check(rightanswer, useranswer, right):
            try:
                if rightanswer == int(useranswer):
                    right += 1
            except:
                pass
            genLevel(app, level, right, bg)
        
        def quick_save_result(app, level, right, inMenu):
            app.protocol("WM_DELETE_WINDOW", app.destroy)
            foo = Data.download_statistics()
            level = 20
            foo["quick_mode"]["last"] = [right, level]
            try:
                if foo["quick_mode"]["last"][0] > foo["quick_mode"]["best"][0]:
                    foo["quick_mode"]["best"] = foo["quick_mode"]["last"]
            except ZeroDivisionError:
                pass
            Data.upload_statistics(src=foo)
            bar = round(right/level, ndigits=2)
            if bar >= 0.85:
                if Data.download_data()["root"]["lang"] == "eng":
                    recomended_mark = "A"
                else:
                    recomended_mark = 5
            elif (bar >= 0.65) and (bar < 0.85):
                if Data.download_data()["root"]["lang"] == "eng":
                    recomended_mark = "B"
                else:
                    recomended_mark = 4
            elif (bar >= 0.45) and (bar < 0.65):
                if Data.download_data()["root"]["lang"] == "eng":
                    recomended_mark = "C"
                else:
                    recomended_mark = 3
            else:
                if Data.download_data()["root"]["lang"] == "eng":
                    recomended_mark = "F"
                else:
                    recomended_mark = 2
            if bar == 1 and Data.download_data()["root"]["lang"] == "eng":
                recomended_mark = "S"
            elif bar == 1:
                recomended_mark = "5+"
            if Data.download_data()["root"]["sound"]:
                pygame.mixer.music.load("assets/music/menu/menu.mp3")
                pygame.mixer.music.play(loops=-1)
            tkinter.messagebox.showinfo("MathBasics", Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["quick_mode"]["labels"]["result"].format(right, recomended_mark))
            if inMenu:
                for i in app.place_slaves():
                    i.destroy()
                Menu(parent=app).pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
            else:
                lambda: app.destroy()
        
        level += 1
        problem = f"{random.choice(easyList)}*{random.choice(easyList)}"
        rightanswer = eval(problem)
        solves = [rightanswer,
                  rightanswer-random.randint(1, 5),
                  rightanswer+random.randint(1, 2),
                  rightanswer+random.randint(3, 5)]
        random.shuffle(solves)
        
        problemLabel = tkinter.Label(app,
                                     text = f'{Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["problem"]} {level}: {problem} =',
                                     font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 36, tkinter.font.BOLD),
                                     fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                     bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                     justify = tkinter.LEFT)
        
        x = 25
        y = 175
        for i in solves:
            tkinter.Button(app,
                           text = i,
                           font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 16),
                           fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                           bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"],
                           activeforeground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                           activebackground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                           command = lambda x=i: check(rightanswer, x, right)).place(x=x, y=y, width=400, height=75)

            y += 80
            if y > 255:
                x += 425
                y = 175

        currentResultLabel = tkinter.Label(app,
                                           text = f'{Data.get_lang(lang=Data.download_data()["root"]["lang"])["main"]["infinity"]["labels"]["currentlevel"]}:\n{right}/{level - 1}',
                                           font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 24, tkinter.font.BOLD),
                                           fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                           bg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                           justify = tkinter.LEFT)
        
        saveandquitBtn = tkinter.Button(app,
                                        text = Data.get_lang(lang=Data.download_data()["root"]["lang"])["about"]["buttons"]["back_button"],
                                        font = (Data.get_theme(theme=Data.download_data()["root"]["theme"])["font"], 16),
                                        fg = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        bg = "#dd0000", state=tkinter.DISABLED,
                                        activeforeground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["fgcolor"]["master"],
                                        activebackground = Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["master"],
                                        command = lambda: quick_save_result(app, level - 1, right, True))
        
        problemLabel.place(x = 25, y = 25)
        currentResultLabel.place(x = 25, y = 425)
        saveandquitBtn.place(x = int(app.geometry().split("x")[0]) - 400, y = int(app.geometry().split("x")[1].split("+")[0]) - 180, width = 225, height = 75)
        
        if level == 21:
            quick_save_result(app, level, right, True)

        app.mainloop()
    genLevel(app, level, right, Data.get_theme(theme=Data.download_data()["root"]["theme"])["bgcolor"]["extra"])

if __name__ == "__main__":
    pygame.mixer.init()
    mathbasics = App()
    mathbasics.mainloop()