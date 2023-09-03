import pandas as pd
import json
from typing import Union

# Function to load data from a file
def load_data(file_path: str, format: str = 'csv') -> Union[pd.DataFrame, list, dict]:
    """
    Load data from a file.
    
    Parameters:
    - file_path: str: Path to the data file
    - format: str: File format ('csv', 'json')
    
    Returns:
    Loaded data
    """
    if format == 'csv':
        return pd.read_csv(file_path)
    elif format == 'json':
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format")

# Load JSON Array
def load_json_array(file_path: str) -> list:
    """
    Load a JSON array from a file.
    
    Parameters:
    - file_path: str: Path to the JSON file
    
    Returns:
    Loaded JSON array
    """
    with open(file_path, 'r') as f:
        return json.load(f)

# Load JSON Dictionary
def load_json_dict(file_path: str) -> dict:
    """
    Load a JSON dictionary from a file.
    
    Parameters:
    - file_path: str: Path to the JSON file
    
    Returns:
    Loaded JSON dictionary
    """
    with open(file_path, 'r') as f:
        return json.load(f)

# Normalize an array
def normalize_array(arr: list) -> list:
    """
    Normalize an array to the range [0, 1].
    
    Parameters:
    - arr: list: Array to be normalized
    
    Returns:
    Normalized array
    """
    minimum = min(arr)
    maximum = max(arr)
    return [(x - minimum) / (maximum - minimum) for x in arr]

# Normalize the data
def normalize(data):
    return (data - data.min()) / (data.max() - data.min())

# pivot the data
def pivot(data, columns, values):
    return pd.pivot_table(data, values=values, columns=columns)
