"""Zoe Berling DU ID 872608482 count.py
This short program opens a txt file and counts the instances of letters based on command line arguments -c -z and -l
Change the file by updating the file variable.
 Attributes of each argument:
 -c : Converts all capital letters into lower case before counting instances
 -z prints a row for each lower case characer even when it occurs 0 times in the txt
 -l only prints the frequencies of the characters in the argument assigned after -l is called. This is case-sensitive.
 The arguments are additive."""

# Count frequencies of characters in a text file
# create txt file with "Abracadabra!"
# read in txt file
# split text file by letter
# Count instances of each letter
# Save to a dictionary: letter: count
# save dictionary to csv

# -c upper case and lower case
# -l only prints frequencies of the characters in the argument letters for example l aeiou only counts vowels
# -z prints a row for each character even when it occurs 0 times

import sys


def main():
    """handles parsing the arguments -c, -c, -z
    creates empty dictionary
    calls add_frequencies
    prints elements of dictionary in CSV format"""
    d = {}  # a dictionary for characters : frequency
    file = input('Type the name of the file: for example: count_txt or test_text: ')  # name of the file
    remove_case = False  # if True will convert capital letters to lowercase before counting frequency

    for i in range(1, len(sys.argv)):

        if '-c' in sys.argv:  # - c (distinguish between upper and lowercase
            remove_case = True

        if '-z' in sys.argv:  # -z print a row for each character: even if it never occurs (will include capital letters if -c isn't an argument)
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            for character in alphabet:
                d[character] = 0

    # print(f'this is the entire list: {sys.argv}')

    add_frequencies(d, file, remove_case)

    for key in d:
        if '-l' in sys.argv:  # deals with -l argument : characters are case sensitive and must immediately follow -l
            try:  # catch index error
                index = sys.argv.index('-l')
                letters = sys.argv[index + 1 ]
                if '-' in letters:  # checks if the next item in the index is a new flag
                    print("Characters for the argument -l not found. Letters to count must follow the argument -l.")
                else:
                    if key in letters:
                        print(key, ',', d[key])
            except IndexError:
                print("Characters for the argument -l not found. Letters to count must follow the argument -l.")
                break
        else:
            print(key, ',', d[key])



def add_frequencies(d, file, remove_case):
    """Takes in three parameters: a dictionary, a file object, and a bool.
    1st checks if the characters in the file are lower case or capital
        If capital: bool is False: switch for lower case
        If lowercase: bool is True: use as key in dictionary
    2st Counts the frequency of characters in the file
    3nd Maps the characters : frequency to the dictionary
    returns dictionary"""
    file = open(file, mode='r')
    text = file.read()
    file.close()
    if remove_case is True:  # convert to lowercase
        text = text.lower()
    else: # count each character
        pass

    for letter in text:
        if letter.isalpha() is True:  # only count letters
            count = text.count(letter)
            d[letter] = count
    # print(d)



if __name__ == '__main__':
    main()



