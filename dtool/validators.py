"""
Utility functions for validating and checking various data formats and conditions.

Functions:
- `check_shamsi`: Check if a date string is in the Shamsi (Jalali) format ('YYYY/MM/DD').
- `check_farsi_name`: Check if a string consists only of Persian characters and spaces.
- `is_center`: Check if a string matches any province name in Iran.
- `is_cities`: Check if a string matches any city name in Iran.
- `college_trust`: Check if a string represents a trusted college name.
- `trust`: Check if a string matches any engineering field in Iran.
- `validate_national_id`: Validate the format and checksum of an Iranian national ID number.

Note:
- Data sources are loaded from JSON files ('iran_provinces.json', 'province.json', 'engineering_fields.json').
"""
import json
import re
import jdatetime



def check_shamsi(d_str: str) -> bool:
    """
    Check if a date string is in the Shamsi (Jalali) format ('YYYY/MM/DD').
    Returns:
    - bool: True if the date string is in the correct format, False otherwise.
    """
    obj_date = jdatetime.datetime
    try:
        obj_date.strptime(d_str, '%Y/%m/%d')
        return True
    except ValueError:
        return False

def check_farsi_name(n: str) -> bool:
    """
    Check if a string consists only of Persian characters and spaces.
    Returns:
    - bool: True if the string consists only of Persian characters and spaces, False otherwise.
    """
    pattern = r"^[\u0600-\u06FF\s1-9]+$"
    if re.match(pattern, n):
        return True
    else:
        return False


def is_center(n: str) -> bool:
    """
    Check if a string matches any province name in Iran.
    Returns:
    - bool: True if the string matches any province name, False otherwise.
    """
    with open("iran_provinces.json", "r", encoding= "utf-8") as f:
        ob = json.load(f)
    for char in ob:
        if char in n:
            return True

def is_cities(n: str) -> bool:
    """
    Check if a string matches any city name in Iran.
    Returns:
    - bool: True if the string matches any city name, False otherwise.
    """
    with open("province.json", "r", encoding="utf-8") as f:
        ob = json.load(f)

    for char in ob:
        if char in n:
            return True

def college_trust(n: str) -> bool:
    """
    Check if a string represents a trusted college name.
    Returns:
    - bool: True if the string represents a trusted college name, False otherwise.
    """
    lst_college = ["فنی و مهندسی", "علوم پایه", "علوم انسانی", "دامپزشکی", "اقتصاد", "کشاورزی", "منابع طبیعی"]
    for lst in lst_college:
        if n in lst:
            return True

def trust(n: str) -> bool:
    """
    Check if a string matches any engineering field in Iran.
    Returns:
    - bool: True if the string matches any engineering field, False otherwise.
    """
    with open("engineering_fields.json", "r", encoding= "utf-8") as f:
        ob = json.load(f)
    for char in ob :
        if n in char:
            return True

def validate_national_id(n: int) -> bool:
    """
    Validate the format and checksum of an Iranian national ID number.

    Returns:
    - bool: True if the national ID number is valid, False otherwise.
    """
    if len(str(n)) < 8 or len(str(n)) > 10:
        return False
    if len(str(n)) < 10:
        n_id = "0" * (10 - len(str(n)) + n)
    if len(str(n)) == 10:
        n_id = str(n)
    coefficients = [10 , 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(n_id[i]) * coefficients[i] for i in range(9))
    reminder = total % 11
    if reminder < 2:
        return int(n_id[9]) == reminder
    else:
        return int(n_id[9]) == 11 - reminder
