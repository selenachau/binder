#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 10:31:52 2022

Place csv file in same directory as your python file

@author: selenachau-local
"""

import pandas as pd    
from isbnlib import canonical 

# read csv file
# isbns = pd.read_csv("isbns.csv")

# display DataFrame
# print(isbns)

def clean_isbn(row):
    return canonical(row[0])


# Open file as dataframe
#with open('isbns.csv') as file_obj:
df = pd.read_csv('isbns.csv', dtype="string", header=None)
first_row = df.iloc[0]
#print(canonical("978-90-04335-46-2"))
#print(get_canonical_isbn("978-90-04335-46-2"))

# applying function to each row in the dataframe
# and storing result in a new column
df2 = df.apply(clean_isbn, axis=1)
print(df2)

#print('\nAfter Applying Function: ')
#print(df)


"""
    # Create reader object by passing the file 
    # object to reader method
    reader_obj = csv.reader(file_obj)
    
    # Iterate over each row in the csv 
    # file using reader object
    for row in reader_obj:
        print(row)

type(row)
type(reader_obj)
   
# print(clean_isbn)
# clean = canonical("978-90-04335-46-2")
"""
