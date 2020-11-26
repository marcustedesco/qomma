#!/usr/bin/python3
import os
import sys

def main():
    path = sys.argv[1]
    tables = load_csv_files(path)
    directory = os.path.basename(os.path.normpath(path))
    handle_input_queries(directory, tables)

# Loads CSV files
# Returns a tables object
# {
#     "table_name_1": [
#         {
#             "column_name_1": value1
#             "column_name_2": value2
#         },
#         {
#             "column_name_1": value3
#             "column_name_2": value4
#         }
#     ],
#     etc...
# }
def load_csv_files(path):
    tables = {}
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            # Process the CSV file rows
            rows = []
            column_names = []
            line_count = 0
            lines = open(path+filename, 'r')
            for line in lines:
                parsed_line = parse_line(line)
                if(line_count == 0):
                    column_names = [item.lower() for item in parsed_line]
                else:
                    row = {}
                    j = 0
                    while j < len(parsed_line):
                        # Assuming that there will not be any empty values in the rows
                        row[column_names[j]] = parsed_line[j]
                        j += 1
                    rows.append(row)
                line_count += 1
            tables[filename.replace('.csv','')] = rows

    # Print CSV load summary
    print(len(tables.keys()), 'table(s) found:')
    for table in tables:
        print(table)

    return tables

# Runtime loop after load
# Returns None
def handle_input_queries(directory, tables):
    while True:
        # Output the directory name and wait for input
        sql_query = input('\n'+directory+'=# ').lower()

        if(sql_query.startswith('\q')):
            quit()
        else: 
            parsed_query = parse_query(sql_query)
            output_table = run_query(parsed_query, tables)
            print_table(output_table)

# Parses a query str to an object that can be used to run the query on the data
# Returns a query object 
# {
#     "FROM": table_value,
#     "SELECT": [
#         column_name_1,
#         column_name_2
#     ],
#     "WHERE": [
#         {
#             "conjunction": "AND" | "OR" | None,
#             "column": column_name_2,
#             "operator": "=" | ">" | "<",
#             "value": val
#         }
#     ]
# }
def parse_query(sql_query):
    parsed_query = {}

    # Find the end of the query
    semi_index = sql_query.find(';')
    if(semi_index == -1):
        sys.exit('Error: missing closing semicolon')

    # Split the query into parts using comma and spaces as delimiters
    terms = sql_query[:semi_index]
    # Replace commas and quotes with spaces
    # TODO: Refactor parse logic to keep quoted strings together
    terms = terms.replace(',',' ').replace('\'',' ').replace('‘',' ').replace('\"',' ')
    # Pad operators with space
    terms = terms.replace('=',' = ').replace('>',' > ').replace('<',' < ')
    terms = " ".join(terms.split()).split(' ')
    terms = [term.strip(' \t\n\r') for term in terms]

    i = 0
    while i < len(terms):
        if(terms[i] == 'select'):
            select_attr = []
            while terms[i+1] != 'from':
                select_attr.append(terms[i+1])
                i+=1
            parsed_query['SELECT'] = select_attr
        elif(terms[i] == 'from'):
            parsed_query['FROM'] = terms[i+1]
            i+=1
        elif(terms[i] == 'where'):
            parsed_query['WHERE'] = []
            while i+1 < len(terms): 
                conjunction = None
                if terms[i+1] == 'and':
                    conjunction = 'AND'
                    i+=1
                elif terms[i+1] == 'or':
                    conjunction = 'OR'
                    i+=1
                # Assumes SQL query follows fixed pattern 
                # Currently does not support quoted values with spaces or commas
                parsed_query['WHERE'].append({
                    'conjunction': conjunction,
                    'column': terms[i+1],
                    'operator': terms[i+2],
                    'value': terms[i+3]
                })
                i+=3
        i+=1

    return parsed_query

# Determines the output of the SQL query against the db
# Supports SELECT, FROM, WHERE, AND, OR
# Returns list of row objects
def run_query(parsed_query, tables):
    output_table = []
    table = tables[parsed_query['FROM']]

    for row in table:
        match = True

        # Filter by WHERE expressions
        if 'WHERE' in parsed_query:
            for expression in parsed_query['WHERE']:
                # If this is the first expression
                if expression['conjunction'] == None:
                    match = eval_expression(row, expression)
                else:
                    if expression['conjunction'] == 'AND':
                        match = match and eval_expression(row, expression)
                    elif expression['conjunction'] == 'OR':
                        match = match or eval_expression(row, expression)

        # Get SELECT columns
        if match:
            selected_values = {}
            if '*' in parsed_query['SELECT']:
                selected_values = row
            else:
                for attr in parsed_query['SELECT']:
                    selected_values[attr] = row[attr]
            output_table.append(selected_values)     
    
    return output_table

# Evaluates the result of the WHERE conditional statement on a row
# Returns True or False
def eval_expression(row, expression):
    row_value = row[expression['column']].lower()
    if(expression['operator'] == '='):
        if(row_value == expression['value']):
            return True
    elif(expression['operator'] == '>'):
        if(row_value > expression['value']):
            return True
    elif(expression['operator'] == '<'):
        if(row_value < expression['value']):
            return True
    else:
        return False

# Prints the query result table without columns
# Returns None
def print_table(table):
    for row in table:
        values = []
        for key in row.keys():
            values.append(row[key])
        print(', '.join(values))

# Parse line of the CSV from a space and comma delimited string to a list
# Returns list of str
def parse_line(row):
    items = row.split(',')
    items = [item.strip(' \t\n\r') for item in items]
    return items

if __name__ == '__main__':
    main()