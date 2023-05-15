import numpy as np
from numpy import random as rd


def generate_number() -> np.ndarray:
    """Generates a array with 5 random numbers from 0 to 9
    
    Returns:
    random_number(np.ndarray): An array with 5 digits, each ranging from 0 to 9
    """
    random_number = np.array(rd.randint(1, 10, 1))
    random_number = np.append(random_number, rd.randint(0, 10, 4))
    # print(random_number)  # Used for testing ONLY
    return random_number
