import time
import requests
from tkinter import *
from bs4 import BeautifulSoup

# ------------------- Dummy Text Web Scraping ------------------- #
DUMMY_TEXT_URL = "http://www.randomtextgenerator.com/"
word_count = 0
random_text = ""
random_words = []


def get_word():
    global word_count, random_text, random_words
    response = requests.get(DUMMY_TEXT_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    random_text = soup.find(id="generatedtext").getText().split("\n")[0].replace("/r", "")
    random_words = random_text.split()
    word_count = len(random_words)


get_word()

# ------------------- Program Logic ------------------- #
time_started = 0


def start_challenge():
    global time_started, random_text
    get_word()
    time_started = time.time()

    result_box.config(state=NORMAL)
    result_box.delete("1.0", "end")
    result_box.config(state=DISABLED)

    user_box.delete("1.0", "end")

    text_box.config(state=NORMAL)
    text_box.delete("1.0", "end")
    text_box.insert(INSERT, random_text)
    text_box.config(state=DISABLED)


def end_challenge():
    time_ended = time.time()
    global word_count, random_words
    player_words = user_box.get(1.0, "end-1c").split()
    right_words = 0
    words_per_minute = 0

    for _ in range(len(player_words)):
        if player_words[_] == random_words[_]:
            right_words += 1
            words_per_minute += 1
        else:
            user_box.insert(END, f"\n{player_words[_]}", 'error')

    accuracy_pct = round((right_words / word_count * 100), 2)
    words_per_minute = round((60 / (time_ended - time_started) * words_per_minute), 2)
    result_box.config(state=NORMAL)
    result_box.delete("1.0", "end")
    result_box.insert(INSERT, f"Your speed is {words_per_minute} words per minute, with a total accuracy of "
                              f"{accuracy_pct}%")
    result_box.config(state=DISABLED)

# ------------------- UI ------------------- #


window = Tk()
window.title("Typing Speed Test")
window.config(padx=20, pady=20)

title_label = Label(text="Text to copy", font=35)
title_label.grid(column=0, row=0, columnspan=2)

text_box = Text(window, padx=20, pady=20, height=5, font=("Helvetica", 16))
text_box.grid(column=0, row=1, columnspan=2)

user_box = Text(window, padx=20, pady=20, height=5, font=("Helvetica", 16))
user_box.tag_config('error', foreground="red")
user_box.grid(column=0, row=2, columnspan=2)

start_button = Button(window, text="Start Test", command=start_challenge)
start_button.grid(column=0, row=3)

end_button = Button(window, text="Check Result", command=end_challenge)
end_button.grid(column=1, row=3)

result_label = Label(text="Results", font=25, pady=20)
result_label.grid(column=0, row=4)

result_box = Text(window, padx=20, pady=20, height=1, font=("Helvetica", 16))
result_box.grid(column=1, row=4)
result_box.config(state=DISABLED)

window.mainloop()
