import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"

try:
    df = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("./data/french_words.csv")


to_learn = df.to_dict(orient="records")
list_of_french_words = df.French.to_list()
list_of_english_words = df.English.to_list()
current_card = {}


def update_card():
    global df
    global to_learn
    try:
        df = pandas.read_csv("./data/words_to_learn.csv")
    except FileNotFoundError:
        df = pandas.read_csv("./data/french_words.csv")

    to_learn = df.to_dict(orient="records")


def remove_card():
    global current_card
    global list_of_french_words
    global list_of_english_words
    list_of_french_words.remove(current_card["French"])
    list_of_english_words.remove(current_card["English"])
    new_data = pandas.DataFrame({"French": list_of_french_words, "English": list_of_english_words})
    new_data.to_csv('./data/words_to_learn.csv', index=False)
    update_card()
    next_card()


def next_card():
    global current_card
    global timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    current_french_word = current_card["French"]
    card_canvas.itemconfig(canvas_image, image=card_front_img)
    card_canvas.itemconfig(title_text, text="French", fill="black")
    card_canvas.itemconfig(word_text, text=current_french_word, fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    current_english_word = current_card["English"]
    card_canvas.itemconfig(canvas_image, image=card_back_img)
    card_canvas.itemconfig(title_text, text="English", fill="white")
    card_canvas.itemconfig(word_text, text=current_english_word, fill="white")
    window.after_cancel(timer)


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_image = card_canvas.create_image(400, 263, image=card_front_img)
card_canvas.grid(row=0, column=0, columnspan=2)
title_text = card_canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = card_canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), tag="word_tag")

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=remove_card)
right_button.grid(row=1, column=1)

timer = window.after(3000, flip_card)
next_card()

window.mainloop()
