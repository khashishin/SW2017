# -*- coding: utf-8 -*-
from Tkinter import *

def do_magic():
    pass

wojewodztwa = ['dolnoslaskie', 'kujawskopomorskie', 'lodzkie', 'lubelskie', 'lubuskie', 'malopolskie', 'mazowieckie', 'opolskie', 'podkarpackie', 'podlaskie', 'pomorskie', 'slaskie', 'swietokrzyskie', 'warminskomazurskie', 'wielkopolskie', 'zachodniopomorskie']
wojewodztwa_pl = ['dolnośląskie', 'kujawsko-pomorskie', 'łódzkie', 'lubelskie', 'lubuskie', 'małopolskie', 'mazowieckie', 'opolskie', 'podkarpackie', 'podlaskie', 'pomorskie', 'śląskie', 'świętokrzyskie', 'warmińsko-mazurskie', 'wielkopolskie', 'zachodniopomorskie']


master = Tk()
master.title("Wyszukaj")
master.geometry("350x370")
master.option_add("*Label.Font", "helvetica 10 bold")

listbox = Listbox(master)
for item in wojewodztwa_pl:
    listbox.insert(END, item)

w0 = Label(master, text="Geograficzne tagowanie treści wiadomości online")
# w0.config(font=("Arial", 10))
w1 = Label(master, text="Wybierz województwo")
w2 = Label(master, text="Wpisz zapytanie")
e = Entry(master)
b = Button(master, text="Wyszukaj i wyświetl wiadomości", command=do_magic())

listbox.config(height=16)

w0.pack()
w1.pack()
listbox.pack()
w2.pack()
e.pack()
b.pack()
mainloop()
