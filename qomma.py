#!/usr/bin/python3
import os
import sys

path = sys.argv[1]
tables = {}

# TODO: add error handling for bad directory str input
# TODO: make this only work for subdirectories?
# TODO: toLower for all key names
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        # process the csv file rows
        rows = []
        column_names = []
        line_count = 0
        lines = open(path+filename, 'r')
        for line in lines:
            items = line.split(',')
            stripped_items = [item.strip(' \t\n\r') for item in items]
            if(line_count == 0):
                # print('column_names: '+line)
                column_names = stripped_items
            else:
                # print(line) 
                row = {}
                column_num = 0
                for item in stripped_items:
                    # assuming that there will not be any empty values in the rows
                    row[column_names[column_num]] = item
                    column_num += 1
                rows.append(row)
            line_count += 1
        tables[filename.replace('.csv','')] = rows
        # print('Processed ',line_count-1,'rows.')

# print 
print(len(tables.keys()), 'table(s) found:')
for table in tables:
    print(table)

while True:
    # output the directory name and wait for input
    s = input('\n'+os.path.basename(os.path.normpath(path))+'=# ')
    # TODO: all string toLower
    if(s.startswith('\q')):
        # what is the best practice here?
        quit()
    # TODO: turn this into a function
    elif(s.startswith('select *')):
        for table_name in tables:
            table = tables[table_name]
            for row in table:
                print(row)