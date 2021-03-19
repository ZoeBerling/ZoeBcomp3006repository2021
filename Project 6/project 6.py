import numpy as np
import random
import pandas as pd
""" Zoe Berling DU ID 872608482 Project 6
Part 1 File generation:
Using numpy, generate a 10 column by 1000 row matrix of values (this values may be whatever you want. Get Creative!)
Create a csv file using this data. Please choose 10 column names for the file.
Please attach your csv file along with your code

Part 2 Loading in the file via pandas:
Using pandas, load the file you created above into your project as a dataframe.

Part 3 Statistics:
Calculate the mean, standard deviation, mode, and median of the values in each column in your file.
Part 4 Generate Summary File:
Generate a text file that includes:
The above statistics
The column names used in the file (gotten from the dataframe not hard coded)
3 rows of your choosing from the dataframe as sample data"""

num_rows = 10000

a = [random.randint(2,2000) for day in range(num_rows)]
b = [random.random() for rand in range(num_rows)]
c = [random.randint(1,12) for lbs in range(num_rows)]
d = [random.randint(1,9999) for emails in range(num_rows)]
e = [random.randint(1,5) for num in range(num_rows)]
f = [random.randint(50,1000) for num2 in range(num_rows)]
g = [random.randint(1,104) for age in range(num_rows)]
h = [random.randint(2,186) for point in range(num_rows)]
i = [random.randint(1000,100000) for tear in range(num_rows)]
j = [random.random()+random.randint(1,80) for wood in range(num_rows)]

matrix_values = np.array([a, b, c, d, e, f, g, h, i, j])
matrix_col = matrix_values.T
this_one = "randomcount.csv"
create = 0

# Using numpy, generate a 10 column by 1000 row matrix of values (this values may be whatever you want.
headers = ["Days Wasted","Nitrogen Levels","Price per Pound","Unread Emails","Big Foot Sightings", "Ice Cream Related Deaths","Years Old", "Hours Wasted" ,"Bad Dates" ,"Beard Length in Meters"]
# print(len(headers))
# Create a csv file using this data. Please choose 10 column names for the file. (native python csv reader)
if create == 1:
    with open(this_one, "w") as csv_file:
        csv_file.write(",".join(headers) + '\n')
        np.savetxt(csv_file, matrix_col, '%s', ',')


# Using pandas, load the file you created above into your project as a dataframe.
data_frame = pd.read_csv(this_one, header=0)

# Calculate the mean, standard deviation, mode, and median of the values in each column in your file.
headers_df = data_frame.columns.values

mean = pd.DataFrame(data_frame.mean()) # mean
mean = mean.rename(columns = {0:'Mean'})

std = pd.DataFrame(data_frame.std()) # standard deviation
std = std.rename(columns = {0:'Standard Deviation'})

median = pd.DataFrame(data_frame.median()) # medean
median = median.rename(columns = {0: 'Median'})

mode = pd.DataFrame(data_frame.mode()) # mode

df_except_mode = pd.concat([mean, std, median], axis=1)

df_array = df_except_mode.to_numpy()

with open("test_file.txt", 'w') as txt:
    txt.write(f'Summary of Averages:\n\n')
    txt.write(df_except_mode.to_string(header= True, index= True)) # table of averages
    txt.write(f'\n\nMode/s (Only showing 10 rows bc a couple columns are all unique values:\n')
    txt.write(mode.to_string(header=True, max_rows= 10, na_rep='NaN')) # mode (in a separate table bc some columns have multiple modes
    txt.write(f'\n\nSample Data:\n')
    txt.write(data_frame.head(n=3).to_string(header=True, index= True)) # 3 rows of the sample data