##
#-*-coding: utf-8-*-
#by: robertproducts

import tkinter
import tkinter.font
import tkinter.messagebox
import tkinter.ttk

import os
import random
import datetime
import webbrowser
import pygame.mixer
import time
import json

pygame.mixer.init()

def achievement(achievement=str):
    if os.path.exists(".disableachievements"):return
    with open("data/achievements.json", "r", encoding="utf-8") as f:
        d = json.load(f)
        if not(d[achievement]):
            tkinter.messagebox.showinfo(data.lang()["achievements"]["title"], data.lang()["achievements"]["achievement_made"]+": "+data.lang()["achievements"][achievement]+"!")
            d[achievement] = not(d[achievement])
    with open("data/achievements.json", "w", encoding="utf-8") as f:
        json.dump(d, f)

class data:
    def get(src="data/main.json"):
        with open(src, "r", encoding="utf-8") as f: return json.load(f)
    
    def push(src=dict, path="data/main.json"):
        with open(path, "w", encoding="utf-8") as f: json.dump(src, f)
    
    def theme():
        with open("data/main.json", "r", encoding="utf-8") as f:
            with open(json.load(f)["theme"], "r", encoding="utf-8") as t:
                return json.load(t)

    def lang():
        with open("data/main.json", "r", encoding="utf-8") as f:
            with open(json.load(f)["lang"], "r", encoding="utf-8") as l:
                return json.load(l)

    def sound():
        with open("data/main.json", "r", encoding="utf-8") as f:return json.load(f)["sound"]

    def switch_sound():
        d = data.get()
        d["sound"] = not(d["sound"])
        data.push(src=d)
        if d["sound"]:
            pygame.mixer.music.load("assets/sounds/menu.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()
            pygame.mixer.stop()

    def switch_theme():
        themes = os.listdir("assets/themes")
        last_data = data.get()
        cur_index = themes.index(last_data["theme"].split("/")[-1])
        if cur_index == len(themes) - 1:
            cur_index = 0
        else:
            cur_index += 1
        last_data["theme"] = "assets/themes/"+themes[cur_index]
        data.push(src=last_data)

    def switch_lang():
        locales = os.listdir("assets/locales")
        last_data = data.get()
        cur_index = locales.index(last_data["lang"].split("/")[-1])
        if cur_index == len(locales) - 1:
            cur_index = 0
        else:
            cur_index += 1
        last_data["lang"] = "assets/locales/"+locales[cur_index]
        data.push(src=last_data)
    
    def splash():
        with open("assets/topsecret.txt", "r", encoding="utf-8") as f:
            return random.choice(f.read().split(";"))

class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("EXECUTE!")
        self.geometry(f"1280x720+{self.winfo_screenwidth()//2 - 640}+48")
        self.resizable(False, False)
        self.iconbitmap(data.get()["icon"])
        self.config(bg=data.theme()["bg"])

        if data.sound():
            pygame.mixer.music.load("assets/sounds/menu.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1)

        if datetime.datetime.now().month == 4 and datetime.datetime.now().day == 10:achievement(achievement="enter_on_birthday")
        if os.path.exists("lorem"):achievement(achievement="lorem")

        Menu(parent=self).pack(side="top", expand=1, fill="both")

class Menu(tkinter.Frame):
    def __init__(self, parent=tkinter.Tk):
        super().__init__()
        self.parent = parent
        self.parent.title("EXECUTE!")
        self.config(bg=data.theme()["bg"])
        self.widgets()

        mxs = 0
        for fl in os.listdir("results"):
            with open("results/"+fl, "r", encoding="utf-8") as f:
                if "100.0%" in f.read():mxs += 1
                if "0.0%" in f.read():achievement(achievement="wrong_all_answers")
            
            if len(os.listdir("results")) == 1:achievement(achievement="first_test_passed")
            if len(os.listdir("results")) == mxs == 1:achievement(achievement="first_test_passed_max")
            if len(os.listdir("results")) == 5:achievement(achievement="five_tests_passed")
            if len(os.listdir("results")) == mxs == 5:achievement(achievement="five_tests_passed_max")
            if len(os.listdir("results")) == 10:achievement(achievement="ten_tests_passed")
            if len(os.listdir("results")) == mxs == 10:achievement(achievement="ten_tests_passed_max")
            if len(os.listdir("results")) == 20:achievement(achievement="twenty_tests_passed")
            if len(os.listdir("results")) == mxs == 20:achievement(achievement="twenty_tests_passed_max")
            if len(os.listdir("results")) == 100:achievement(achievement="hundred_tests_passed")
            if len(os.listdir("results")) == mxs == 100:achievement(achievement="hundred_test_passed_max")

    def widgets(self):
        self.title = tkinter.Label(self,
                                   text="EXECUTE!",
                                   fg=data.theme()["fg"],
                                   bg=data.theme()["bg"],
                                   font=(data.theme()["font"], 48, tkinter.font.BOLD))
        
        self.start_btn = tkinter.Button(self,
                                        text=data.lang()["menu"]["start_btn"],
                                        fg=data.theme()["fg_"],
                                        bg=data.theme()["bg_"],
                                        activeforeground=data.theme()["fg"],
                                        activebackground=data.theme()["bg"],
                                        font=(data.theme()["font"], 24),
                                        command=self.start_btn_pressed)
        
        self.about_btn = tkinter.Button(self,
                                        text=data.lang()["menu"]["about_btn"],
                                        fg=data.theme()["fg_"],
                                        bg=data.theme()["bg_"],
                                        activeforeground=data.theme()["fg"],
                                        activebackground=data.theme()["bg"],
                                        font=(data.theme()["font"], 24),
                                        command=self.about_btn_pressed)
                                        
        self.quit_btn = tkinter.Button(self,
                                       text=data.lang()["menu"]["quit_btn"],
                                       fg=data.theme()["bg_"],
                                       bg="#cc0000",
                                       activeforeground=data.theme()["bg"],
                                       activebackground="#dd0000",
                                       font=(data.theme()["font"], 24),
                                       command=self.quit_btn_pressed)

        self.quit_btn.bind("<Enter>", func=lambda x: self.quit_btn.config(text=data.lang()["menu"]["true_quit_btn"]))
        self.quit_btn.bind("<Leave>", func=lambda x: self.quit_btn.config(text=data.lang()["menu"]["quit_btn"]))

        self.sound_btn = tkinter.Button(self,
                                        text=data.lang()["menu"]["sound_btn"],
                                        fg=data.theme()["fg_"],
                                        bg=data.theme()["bg_"],
                                        activeforeground=data.theme()["fg"],
                                        activebackground=data.theme()["bg"],
                                        font=(data.theme()["font"], 12),
                                        command=self.sound_btn_pressed)

        self.theme_btn = tkinter.Button(self,
                                        text=data.lang()["menu"]["theme_btn"],
                                        fg=data.theme()["fg_"],
                                        bg=data.theme()["bg_"],
                                        activeforeground=data.theme()["fg"],
                                        activebackground=data.theme()["bg"],
                                        font=(data.theme()["font"], 12),
                                        command=self.theme_btn_pressed)

        self.lang_btn = tkinter.Button(self,
                                       text=data.lang()["menu"]["lang_btn"],
                                       fg=data.theme()["fg_"],
                                       bg=data.theme()["bg_"],
                                       activeforeground=data.theme()["fg"],
                                       activebackground=data.theme()["bg"],
                                       font=(data.theme()["font"], 12),
                                       command=self.lang_btn_pressed)

        self.credits = tkinter.Label(self,
                                     text="v.2022.05.25\nUnlimited edition",
                                     fg=data.theme()["fg"],
                                     bg=data.theme()["bg"],
                                     font=(data.theme()["font"], 14),
                                     justify="right")

        self.theme_btn.bind("<Enter>", func=lambda x: self.theme_btn.config(text=data.theme()["title"]))
        self.theme_btn.bind("<Leave>", func=lambda x: self.theme_btn.config(text=data.lang()["menu"]["theme_btn"]))

        self.lang_btn.bind("<Enter>", func=lambda x: self.lang_btn.config(text=data.lang()["title"]))
        self.lang_btn.bind("<Leave>", func=lambda x: self.lang_btn.config(text=data.lang()["menu"]["lang_btn"]))

        self.sound_btn.bind("<Enter>", func=lambda x: self.sound_btn.config(text="true" if data.get()["sound"] else "false"))
        self.sound_btn.bind("<Leave>", func=lambda x: self.sound_btn.config(text=data.lang()["menu"]["sound_btn"]))

        self.title.place(x=640, y=25, anchor="n")
        self.start_btn.place(x=640, y=225, anchor="n", width=384, height=75)
        self.about_btn.place(x=640, y=305, anchor="n", width=384, height=75)
        self.quit_btn.place(x=640, y=385, anchor="n", width=384, height=75)

        self.credits.place(x=1280, y=720, anchor="se")

        self.sound_btn.place(x=5, y=600, width=128, height=35)
        self.theme_btn.place(x=5, y=640, width=128, height=35)
        self.lang_btn.place(x=5, y=680, width=128, height=35)

    def start_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        self.destroy()
        Choose(parent=self.parent).pack(side="top", expand=1, fill="both")
    
    def about_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        self.destroy()
        About(parent=self.parent).pack(side="top", expand=1, fill="both")
    
    def quit_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        self.parent.destroy() #бессердечная ты сволочь!
    
    def theme_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        data.switch_theme()
        achievement(achievement="theme_changed")
        self.destroy()
        self.parent.config(bg=data.theme()["bg"])
        Menu(parent=self.parent).pack(side="top", expand=1, fill="both")

    def sound_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        data.switch_sound()
        if not(data.get()["sound"]):achievement(achievement="sound_off")
        pygame.mixer.stop()
        pygame.mixer.init()

    def lang_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        data.switch_lang()
        achievement(achievement="lang_changed")
        self.destroy()
        Menu(parent=self.parent).pack(side="top", expand=1, fill="both")

class Choose(tkinter.Frame):
    def __init__(self, parent=tkinter.Tk):
        super().__init__()
        self.parent = parent
        self.config(bg=data.theme()["bg"])
        self.widgets()
    
    def widgets(self):
        self.back_btn = tkinter.Button(self,
                                       text=data.lang()["about"]["back_btn"],
                                       fg=data.theme()["bg_"],
                                       bg="#cc0000",
                                       activeforeground=data.theme()["bg"],
                                       activebackground="#dd0000",
                                       font=(data.theme()["font"], 24),
                                       command=self.back_btn_pressed)

        self.title = tkinter.Label(self,
                                   text=data.lang()["choose"]["title"],
                                   fg=data.theme()["fg"],
                                   bg=data.theme()["bg"],
                                   font=(data.theme()["font"], 48, tkinter.font.BOLD))

        self.chooseListbox = tkinter.Listbox(self,
            bg=data.theme()["bg_"], fg=data.theme()["fg"],
            selectbackground=data.theme()["fg_"],
            selectforeground=data.theme()["bg"],
            font=(data.theme()["font"], 16, tkinter.font.BOLD),
            width=40, height=10)

        if len(os.listdir("levels")) == 0:
            self.startButton.config(state="disabled")
        else:
            for i in os.listdir("levels"):
                if i.endswith(".json"):
                    self.chooseListbox.insert(tkinter.END, i)
            self.chooseListbox.select_set(0)
            self.chooseListbox.event_generate("<<ListboxSelect>>")

        self.sel_btn = tkinter.Button(
            self, text=data.lang()["choose"]["sel_btn"], fg=data.theme()["fg"],
            bg=data.theme()["bg_"], activeforeground = data.theme()["fg_"],
            activebackground = data.theme()["bg"], font=(data.theme()["font"], 16),
            command=self.start)
        
        self.dirButton = tkinter.Button(
            self, text=data.lang()["choose"]["dir_btn"], fg=data.theme()["fg"],
            bg=data.theme()["bg_"], activeforeground = data.theme()["fg_"],
            activebackground = data.theme()["bg"], font=(data.theme()["font"], 16),
            command=self.dir_btn_pressed)

        self.chooseListbox.place(x=640, y=225, anchor="n", height=315)
        self.sel_btn.place(x=640-125-5, y=545, anchor="n", width=250, height=75)
        self.dirButton.place(x=640+125+5, y=545, anchor="n", width=250, height=75)
        
        self.back_btn.place(x=25, y=720-25, width=192, height=75, anchor="sw")
        self.title.place(x=640, y=25, anchor="n")
    
    def start(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        test = self.chooseListbox.get(self.chooseListbox.curselection()[0])
        self.destroy()
        letstarttest(testname=test, parent=self.parent)

    def dir_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        os.startfile("levels")

    def back_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        self.destroy()
        Menu(parent=self.parent).pack(side="top", expand=1, fill="both")

class About(tkinter.Frame):
    def __init__(self, parent=tkinter.Tk):
        super().__init__()
        self.parent = parent
        self.parent.title("EXECUTE! - О приложении")
        self.config(bg=data.theme()["bg"])
        self.widgets()
    
    def widgets(self):
        self.title = tkinter.Label(self,
                                   text=data.lang()["about"]["title"],
                                   fg=data.theme()["fg"],
                                   bg=data.theme()["bg"],
                                   font=(data.theme()["font"], 36, tkinter.font.BOLD))
        
        self.back_btn = tkinter.Button(self,
                                      text=data.lang()["about"]["back_btn"],
                                      fg=data.theme()["bg_"],
                                      bg="#cc0000",
                                      activeforeground=data.theme()["bg"],
                                      activebackground="#dd0000",
                                      font=(data.theme()["font"], 24),
                                      command=self.back_btn_pressed)

        self.dev = tkinter.Label(self,
                                 text=data.lang()["about"]["dev"].format("robertproducts".upper()),
                                 fg=data.theme()["fg"],
                                 bg=data.theme()["bg"],
                                 font=(data.theme()["font"], 24),
                                 justify="left")

        self.gfx = tkinter.Label(self,
                                 text=data.lang()["about"]["gfx"].format("robertproducts".upper()),
                                 fg=data.theme()["fg"],
                                 bg=data.theme()["bg"],
                                 font=(data.theme()["font"], 24),
                                 justify="left")

        self.sfx = tkinter.Label(self,
                                 text=data.lang()["about"]["sfx"].format("royalty free".upper()),
                                 fg=data.theme()["fg"],
                                 bg=data.theme()["bg"],
                                 font=(data.theme()["font"], 24),
                                 justify="left")

        self.ide = tkinter.Label(self,
                                 text=data.lang()["about"]["dev"].format("robertproducts".upper()),
                                 fg=data.theme()["fg"],
                                 bg=data.theme()["bg"],
                                 font=(data.theme()["font"], 24),
                                 justify="left")

        self.vk = tkinter.PhotoImage(file=f"assets/images/vk.gif")
        self.tg = tkinter.PhotoImage(file=f"assets/images/tg.gif")
        self.ig = tkinter.PhotoImage(file=f"assets/images/ig.gif")
        self.ok = tkinter.PhotoImage(file=f"assets/images/ok.gif")
        self.yt = tkinter.PhotoImage(file=f"assets/images/yt.gif")

        self.yt_btn = tkinter.Button(self,
                                     image=self.yt,
                                     compound = "left",
                                     bg = "#000000",
                                     activebackground="#000000",
                                     command=lambda:self.social(link="https://www.youtube.com/channel/UCLqk9zFK3-wGRsQE-htEooQ"))

        self.ok_btn = tkinter.Button(self,
                                     image=self.ok,
                                     compound = "left",
                                     bg = "#000000",
                                     activebackground="#000000",
                                     command=lambda:self.social(link="https://ok.ru/profile/574412470942?utm_campaign=web_share&utm_content=profile"))

        self.ig_btn = tkinter.Button(self,
                                     image=self.ig,
                                     compound = "left",
                                     bg = "#000000",
                                     activebackground="#000000",
                                     command=lambda:self.social(link="https://instagram.com/robertproducts"))

        self.tg_btn = tkinter.Button(self,
                                     image=self.tg,
                                     compound = "left",
                                     bg = "#000000",
                                     activebackground="#000000",
                                     command=lambda:self.social(link="https://t.me/robertproducts"))

        self.vk_btn = tkinter.Button(self,
                                     image=self.vk,
                                     compound = "left",
                                     bg = "#000000",
                                     activebackground="#000000",
                                     command=lambda:self.social(link="https://vk.com/robertproducts"))

        self.web_btn = tkinter.Button(self,
                                      text="Веб-сайт",
                                      bg = "#000000",
                                      activebackground="#000000",
                                      fg="#ffffff",
                                      activeforeground="#ffffff",
                                      font=("Courier", 14),
                                      command=lambda:self.social(link="https://robertproducts.netlify.app"))

        self.title.place(x=25, y=25)
        self.dev.place(x=50, y=125, height=75)
        self.gfx.place(x=50, y=205, height=75)
        self.sfx.place(x=50, y=285, height=75)
        self.ide.place(x=50, y=365, height=75)

        self.yt_btn.place(x=1280-25, y=720-100, width=54, height=54, anchor="ne")
        self.ok_btn.place(x=1280-25-54-5, y=720-100, width=54, height=54, anchor="ne")
        self.ig_btn.place(x=1280-25-54-5-54-5, y=720-100, width=54, height=54, anchor="ne")
        self.tg_btn.place(x=1280-25-54-5-54-5-54-5, y=720-100, width=54, height=54, anchor="ne")
        self.vk_btn.place(x=1280-25-54-5-54-5-54-5-54-5, y=720-100, width=54, height=54, anchor="ne")
        self.web_btn.place(x=1280-25-54-5-54-5-54-5-54-5-54-5, y=720-100, width=216, height=54, anchor="ne")

        self.back_btn.place(x=25, y=720-25, width=192, height=75, anchor="sw")
    
    def back_btn_pressed(self):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        self.destroy()
        Menu(parent=self.parent).pack(side="top", expand=1, fill="both")
    
    def social(self, link=str):
        if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
        webbrowser.open(link, new="2")
        if link == "https://robertproducts.netlify.app":achievement(achievement="web_check")
        else:achievement(achievement="social_check")

def letstarttest(testname=str, parent=tkinter.Tk):
    pygame.mixer.music.stop()
    if data.sound():
        pygame.mixer.music.load("assets/sounds/main.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
    parent.title("EXECUTE! - "+testname)
    with open("levels/"+testname, "r", encoding="utf-8") as f: test = json.load(f)
    tkinter.messagebox.showinfo("Информация перед началом теста", test["intro"])
    
    def genLevel(app=tkinter.Tk, level=int, right=int, test=dict):
        def check(useranswers, right, test=dict, question=list(test["test"])[level]):
            if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
            if test["test"][question]["type"] == "btn":
                if useranswers:
                    right += 1
            elif test["test"][question]["type"]=="ent":
                if test["test"][question]["answer"].lower() == useranswers.lower():
                    right += 1
            elif test["test"][question]["type"]=="ent!":
                if test["test"][question]["answer"] == useranswers:
                    right += 1
            if level+1 > len(test):
                result(app, len(test["test"]), right, True, test=test)
            else:
                genLevel(app=app, level=level, right=right, test=test)
        
        def result(app, total, right, inMenu, test=dict):
            total += 1
            percent = round(right/(total-1), ndigits=2)*100
            mark = 2
            annotation_key = "2"
            if percent >= 45:
                mark = 3
                annotation_key = "3"
            if percent >= 65:
                mark = 4
                annotation_key = "4"
            if percent >= 85:
                mark = 5
                annotation_key = "5"
            if percent == 100:
                mark = "5+"
                annotation_key = "5+"
            if percent > 100:
                mark = 6
                annotation_key = "WTF, dude"
            tkinter.messagebox.showinfo("EXECUTE!", data.lang()["main"]["res_msg_box"].format(right, total-1, percent, mark, test["outro"][annotation_key]))
            with open(f"results/{testname}.txt", "a", encoding="utf-8") as f:
                f.write(f"lvl: {testname}, res: {mark} ({right}/{total-1} = {percent}%)\n")
            if inMenu:
                for i in app.place_slaves():
                    i.destroy()
                if data.sound():
                    pygame.mixer.music.load("assets/sounds/menu.mp3")
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(loops=-1)
                Menu(parent=app).pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
            else:
                lambda: app.destroy()

        question = list(test["test"])[level]
        level += 1
        
        for i in app.place_slaves():
            i.destroy()
        
        problemLabel = tkinter.Label(app,
                                     text=data.lang()["main"]["question"].format(level, list(test["test"])[level-1]),
                                     font=(data.theme()["font"], 14),
                                     fg=data.theme()["fg"], bg=data.theme()["bg"],
                                     justify = tkinter.LEFT)
        
        x = 25
        y = 175
        if test["test"][question]["type"] == "btn":
            solves = list(test["test"][question]["answer"])
            random.shuffle(solves)
            for i in range(len(solves)):
                tkinter.Button(app,
                        text=solves[i],
                        font=(data.theme()["font"], 16),
                        fg=data.theme()["fg"],
                        bg=data.theme()["bg_"],
                        activeforeground=data.theme()["fg_"],
                        activebackground=data.theme()["bg"],
                        command=lambda x=test["test"][question]["answer"][solves[i]]: check(x, right, test=test)
                        ).place(x=x, y=y, width=550, height=75)
                y += 80
                if y > 495:
                    x += 555
                    y = 175
        elif test["test"][question]["type"] == "ent":
            tkinter.Label(app,
                            text=data.lang()["main"]["answer"],
                            font = (data.theme()["font"], 24, tkinter.font.BOLD),
                            fg = data.theme()["fg"],
                            bg = data.theme()["bg"],
                            justify = tkinter.RIGHT).place(x=x, y=y)

            space = tkinter.Entry(app,
                                  font = (data.theme()["font"], 24, tkinter.font.BOLD),
                                  fg = data.theme()["fg"],
                                  bg = data.theme()["bg"],
                                  justify = tkinter.LEFT)
            space.delete(0, tkinter.END)
            space.place(x=1280-x, y=y, anchor="ne")
            
            sendBtn =  tkinter.Button(app,
                                        text=data.lang()["main"]["send_btn"],
                                        font=(data.theme()["font"], 16),
                                        fg=data.theme()["fg"],
                                        bg="#00dd00",
                                        activeforeground=data.theme()["fg"],
                                        activebackgroun=data.theme()["bg"],
                                        command=lambda: check(space.get(), right, question=question, test=test))
            
            sendBtn.place(x = int(1280) - 25, y = 720 - 180, width = 225, height = 75, anchor="ne")
        elif test["test"][question]["type"] == "ent!":
            tkinter.Label(app,
                            text=data.lang()["main"]["answer"],
                            font = (data.theme()["font"], 24, tkinter.font.BOLD),
                            fg = data.theme()["fg"],
                            bg = data.theme()["bg"],
                            justify = tkinter.RIGHT).place(x=x, y=y)

            space = tkinter.Entry(app,
                                    font = (data.theme()["font"], 24, tkinter.font.BOLD),
                                    fg = data.theme()["fg"],
                                    bg = data.theme()["bg"],
                                    justify = tkinter.LEFT)
            space.delete(0, tkinter.END)
            space.place(x=1280-x, y=y, anchor="ne")
            
            sendBtn =  tkinter.Button(app,
                                        text=data.lang()["main"]["send_btn"],
                                        font=(data.theme()["font"], 16),
                                        fg=data.theme()["fg"],
                                        bg="#00dd00",
                                        activeforeground=data.theme()["fg"],
                                        activebackgroun=data.theme()["bg"],
                                        command=lambda: check(space.get(), right, question=question, test=test))
            
            sendBtn.place(x = int(1280) - 25, y = 720 - 180, width = 225, height = 75, anchor="ne")
    
        currentResultLabel = tkinter.Label(app,
                                           text = data.lang()["main"]["passed"].format(right, len(test["test"])),
                                           font = (data.theme()["font"], 14),
                                           fg = data.theme()["fg"],
                                           bg = data.theme()["bg"],
                                           justify = tkinter.RIGHT)
        
        def saveandquitBtn_pressed(app, total, right, inMenu, test=dict):
            if data.sound():pygame.mixer.Sound("assets/sounds/click.mp3").play()
            if tkinter.messagebox.askyesno("EXECUTE!", data.lang()["main"]["ask_msg_box"]):
                result(app, total, right, inMenu, test=test)

        saveandquitBtn = tkinter.Button(app,
                                        text=data.lang()["about"]["back_btn"],
                                        font=(data.theme()["font"], 16),
                                        fg=data.theme()["fg"],
                                        bg="#dd0000",
                                        activeforeground=data.theme()["fg"],
                                        activebackgroun=data.theme()["bg"],
                                        command=lambda: saveandquitBtn_pressed(app, len(test["test"]), right, True, test=test))
        
        problemLabel.place(x = 25, y = 25)
        currentResultLabel.place(x = int(1280) - 300, y = 720 - 100, anchor="ne")
        saveandquitBtn.place(x = int(1280) - 25, y = 720 - 100, width = 225, height = 75, anchor="ne")

        app.mainloop()
    genLevel(app=parent, level=0, right=0, test=test)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
