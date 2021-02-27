import csv
import random

"""Zoe Berling DU ID 872608482 card_classes.py"""

"""This code is an abridged solitaire version of Cards Against Humanity where a single user is presented a white card
and is prompted to select a black card/cards to fill in the blanks. As a solitary game, the player cannot technically
win. However, each white card and black card has *one* identifying tag that generally describes the card.
As the player chooses black cards, this program saves their choices to begin to learn a small slice of the player's
sense of humor."""

"""This version 1.0 of the game has:
1) Class Cards that stores card objects with the attributes: text, tag, # spaces, and color.
2) Class Deck: all piles of cards are treated as decks including player hands, cards in play, cards won,
and discard piles
3) Class Group: creates dictionaries of cards with white cards as the keys and black cards as the values to save player
preferences and eventually score them.
At some point it would be cool to add the NLTK library but at the moment and at this scale, cards just have one manually
added tag description. I also didn't end up having time before the due date to do anything with tags.."""


CARDS_IN_HAND = 5


class Card:
    """object for Card attributes"""
    def __init__(self, text, tag, color, space=None):
        self._text = text
        self._tag = tag
        self._space = space
        self._color = color

    def __repr__(self):
        """Override the system default representation of class method"""
        return self._text

    def show_card(self):
        """method to print card color and text values"""
        print(f'{self._color} card: {self._text}')

    def return_tag(self):
        """method to return the card tags"""
        return self._tag

    def return_space(self):
        """method to return the number of spaces"""
        return self._space


class Deck:
    """ Object for Deck attributes and functions"""
    def __init__(self, color=None, c=None, shuffle=False):
        self._deck = []
        if c is not None:
            self.create(color, c)
        if shuffle is True:
            random.shuffle(self._deck)

    def __len__(self):
        """return length of the list"""
        return len(self._deck)

    def create(self, color, c):
        """method to create the deck"""
        list_1 = []
        with open(c) as card_csv:
            csv_file = csv.reader(card_csv)
            for text, tag in csv_file:
                if color == 'white':
                    if text:
                        if '_____' in text:  # Add cards with spaces to white card deck
                            space = text.count('_____')
                            list_1.append(Card(text, tag, color, space))
                        else:
                            pass
                if color == 'black':
                    if text:
                        if '_____' not in text:
                            space = 1
                            list_1.append(Card(text, tag, color, space))
                        else:
                            pass
        self._deck = list_1  # Alias
        card_csv.close()

    def shuffle_deck(self):
        """method to shuffle the deck"""
        random.shuffle(self._deck)
        return self._deck

    def remove_card(self, index=0):  # deal
        """method that removes card from specified deck and returns it"""
        a = self._deck.pop(index)
        return a

    def return_card(self, index = 0):
        """method that returns value of card: does not manipulate it"""
        return self._deck[index]

    def show(self):
        """method that prints cards from deck"""
        for i, card in enumerate(self._deck):
            print(f"{i + 1}: ", end ='')
            card.show_card()

    def add(self, deck, index = 0):
        """method that takes in a deck argument, removes an element from that deck list and appends it to the called
        deck list (uses remove_card)"""
        add_card = deck.remove_card(index)  # shallow copy
        self._deck.append(add_card)

    def return_space(self):
        """method to card.return_space()"""
        for card in self._deck:
            return card.return_space()

    def return_list(self):
        """method to return the deck list"""
        # list1 = self._deck
        return self._deck

class Group:
    """classify selected cards"""
    def __init__(self):
        self._group = {}

    def __len__(self):
        return len(self._group)

    def group_cards(self, key_card, value_card=None):
        """ takes in two card elements from any decks- one for the key and one for the value and adds them to a dictionary
        then saves them to the called dictionary"""
        dictionary = self._group  # dictionary of cards # shallow copy
        # dictionary[key_card] = value_card
        if key_card not in dictionary:
            dictionary[key_card] = [value_card]
        else:
            dictionary[key_card].append(value_card)

        self._group = dictionary  # Alias

    def return_dict(self):
        """return the group dictionary"""
        return self._group

    def create_csv(self, name):
        pass

    def identify_tag(self, key_card, value_card=None):
        """takes in two card elements from any decks- one for the key and one for the value and extracts the tags."""
        dictionary = self._group
        if key_card not in dictionary:
            dictionary[key_card.return_tag()] = [value_card.return_tag()]
        else:
            dictionary[key_card.return_tag()].append(value_card.return_tag())
        self._group = dictionary

class Card_Text:
    def __init__(self):
        self._list_words = []

    def __len__(self):
        return len(self._list_words)

    def parse_text(self, card):
        """start transformations on the text in the cards"""
        this_text = card.text
        words = this_text.split()
        self._list_words = words





def main():
    black_deck = Deck('black', 'cards.csv', True)  # create and shuffle black deck
    white_deck = Deck('white', 'cards.csv', True)  # create and shuffle white deck
    dis_card = Deck()  # create pile for White Card in play
    options = Deck()  # create deck of black cards in play
    played_cards = Group()  # create a dictionary of cards that have been played: should be a shallow? copy of the cards
    card_tags = Group()
    dump = Deck()

    for i in range(CARDS_IN_HAND):  # add cards to option deck to start game
        options.add(black_deck)

    print(len(white_deck))

    a = ''
    while a != 0 and len(white_deck) != 0:

        if a == 0 or len(white_deck) == 0:
            print(f'played cards: {played_cards.return_dict()}')

        else:

            dis_card.add(white_deck)  # white card is chosen to play

            j = dis_card.return_space()  # count black spaces in white card

            for i in range(j):
                dis_card.show() # White card is shown to player
                print("\n")  # visual break
                options.show()
                print("\n")  # visual break
                a = (int(input(f'Please pick a card to play ({i+1} of {j}) \nOr type 0 to exit: ')))  # ask player what card they want to select
                if a == 0:
                    break
                else:
                    played_cards.group_cards(dis_card.return_card(), options.return_card(a-1))  # shallow copy add to dictionary
                    card_tags.identify_tag(dis_card.return_card(), options.return_card(a - 1))
                    dump.add(options, a-1) # move black card to dump deck
                    print("\n")  # visual break
                    # dump.show()

            print('Played:')
            dis_card.show()
            dump.show()
            print("\n")  # visual break

            if a == 0:
                break
            else:
                dis_card.remove_card()  # refresh white card

                for i in range(j):
                    dump.remove_card()
                    options.add(black_deck)  # replace options

    print(f'Played cards: {played_cards.return_dict()}')
    print(f"tags: {card_tags.return_dict()}")


if __name__ == '__main__':
    main()
