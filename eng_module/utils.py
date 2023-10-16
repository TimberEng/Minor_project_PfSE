import csv

def str_to_float (s):
    """
    Returns a float or string from a numeric string
    """
    try:
        value = float (s)
        return value
    except ValueError:
        return s
    
def str_to_int (s):
    """
    The function should convert a numeric string to an integer.
    """
    try:
        value = int (s)
        return value
    except ValueError:
        return s

def read_csv_file (file_name: str) -> list[list[str]]:
    """
    Returns a long string of text representing the text data in the file
    """
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        file_data = list(csv_reader)
    return file_data