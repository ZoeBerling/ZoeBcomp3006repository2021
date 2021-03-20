import csv
import string

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
import keras.utils as ku

import numpy as np
from numpy.random import seed
import random

import tkinter as tk
seed(1)


tokenizer = Tokenizer()
MAX_CARDS = 30
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
CARD_WIDTH = 450
CARD_HEIGHT = 325

CANVAS = 1
GENERATE = 0
def main():
    c = 'cards.csv'
    white = []
    black = []
    punct = set(string.punctuation)  # create a set of punctuation
    with open(c) as card_csv:
        csv_file = csv.reader(card_csv)
        for text, tag in csv_file:
            if text:
                if '_____' in text:
                    # text = text.replace("-", " ")  # Assume '-' is used as ' '
                    white.append(text)

                else:  # Add cards without spaces to black card deck
                    # text = text.replace("-", " ")  # Assume '-' is used as ' '
                    black.append(text)

    card_csv.close()

    black_c = [clean(text, punct) for text in black]

    if GENERATE == 1:
        generate_machine(black_c)

    if CANVAS == 1:
        create_canvas('generated cards.csv', white)


def generate_machine(black_c):

    black_sequences, total_black = sequence_of_tokens(black_c)
    predictors, label, max_len = padded_sequences(black_sequences, total_black)
    model1 = create_model(max_len, total_black)
    model1.fit(predictors, label, epochs=50, verbose=5)
    model1.summary()
    #
    black_w = [item.split() for item in black_c]
    display_cards = []
    for i in range(MAX_CARDS): # Generate x amount of cards and save them to a list
        random_item = black_w[random.randint(0, len(black_w))]
        random_word = random_item[random.randint(0,len(random_item)-1)]
        print(random_item)
        print(random_word)
        # generate = generate_text(black_c[random.randint(0, len(black_c))], random.randint(4, 7), model1, max_len)
        generate = generate_text(random_word, random.randint(4, 7), model1, max_len)
        display_cards.append(generate)

    with open("generated cards.csv", 'ab') as p_csv:
        np.savetxt(p_csv, display_cards, fmt= '%s')



def create_canvas(d, white):
    display_cards = []
    with open(d) as c:
        for text in c:
            display_cards.append(text)


    canvas = makeCanvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Boards Resistant to Mortals')
    canvas.bind("<Button-1>", lambda e: mousePress(e, canvas, display_cards, white))

    draw_cards(canvas, 1, 'black')  # create black cards on the right
    draw_cards(canvas, 0, 'white')  # create white cards on the left
    write_txt(canvas, display_cards, 1, 'black')  # create white text
    write_txt(canvas, white, 0, 'white')  # create white text

    canvas.mainloop()

def write_txt(canvas, cards, a, color):
    x = (a * CANVAS_WIDTH / 2) + 20
    y = (CANVAS_HEIGHT / 2) - CARD_HEIGHT

    if color == 'black':
        fc = 'white'
    else:
        fc = 'black'

    canvas.create_text(x + (CARD_WIDTH / 2), y * 10, font='Helvetica 27 bold',
                       text=cards[0],
                       fill=fc, justify=tk.CENTER, tags=color, width=310)


def draw_cards(canvas, a, color=None):

    x = (a* CANVAS_WIDTH/2) + 20
    y = (CANVAS_HEIGHT / 2) - CARD_HEIGHT

    canvas.create_rectangle(x, y, x + CARD_WIDTH, y + (CARD_HEIGHT*1.75), fill=color, outline='black', )
    # canvas.create_text(CANVAS_WIDTH/2 + a * (CARD_WIDTH/2), CARD_HEIGHT, font='Helvetica  bold', text=display_cards[0],
                       # fill='black', justify=tk.CENTER, tags=color, width=300)


def mousePress(event, canvas, display_cards, white):
    """Track mouse clicks to play the game on the tkinter canvas"""
    # print('mouse pressed', event.x, event.y)
    x = event.x
    y = event.y
    found = canvas.find_overlapping(x, y, x, y)

    if found[0] > 0:
        print(found)
        if found[0] == 1:
            print('black')
            canvas.delete('black')
            canvas.update()
            revealCards(display_cards, found)
            write_txt(canvas, display_cards, 1, 'black') # create white text
            canvas.update()
        elif found[0] == 2:
            canvas.delete('white')
            canvas.update()
            revealCards(white, found)
            write_txt(canvas, white, 0, 'white')  # create white text
            canvas.update()


def revealCards(card_list, m=None):
    while m is None:
        continue
    if m is not None:
        card_list.pop(0)


def makeCanvas(width, height, title):
    """make the window that contains the canvas"""

    top = tk.Tk()
    top.minsize(width=width, height=height)
    top.title(title)

    canvas = tk.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly. I got this from my last project
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off. I got this from my last project

    return canvas


def clean(ttext, punct):
    ttext = "".join(v for v in ttext if v not in punct).lower()
    ttext = ttext.encode("utf8").decode("ascii", 'ignore')
    return ttext

def word_split(card, stop, exclude, lemma, z= False):
    """Clean card by getting rid of stop words and punctuation. Return normalized item"""

    if z == False:
        stop_free = " ".join([i for i in card.lower().split() if i not in stop])
        # print(type(stop_free))
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        # print(punc_free)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    else:
        punc_free = ''.join(ch for ch in card.lower() if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())

    return normalized

def sequence_of_tokens(txt):
    ## tokenization
    tokenizer.fit_on_texts(txt)
    total_words = len(tokenizer.word_index) + 1

    ## convert data to sequence of tokens
    input_sequences = []
    for line in txt:
        sequence = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(sequence)):
            n_gram_sequence = sequence[:i + 1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words


def padded_sequences(input_sequences, total_words):
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    label = ku.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len


def create_model(max_sequence_len, total_words):
    input_len = max_sequence_len - 1
    model = Sequential()

    # Add Input Embedding Layer
    model.add(Embedding(total_words, 10, input_length=input_len))

    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(100))
    model.add(Dropout(0.1))

    # Add Output Layer
    model.add(Dense(total_words, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


def generate_text(seed_text, num_words, model, max_sequence_len):
    for _ in range(num_words):
        sequence = tokenizer.texts_to_sequences([seed_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_sequence_len - 1, padding='pre')
        #  predicted = model.predict_classes(sequence, verbose=0)
        predicted = np.argmax(model.predict(sequence, verbose=0))

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text.title()


if __name__ == '__main__':
    main()