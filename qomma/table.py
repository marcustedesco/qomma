class Table:
    """
    A class used to represent a Table

    ...

    Attributes
    ----------
    column_names : tuple
        a tuple representing the names of the table columns
    rows : list of tuples
        the list of rows each represented by a tuple of values 

    Methods
    -------
    load_from_csv(filepath: str)
        Loads the CSV data into memory as Table attributes
    parse_line(row: str) -> list
        Parses a string representing a comma-delimited line in the CSV file
    """
    def __init__(self):
        self.column_names: tuple = ()
        self.rows: list = []

    def load_from_csv(self, filepath: str) -> None:
        # Process the CSV file rows
        self.column_names: tuple = ()
        self.rows: list = []
        line_count: int = 0
        lines: str = open(filepath, 'r')
        for line in lines:
            parsed_line = self.parse_line(line)
            if(line_count == 0):
                self.column_names = tuple([item.lower() for item in parsed_line])
            else:
                self.rows.append(tuple(parsed_line))
                # row = {}
                # j = 0
                # while j < len(parsed_line):
                #     # Assuming that there will not be any empty values in the rows
                #     row[column_names[j]] = parsed_line[j]
                #     j += 1
                # rows.append(row)
            line_count += 1
        # tables[filename.replace('.csv','')] = rows

    def parse_line(self, row: str) -> list:
        """Parses a string representing a comma-delimited line in the CSV file

        Parameters
        ----------
        row : str
            The str representing the row in the CSV file

        Returns
        ------
        list
            A sanitized list of strings representing the values from the CSV row
        """
        items: list = row.split(',')
        # Remove extra spaces, tabs, new lines and returns
        items = [item.strip(' \t\n\r') for item in items]
        return items
    
    def print_table_rows(self):
        for row in self.rows:
            print(*row, sep=', ')
    
    def set_columns(self, column_names: tuple) -> None:
        self.column_names = column_names

    def append_row(self, row: tuple) -> None:
        self.rows.append(row) 