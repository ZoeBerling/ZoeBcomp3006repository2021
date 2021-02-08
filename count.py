"""Zoe Berling DU ID 872608482 count.py
This short program opens a txt file and counts the instances of letters based on command line arguments -c -z and -l
Change the file by updating the file variable.
 Attributes of each argument:
 -c : Converts all capital letters into lower case before counting instances
 -z prints a row for each lower case characer even when it occurs 0 times in the txt
 -l only prints the frequencies of the characters in the argument assigned after -l is called. This is case-sensitive.
 The arguments are additive."""

import string
import sys
# sys.path.insert(0, "/home/zoebe/PycharmProjects/DU Assignments")


def main():
    og_function() # used to be main, returns dictionary

def og_function():
    """handles parsing the arguments -c, -c, -z
        creates empty dictionary
        calls add_frequencies
        prints elements of dictionary in CSV format"""
    d = {}  # a dictionary for characters : frequency
    remove_case = False  # if True will convert capital letters to lowercase before counting frequency

    ## get "real arguments".  that is, ignore the script name ## from count_sample_solution
    args = sys.argv[1:]

    ## process the leading flags  ## from count_sample_solution
    while args and args[0].startswith('-'):
        ## remove the next flag from the list  ## from count_sample_solution
        arg = args.pop(0)

        ## handle that flag  ## from count_sample_solution
        if arg == '-c':
            remove_case = False

        elif arg == '-l':
            specify_letters = args.pop(0)

        elif arg == '-z':
            alphabet = string.ascii_letters
            for character in alphabet:
                d[character] = 0

        elif arg == '--':
            break

    # The rest should be files
    for filename in args:
        file = filename
        try:
            add_frequencies(d, file, remove_case)
        except IOError:
            pass


    # print(f'this is the entire list: {sys.argv}')

    if '-l' in sys.argv:  # deals with -l argument : characters are case sensitive and must immediately follow -l
        for key in d:
            try:  # catch index error
                index = sys.argv.index('-l')
                # letters = sys.argv[index + 1]
                letters = specify_letters
                if '-' in letters:  # checks if the next item in the index is a new flag
                    d = []  # returns empty dictionary since there are no letters to count
                else:
                    if key not in letters: # set count to -1 for letters not in argument
                        d[key] = -1
                        # del d[key]
            except IndexError:
                d = [] # returns empty dictionary since there are no letters to count
                break
    else:
        print(d)
        return d
    print(d)
    return d



def add_frequencies(d, f, remove_case):
    """Takes in three parameters: a dictionary, a file object, and a bool.
    1) checks if the characters in the file are lower case or capital
        If capital: bool is False: switch for lower case
        If lowercase: bool is True: use as key in dictionary
    2) Counts the frequency of characters in the file
    3) Maps the characters : frequency to the dictionary and returns dictionary"""

    file = open(f, 'r') # for some reason this only opens if txt is not included in the name.
    text = file.read()
    file.close()
    if remove_case is True:  # convert to lowercase
        text = text.lower()
    else: # count each character
        pass

    for letter in text:
        if letter.isalpha() is True:  # only count letters
            if letter in d:  # add to letters in dictionary OR create instance in dictionary
                d[letter] += 1
            else:
                d[letter] = 1
    print(d)
    return(d)


if __name__ == '__main__':
    main()

