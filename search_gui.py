# -*- coding: utf-8 -*-
from Tkinter import *
import crawler

wojewodztwa = ['dolnoslaskie', 'kujawskopomorskie', 'lodzkie', 'lubelskie', 'lubuskie', 'malopolskie', 'mazowieckie', 'opolskie', 'podkarpackie', 'podlaskie', 'pomorskie', 'slaskie', 'swietokrzyskie', 'warminskomazurskie', 'wielkopolskie', 'zachodniopomorskie']
wojewodztwa_pl = ['dolnośląskie', 'kujawsko-pomorskie', 'łódzkie', 'lubelskie', 'lubuskie', 'małopolskie', 'mazowieckie', 'opolskie', 'podkarpackie', 'podlaskie', 'pomorskie', 'śląskie', 'świętokrzyskie', 'warmińsko-mazurskie', 'wielkopolskie', 'zachodniopomorskie']

master = Tk()
master.title("Wyszukaj")
master.geometry("350x370")
master.option_add("*Label.Font", "helvetica 10 bold")

listbox = Listbox(master)
listbox.config(height=16)

def do_magic():
    crawler.main(target_wojewodztwo=wojewodztwa[int(listbox.curselection()[0])], query= e.get())
    print wojewodztwa[int(listbox.curselection()[0])], e.get()

for item in wojewodztwa_pl:
    listbox.insert(END, item)

title = Label(master, text="Geograficzne tagowanie treści wiadomości online")
label1 = Label(master, text="Wybierz województwo")
label2 = Label(master, text="Wpisz zapytanie")
e = Entry(master)
b = Button(master, text="Wyszukaj i wyświetl wiadomości", command=do_magic)


title.pack()
label1.pack()
listbox.pack()
label2.pack()
e.pack()
b.pack()
mainloop()

