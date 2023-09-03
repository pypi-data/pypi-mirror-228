"""Useful functions to be used throughout the psusannx packages"""
import unidecode
import pandas as pd

def standardize_name(name):
    """
    Decode the special characters within a player's 
    name and make the name all lower case characters

    Parameters
    ----------
    name: str
        The raw sting containing the name of the player.

    Returns
    -------
    The clean & standardised player name.
    """
    
    return unidecode.unidecode(name).lower().replace("-"," ")


def number_position_suffix(number):
    """
    Suffix a number with either st, nd, rd or th.

    Parameters
    ----------
    number: The number (integer) that should be suffixed

    Returns
    -------
    if 1 is input, will return '1st'. If 2 is input will return '2nd' etc.
    """

    # Set up a liast for each possible suffix
    date_suffix = ["th", "st", "nd", "rd"]

    # Use modular arithmetic to figure out which suffix to use
    if number % 10 in [1, 2, 3] and number not in [11, 12, 13]:
        return str(number) + date_suffix[number % 10]
    else:
        return str(number) + date_suffix[0]
    

def sort_season_data(df):
    """
    Put the matches in chronological order (Must be a 'Date' field)
    & also in alphabetical order of the home team.
    Also delete duplicate rows of data to keep it clean.

    Parameters
    ----------
    df: The season data with the "Date" & "Home_team" columns to sort the data with.
    
    Returns
    -------
    The same dataframe that was entered, sorted by the ascending Date & Home_team columns.
    """

    # Make a copy of the input dataframe
    df_ = df.copy()

    # Make the date field a datetime
    df_["Date"] = pd.to_datetime(df.Date)

    # Sort the values
    df_sorted = df_.sort_values(by=["Date", "Home_team"]).reset_index(drop=True)

    # Make sure to just keep the date
    df_sorted["Date"] = pd.to_datetime(df_sorted["Date"]).dt.date

    # Make sure the 'Date' column is just a string
    df_sorted = df_sorted.astype({"Date": str})

    return df_sorted