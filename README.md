# qomma

## Description
SQL queries against CSV data using Python

Supports SELECT, FROM, WHERE, AND, OR

## Assumptions
1. Importing os and sys is allowed
2. There are no empty values in the data rows
3. Queries follow the grammar:
    
    `SELECT columns FROM table WHERE column conditional value AND/OR column conditional value;`

    Errors resulting from queries not matching this pattern will not be handled.

## How to use
Load a directory containing .csv files: 

`./qomma.py csv-samples`

`./qomma.py ./csv-samples/`

`./qomma.py /<path>/my-directory/`

## Data structures

### Tables dictionary
```
{
    "table_name_1": [
        {
            "column_name_1": value1
            "column_name_2": value2
        },
        {
            "column_name_1": value3
            "column_name_2": value4
        }
    ],
    "table_name_2": [
        {
            "column_name_A": valueA
            "column_name_B": valueB
        },
        {
            "column_name_A": valueC
            "column_name_B": valueD
        }
    ]
}
```

### Parsed SQL query dictionary
```
{
    "FROM": table_value,
    "SELECT": [
        column_name_1,
        column_name_2
    ],
    "WHERE": [
        {
            "conjunction": "AND" | "OR" | None,
            "column": column_name_2,
            "operator": "=" | ">" | "<",
            "value": val
        }
    ]
}
```