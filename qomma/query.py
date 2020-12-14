import sys
from qomma.table import Table
from qomma.expression import Expression

class Query:
    """
    A class used to represent a Query 

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    def __init__(self, sql_query: str):
        self.FROM = ''
        self.SELECT = []
        self.WHERE = []
        self.parse_query(sql_query)

    def parse_query(self, sql_query: str):
        # Find the end of the query
        semi_index = sql_query.find(';')
        if(semi_index == -1):
            # TODO: make this Raise an exception instead of using sys.exit
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
                self.SELECT = select_attr
            elif(terms[i] == 'from'):
                self.FROM = terms[i+1]
                i+=1
            elif(terms[i] == 'where'):
                self.WHERE = []
                while i+1 < len(terms): 
                    conjunction: str = None
                    if terms[i+1] == 'and':
                        conjunction = 'AND'
                        i+=1
                    elif terms[i+1] == 'or':
                        conjunction = 'OR'
                        i+=1
                    # Assumes SQL query follows fixed pattern 
                    # Currently does not support quoted values with spaces or commas
                    self.WHERE.append(Expression(conjunction, terms[i+1], terms[i+2], terms[i+3]))
                    # self.WHERE.append({
                    #     'conjunction': conjunction,
                    #     'column': terms[i+1],
                    #     'operator': terms[i+2],
                    #     'value': terms[i+3]
                    # })
                    i+=3
            i+=1