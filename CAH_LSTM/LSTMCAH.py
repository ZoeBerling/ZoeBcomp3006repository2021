import csv
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pad_sequence
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

import string
import gensim
from gensim import corpora
import re
import random

# keras module for building LSTM
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku

# set seeds for reproducability
import tensorflow
from numpy.random import seed
tensorflow.random.set_seed(2)
seed(1)

import pandas as pd
import numpy as np
import string, os

# import warnings
# warnings.filterwarnings("ignore")
# warnings.simplefilter(action='ignore', category=FutureWarning)

"""Zoe Berling
Some code I might want for later:
# add_space = ['$', '£', '¥', '¢', '¤', '®', '©', 'ª', 'º', '°', '-']
# print(re.findall(r"(?=("+'|'.join(add_space)+r"))", card))"""
t = Tokenizer()

def main():
    c = 'cards.csv'
    white = []
    black = []
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

    stop = set(stopwords.words('english'))  # create a set of stopwords from NLTK library
    punct = set(string.punctuation)  # create a set of punctuation
    lemmatizer = WordNetLemmatizer()  #  link words with similar meaning to one key word

    # clean the text
    white_c = [clean(text, punct).split() for text in white]
    black_c = [clean(text, punct).split() for text in black]

    white_z = [clean(text, punct) for text in white]
    black_z = [clean(text, punct) for text in black]


    # tokenize the lists for LDA TDM
    # white_t = [ldatoken(card, stop, punct, lemmatizer).split() for card in white]
    # black_t = [ldatoken(card, stop, punct, lemmatizer).split() for card in black]

    # Creating the term dictionary of our corpus, where every unique term is assigned an index.
    # white_index = corpora.Dictionary(white_c)
    # black_index = corpora.Dictionary(black_c)
    # total_b_words = len(black_index)

    # convert dictionaries to a Term Document Matrix
    # convert dictionaries to a Term Document Matrix
    # white_td_matrix = [white_index.doc2bow(card) for card in white_t]
    # black_td_term_matrix = [black_index.doc2bow(card) for card in black_t]

    # create the object for lDA model with gensim library
    # Lda = gensim.models.ldamodel.LdaModel

    # run training CAH_LDA model on document term matrices
    # white_ldamodel = Lda(white_td_matrix, num_topics=3, id2word=white_index, passes=10)
    # black_ldamodel = Lda(black_td_matrix, num_topics=3, id2word=black_index, passes=10)

    # count_black = len(black_index)
    # predictors, label, max_sequence_len = padded_sequences(black_td_matrix, count_black)

    #print(white)
    #print(white_c)
    #print(white_index)
    # print(white_doc_term_matrix)
    #print(white_ldamodel.print_topics(num_topics=3,num_words=4))

    #print(black_ldamodel.print_topics(num_topics=3, num_words=4))

    # print(black)
    # print(black_c)
    # print(black_z)
    # print(black_index)
    # print(len(black_index))
    # print(black_index.keys())
    # print(black_index[5])
    # black_ngram = token_sequence_list(black_index, black_c)
    # print(type(black_ngram))
    # print(token_sequence_list(black_index, black_c))

    # predictors, label, max_sequence_len = padded_sequences(black_ngram, len(black_index))

    # print(predictors)


    # test of og code
    black_sequences, total_black = sequence_of_tokens(black_c)
    predictors, label, max_len = padded_sequences(black_sequences, total_black)
    model1 = create_model(max_len, total_black)
    model1.fit(predictors, label, epochs=100, verbose=5)
    model1.summary()
    print(generate_text("happy", 5, model1, max_len))
    print(generate_text("black", 5, model1, max_len))
    print(generate_text("tall", 5, model1, max_len))
    print(generate_text("ugly", 5, model1, max_len))
    print(generate_text("scary", 5, model1, max_len))
    print(generate_text("mother", 5, model1, max_len))
    print(generate_text("father", 5, model1, max_len))

    # black_index_list = token_index(black_c) # create list that corresponds to tokens
    # total_words = len(black_index_list)
    # black_ngram = token_sequence_list(black_index_list, black_c) # use token list to tokenize words
    # max_sequence_len = max([len(x) for x in black_ngram])
    #print(black_index_list[:5])
    #print(black_ngram[:10])
    # p, l = padded_sequences(black_ngram, total_words, max_sequence_len)
    # print(p)
    # print(l)
    #model = create_model(max_sequence_len, total_words)
    #model.summary()
    #model.fit(p, l, epochs=50, verbose=5)
    #print(generate_text("mother", 5, model, max_sequence_len, total_words, black_index_list,t))


def ldatoken(card, stop, punct, lemma, z= False):
    """Clean card by getting rid of stop words and punctuation. Return normalized item for LDA"""

    if z == False:
        stop_free = " ".join(i for i in card.lower().split() if i not in stop)
        # print(type(stop_free))
        punc_free = ''.join(ch for ch in stop_free if ch not in punct)
        # print(punc_free)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    else:
        punc_free = ''.join(ch for ch in card.lower() if ch not in punct)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())

    return normalized


def clean(text, punct):
    text = "".join(v for v in text if v not in punct).lower()
    text = text.encode("utf8").decode("ascii", 'ignore')
    return text

def sequence_of_tokens(txt):
    """Keras LSTM blog"""

    t.fit_on_texts(txt)

    total_words = len(t.word_index) + 1
    # convert data to sequence of tokens

    input_sequences = []
    for line in txt:
        sequences = t.texts_to_sequences([line])[0]
        for i in range(1, len(sequences)):
            n_gram_sequence = sequences[:i + 1]
            input_sequences.append(n_gram_sequence)
            # print(n_gram_sequence)
    return input_sequences, total_words


# def padded_sequences(input_sequences, total_words, max_sequence_len):
def padded_sequences(input_sequences, total_words):
    """takes in a list of lists"""
    max_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_len, padding='pre'))
    print(input_sequences)

    predictors, label = input_sequences[:, :-1], input_sequences[:, -1] # creates two variables: sequence / next word of Ngram
    label = ku.to_categorical(label, num_classes=total_words)
    return predictors, label, max_len


def token_sequence_list(d, card_list):
    input_sequences = []
    for lst in card_list:   # create a sequence of indices increasing length
        for w in range(1, len(lst)):
            n_gram_index_sequence = lst[:w+1]
            for i, word in enumerate(n_gram_index_sequence): # change to index
                if word in d:
                    n_gram_index_sequence[i] = d.index(word) # return sequence of tokens

            input_sequences.append(n_gram_index_sequence)
    return input_sequences

def token_index(lst):
    count = []
    for item in lst:
        for j in item:
            count.append(j)
    return count


def create_model(max_sequence_len, total_words):
    input_len = max_sequence_len - 1
    model = Sequential()

    # Add Input Embedding Layer
    model.add(Embedding(total_words, 10, input_length=input_len))
    zero_mask = True

    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(100))
    model.add(Dropout(0.1))

    # Add Output Layer
    model.add(Dense(total_words, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


# def generate_text(seed_text, num_words, model, max_sequence_len, t_index, tokenizer):
def generate_text(seed_text, num_words, model, max_sequence_len):
    for i in range(num_words):
        token_list = t.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding= 'pre')
        predicted = model.predict_classes(token_list, verbose=0)

        output_word = ""
        # for index, word in enumerate(t_index):
        for word, index in t.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += ' '+output_word
    return seed_text.title()




if __name__ == '__main__':
    main()
