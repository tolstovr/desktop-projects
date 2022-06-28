##
#-*-coding: utf-8-*-
#by: robertproducts

import tkinter
import tkinter.ttk
import random
import os
import os.path

colors = ["lightpink", "khaki", "powderblue"]

OPENED = 0

root = tkinter.Tk()
root.geometry("0x0-65536-65536")

class Note(tkinter.Toplevel):
    """This class describes one note window"""
    def __init__(self, fname:str, ftext:str):
        super().__init__()
        self.fname = fname
        self.ftext = ftext
        self.protocol("WM_DELETE_WINDOW", self.close_btn_pressed)
        self.title(f"MyNote - {self.fname}")
        self.iconbitmap("main.ico")
        self.attributes("-topmost", True)
        self.bg = random.choice(colors)
        self.config(bg=self.bg)
        self.geometry(f"400x400+{random.choice(range(100, self.winfo_screenwidth()-500, 100))}+{random.choice(range(100, self.winfo_screenheight()-500, 100))}")
        self.widgets()
    
    def widgets(self):
        self.space = tkinter.Text(self, font=("Times", 24), bg=self.bg)
        self.space.place(x=0, y=20, width=400, height=380)
        self.space.insert("end", self.ftext)

        self.add_btn = tkinter.Button(self, text="Добавить заметку", bg=self.bg,
                                      activebackground=self.bg,
                                      relief="flat",
                                      command=new_note)
        self.add_btn.place(x=0, y=0, width=200, height=20)   
        self.del_btn = tkinter.Button(self, text="Удалить заметку", bg=self.bg,
                                      activebackground=self.bg,
                                      relief="flat",
                                      command=self.del_btn_pressed)
        self.del_btn.place(x=200, y=0, width=200, height=20)      

    def close(self):
        self.destroy()
        global OPENED
        OPENED -= 1
        if (len(os.listdir("notes"))==0) or (OPENED == 0): raise SystemExit(0)

    def save(self):
        self.ftext = self.space.get("0.0", "end")
        if self.ftext.replace("/n", "").replace("/t", "") == "":
            self.del_btn_pressed()
        with open(f"notes/{self.fname}", "w", encoding="utf-8") as f:
            f.write(self.ftext)
    
    def close_btn_pressed(self):
        self.save()
        self.close()
    
    def del_btn_pressed(self):
        os.remove(f"notes/{self.fname}")
        self.close()

def show_note(fname:str):
    with open(f"notes/{fname}", "r", encoding="utf-8") as f:
        Note(fname, f.read())
    global OPENED
    OPENED += 1

def new_note(content=""):
    with open(f"notes/{len(os.listdir('notes'))}.txt", "w", encoding="utf-8") as f:
        f.write(content)
    show_note(str(len(os.listdir('notes'))-1)+".txt")

if __name__ == "__main__":
    assert os.getcwd()
    if not(os.path.exists("notes")): os.mkdir("notes")
    if len(os.listdir("notes")) == 0:
        new_note(content="Это ваша первая заметка! Напишите что-нибудь здесь...")
    else:
        for fname in os.listdir("notes"):
            show_note(fname)
    tkinter.mainloop()