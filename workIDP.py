"""workIDP - Routines to help track IDP data and aid data exploration

    Daily data captured from Alvaria "Aspect Workforce"
"""
import pandas as pd


def cleanday(inputfile, idp_date):
    """cleanday(inputfile, idp_date)
        - clean-up raw csv data for a single day from inputfile
        - add idp_date (TODO: enforce datetime data type?)
        - returns the cleaned data as a pandas object
    """
    daily_idp = pd.read_csv(inputfile)

    # Filter out unused columns (Open, Past, OSL, ADH, A-Sch Staff) and Summary
    clean_idp = daily_idp.loc[:47, ['Time Period', 'F-Calls Off',
                                    'A-Calls Off', 'Calls Ans',
                                    'HC Required for SL', 'NET Butts in Seats',
                                    'SL-ACD', 'OAHT', 'A-AHT', 'A-ASA']]

    clean_idp.insert(0, 'Date', idp_date)  # Add the date as first column

    return clean_idp
