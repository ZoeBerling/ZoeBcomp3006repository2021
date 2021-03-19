import csv
import string
import numpy as np

from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
import keras.utils as ku
from numpy.random import seed
seed(1)



tokenizer = Tokenizer()


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

    black_sequences, total_black = sequence_of_tokens(black_c)
    predictors, label, max_len = padded_sequences(black_sequences, total_black)
    model1 = create_model(max_len, total_black)
    model1.fit(predictors, label, epochs=100, verbose=5)
    model1.summary()
    print(generate_text("happy", 5, model1, max_len))
    print(generate_text("horrible", 4, model1, max_len))
    print(generate_text("funny", 5, model1, max_len))
    print(generate_text("ugly", 5, model1, max_len))
    print(generate_text("scary", 6, model1, max_len))
    print(generate_text("mother", 5, model1, max_len))
    print(generate_text("father", 10, model1, max_len))


def clean(ttext, punct):
    ttext = "".join(v for v in ttext if v not in punct).lower()
    ttext = ttext.encode("utf8").decode("ascii", 'ignore')
    return ttext


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
        predicted = model.predict_classes(sequence, verbose=0)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text.title()


if __name__ == '__main__':
    main()