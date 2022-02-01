BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random
import os

screen = Tk()
current_card = {}
to_learn = {}

#kártya hátoldala
def flip_card():
    global current_card
    playing_card.itemconfig(playing_card_img, image=back_img)
    language_label.config(bg="#91c2af", fg="white")
    word_label.config(bg="#91c2af", fg="white")
    language_label.config(text="Magyar")
    hungarian_text = current_card["Magyar"]
    word_label.config(text=hungarian_text)

#tanulandó szavak adatbázis megnyitása
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # ha nincs fájl, megnyitja az összes szó adatbázist
    original_data = pandas.read_csv("data/hun_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # ha van, megnyitja a tanulandó szavakat
    to_learn = data.to_dict(orient="records")

# tanulandó szavak adatbázis kezelése
def is_known():
    if len(to_learn) == 0:
        os.remove("data/words_to_learn.csv")
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=0)
    right_button_command()
# ez a gomb törli a szót a tanulandó szavakból
def right_button_command():
    global flip_timer
    global current_card
    global to_learn
    if len(to_learn) == 0:
        os.remove("data/words_to_learn.csv")
    # kártya konfigurálása
    screen.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    current_word = current_card["English"]
    word_label.config(text=current_word)
    language_label.config(text="English")
    playing_card.itemconfig(playing_card_img, image=front_img)
    language_label.config(bg="white", fg="black")
    word_label.config(bg="white", fg="black")
    # időzítő elindítása, 3 mp után kártya megfordítás
    flip_timer = screen.after(3000, flip_card)


# rendelkezésre álló idő megadása(3mp)
flip_timer = screen.after(3000, flip_card)
# ablak konfigurálás
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
# képek elhelyezkedése
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

playing_card = Canvas(height=650, width=900, bg=BACKGROUND_COLOR, highlightthickness=0)
playing_card_img = playing_card.create_image(450, 280, anchor="center", image=front_img)
playing_card.grid(column=0, row=0)
# szöveg konfigurálás
language_label = Label(text="", font=("Arial", 40, "italic"), bg="white")
language_label.place(x=350, y=150)

word_label = Label(text="", font=("Arial", 60, "bold"), bg="white")
word_label.place(x=350, y=263)
# gombok konfigurálása
right_button = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
right_button.place(x=200, y=560)

left_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, command=right_button_command)
left_button.place(x=600, y=560)

right_button_command()
# ablak folyamatos frissítése
screen.mainloop()
