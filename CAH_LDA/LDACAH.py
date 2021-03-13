import csv
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import re

"""Zoe Berling
Some code I might want for later:
# add_space = ['$', '£', '¥', '¢', '¤', '®', '©', 'ª', 'º', '°', '-']
# print(re.findall(r"(?=("+'|'.join(add_space)+r"))", card))"""

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
    exclude = set(string.punctuation)  # create a set of punctuation
    lemmatizer = WordNetLemmatizer()  #  link words with similar meaning to one key word

    # clean the lists
    white_c = [clean(card, stop, exclude, lemmatizer).split() for card in white]
    black_c = [clean(card, stop, exclude, lemmatizer).split() for card in black]

    # Creating the term dictionary of our corpus, where every unique term is assigned an index.
    white_index = corpora.Dictionary(white_c)
    black_index = corpora.Dictionary(black_c)

    # convert dictionaries to a Document Term Matrix
    white_doc_term_matrix = [white_index.doc2bow(card) for card in white_c]
    black_doc_term_matrix = [black_index.doc2bow(card) for card in black_c]

    # create the object for lDA model with gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # run training CAH_LDA model on document term matrices
    white_ldamodel = Lda(white_doc_term_matrix, num_topics=3, id2word=white_index, passes=10)
    black_ldamodel = Lda(black_doc_term_matrix, num_topics=3, id2word=black_index, passes=10)


    print(white)
    print(white_c)
    #print(white_index)
    # print(white_doc_term_matrix)
    print(white_ldamodel.print_topics(num_topics=3,num_words=3))


    print(black)
    print(black_c)
    # print(black_index)
    # print(black_doc_term_matrix)
    print(black_ldamodel.print_topics(num_topics=3, num_words=3))


def clean(card, stop, exclude, lemma, z= False):
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


if __name__ == '__main__':
    main()
