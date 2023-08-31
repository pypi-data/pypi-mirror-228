.. _Data Preprocessing Library:

Data Preprocessing Library
==========================

This Python library provides a function to preprocess data by splitting a specified column values and filling down other columns values. This is particularly useful for handling multi-valued cells in a DataFrame.

Functionality
-------------

The main function in this library is column_splitter_filler(file_name, column_to_split,separator). 

- column_to_split: The name of the column whose values need to be split.
- separator: The character or string used as the separator for splitting the values in the column_to_split.

The function splits the values in the column_to_split based on the provided separator, and then fills down the other column values. The processed DataFrame is returned by the function.

Usage
-----

Here is a sample usage of the process_data function:

    from MultiValueSplitter import column_splitter_filler

    df = pd.read_csv('data.csv')
    df = column_splitter_filler(df,'Coloumn_Name',',')
    
    print(df)

In this example, data.csv is the CSV file to be processed, Column_Name is the column to be split and Comma is the separator for splitting.