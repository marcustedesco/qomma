class Expression:
    def __init__(self, conjunction: str, column: str, operator: str, value: str):
        self.conjunction: str = conjunction
        self.column: str = column
        self.operator: str = operator
        self.value: str = value