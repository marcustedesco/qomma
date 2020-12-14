import os
from qomma.query import Query
from qomma.table import Table
from qomma.expression import Expression

def load_tables(path: str) -> dict:
    tables = {}
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            # Load the CSV file
            table = Table()
            if not path[-1] == '/':
                path = path + '/'
            table.load_from_csv(path+filename)
            tables[filename.replace('.csv','')] = table

    return tables

def print_tables_found(tables: dict) -> None:
    # Print tables found
    print(len(tables.keys()), 'table(s) found:')
    for table in tables:
        print(table)


def handle_input_queries(directory: str, tables: dict) -> None:
    while True:
        # Output the directory name and wait for input
        query_input: str = input('\n'+directory+'=# ').lower()

        if(query_input.startswith('\q')):
            quit()
        else: 
            query: Query = Query(query_input)
            output_table: Table = run_query(query, tables)
            output_table.print_table_rows()

def run_query(query: Query, tables: dict) -> Table:
    table: Table = tables[query.FROM]

    # Create an empty output Table
    output_table: Table = Table()

    for row in table.rows:
        match = True

        # Filter by WHERE expressions
        if query.WHERE:
            expression: Expression
            for expression in query.WHERE:
                row_value: str = get_row_value(expression.column, row, table.column_names)
                # If this is the first expression
                if expression.conjunction == None:
                    match = eval_expression(row_value, expression)
                else:
                    if expression.conjunction == 'AND':
                        match = match and eval_expression(row_value, expression)
                    elif expression.conjunction == 'OR':
                        match = match or eval_expression(row_value, expression)

        # Get SELECT columns
        if match:
            selected_values: tuple = ()
            if '*' in query.SELECT:
                selected_values = row
            else:
                temp_row_values: list = []
                column: str
                for column in query.SELECT:
                    temp_row_values.append(get_row_value(column, row, table.column_names))
                selected_values = tuple(temp_row_values)
            # Add to output Table
            output_table.append_row(selected_values)     

    # Add the columns names to the table
    if '*' in query.SELECT:
        # Output table should have all the column names
        output_table.set_columns(table.column_names)
    else:
        selected_columns: list = []
        column: str
        for column in query.SELECT:
            selected_columns.append(column)
        # Output table should only have selected columns
        output_table.set_columns(tuple(selected_columns))

    return output_table

def get_row_value(select_column: str, row: tuple, column_names: tuple) -> str:
    # TODO: Add error handling here in case column does not exist
    i: int = column_names.index(select_column)
    return row[i]

def eval_expression(row_value: str, expression: Expression) -> bool:
    row_value = row_value.lower()
    if(expression.operator == '='):
        if(row_value == expression.value):
            return True
    elif(expression.operator == '>'):
        if(row_value > expression.value):
            return True
    elif(expression.operator == '<'):
        if(row_value < expression.value):
            return True
    else:
        return False