# qomma

## Description
SQL queries against CSV data using Python

## Assumptions
1. Importing os and sys is allowed
2. There are no empty values in the data rows

## How to use
Run `./qomma.py <directory>`

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
    ]
}
```