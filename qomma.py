#!/usr/bin/python3
import os
import sys

def main():
    path = sys.argv[1]
    tables = load_csv_files(path)
    directory = os.path.basename(os.path.normpath(path))
    input_queries(directory, tables)

def load_csv_files(path):
    tables = {}
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            # process the csv file rows
            rows = []
            column_names = []
            line_count = 0
            lines = open(path+filename, 'r')
            for line in lines:
                stripped_items = str_to_array(line)
                if(line_count == 0):
                    column_names = [item.lower() for item in stripped_items]
                else:
                    row = {}
                    column_num = 0
                    for item in stripped_items:
                        # assuming that there will not be any empty values in the rows
                        row[column_names[column_num]] = item
                        column_num += 1
                    rows.append(row)
                line_count += 1
            tables[filename.replace('.csv','')] = rows

    # print csv load summary
    print(len(tables.keys()), 'table(s) found:')
    for table in tables:
        print(table)

    return tables

def input_queries(directory, tables):
    while True:
        # output the directory name and wait for input
        sql_query = input('\n'+directory+'=# ').lower()
        
        if(sql_query.startswith('\q')):
            quit()
        else: 
            parsed_query = parse_query(sql_query)
            output_table = process_query(parsed_query, tables)
            print_table(output_table)

# TODO: refactor to use a tree structure
def parse_query(sql_query):
    parsed_query = {}

    # SEMICOLON 
    semi_index = sql_query.find(';')
    if(semi_index == -1):
        sys.exit('Error: missing closing semicolon')

    # SELECT
    select_index = sql_query.find('select')
    if(select_index == -1):
        sys.exit('Error: missing SELECT statement')
    from_index = sql_query.find('from')
    if(from_index == -1):
        sys.exit('Error: missing FROM statement')
    select_attr_str = sql_query[select_index+6:from_index]
    select_attr = str_to_array(select_attr_str)
    if('*' in select_attr):
        parsed_query['SELECT'] = ['*']
    else:
        parsed_query['SELECT'] = select_attr

    # FROM
    from_attr_str = sql_query[from_index+4:semi_index]
    parsed_query['FROM'] = from_attr_str.strip(' \t\n\r')

    return parsed_query

    # WHERE support
    # where_index = sql_query.find('where')
    # if(where_index != -1)

# Supports SELECT, FROM
def process_query(parsed_query, tables):
    output_table = []
    table = tables[parsed_query['FROM']]
    for row in table:
        selected_values = {}
        if('*' in parsed_query['SELECT']):
            selected_values = row
        else:
            for attr in parsed_query['SELECT']:
                selected_values[attr] = row[attr]
        # filter WHERE conditionals
        output_table.append(selected_values)
    
    return output_table

def print_table(table):
    for row in table:
        values = []
        for key in row.keys():
            values.append(row[key])
        print(', '.join(values))

def str_to_array(string):
    items = string.split(',')
    stripped_items = [item.strip(' \t\n\r') for item in items]
    return stripped_items

if __name__ == '__main__':
    main()