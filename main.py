from tkinter import *
import pandas
from random import choice

FONT_NAME = "Ariel"
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

try:
    words_dataframe = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_dataframe = pandas.read_csv("data/french_words.csv")
    to_learn = words_dataframe.to_dict(orient="records")
else:
    to_learn = words_dataframe.to_dict(orient="records")


# ---------------------------------- CREATE NEW FLASHCARDS ----------------------------------
def new_flashcard():
    global current_card, flip_timer
    screen.after_cancel(flip_timer)
    current_card = choice(to_learn)
    card.itemconfig(card_image, image=card_front_img)
    card.itemconfig(card_title, text="French", fill="black")
    card.itemconfig(card_word, text=current_card["French"], fill="black")
    screen.after(3000, func=flip_card)


# ---------------------------------- FLIP THE FLASHCARD ----------------------------------
def is_known():
    global to_learn, current_card
    new_flashcard()
    to_learn.remove(current_card)
    df = pandas.DataFrame([i for i in to_learn])
    df.to_csv("data/words_to_learn.csv", index=False)


# ---------------------------------- FLIP THE FLASHCARD ----------------------------------
def flip_card():
    card.itemconfig(card_image, image=card_back_img)
    card.itemconfig(card_title, text="English", fill="white")
    card.itemconfig(card_word, text=current_card["English"], fill="white")


# ---------------------------------- USER INTERFACE ----------------------------------

screen = Tk()
screen.title("Flashy")
screen.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = screen.after(3000, func=flip_card)

card = Canvas(height=526, width=800, highlightthickness=0, background=BACKGROUND_COLOR)
card.grid(row=0, column=0, columnspan=2)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = card.create_image(400, 263, image=card_front_img)
card_title = card.create_text(400, 150, font=(FONT_NAME, 40, "italic"), text="")
card_word = card.create_text(400, 263, font=(FONT_NAME, 60, "bold"), text="")

x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=new_flashcard)
x_button.grid(row=1, column=0)

tick_image = PhotoImage(file="images/right.png")
tick_button = Button(image=tick_image, highlightthickness=0, command=is_known)
tick_button.grid(row=1, column=1)

new_flashcard()

screen.mainloop()
