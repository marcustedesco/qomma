# qomma

## Description
SQL queries against CSV data using Python

Supports SELECT, FROM, WHERE, AND, OR with =, <, and >

## Assumptions
1. Importing os and sys is allowed
2. There are no empty values in the data rows
3. Queries follow the grammar:
    
    `SELECT columns FROM table WHERE column conditional value AND/OR column conditional value;`

    Errors resulting from queries not matching this pattern will not be handled.

## How to use
1. `pip install setuptools`
2. `python3 setup.py install`
3. Load a directory containing .csv files: 
    
    `qomma csv_samples`

    `qomma ./csv_samples/`

    `qomma /<path>/my_directory/`

2. Run your SQL query using pattern:

    `SELECT columns FROM table WHERE column conditional value AND/OR column conditional value;`

3. Quit the application:

    `\q`

## Local dev
1. `python3 -m qomma csv_samples`

## Issues

1. Does not support conditional values containing spaces. Example: 

    `AND company = 'id Software';`

2. Is not properly unit tested
3. Could use more parameter and return type documentation

## Refactor

1. Uses modules and classes to have proper seperation of concerns
2. Changed the tables dict to use Table as the value instead of an array of dicts. Made the column names and row values into tuples to ensure that the data is immutatable and to save space. Previously stored the column names with every row dict as key-value pairs which was inefficient at scale. 
3. Uses setup.py to make the package executable from the command line
4. Added type hints
5. Added some documentation of the functions