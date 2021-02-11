"""Zoe Berling DU ID 872608482 count_to_csv.py 'In a separate file called count_to_csv.py, import your count.py. This
script will take an additional argument over count.py: the final argument should be the name of a csv file to which
you will write the data printed. This file does not need to already exist. import count.py dictionary and creates a CSV

Note: Do not use .txt or .csv in names of files.
"""

import unittest
import sys
import count


def main():
    print("count")
    dict = count.og_function()
    print(dict)
    print(sys.argv)

    csv_name = sys.argv[-1]  # assume last value in sys.argv is the name of the csv
    create_csv(dict, csv_name)


def create_csv(dict, name):

    c = open(f'{name}.csv', 'w') # writes to csv count_csv: creates a new one if it does not exist
    for key in dict:
        if dict[key] == -1:  # skip letters that are not in -l
            continue
        else:
            # print(key, ',', dict[key])
            c.writelines(f'{key},')
            c.writelines(f'{dict[key]}\n')
    c.close()

if __name__ == '__main__':
    main()




