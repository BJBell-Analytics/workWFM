"""workWFM
    - Routines to help clean, analyze, and track data for my workforce duties.

    Daily data captured from Alvaria "Aspect Workforce"
"""
import pandas as pd
from sqlalchemy import create_engine

# functions to convert data formats


def update_idpdb(daily_idp, database_file, table_name):
    """update_idpdb(daily_idp, database_file, table_name)
        -insert daily_idp into the sql database database_file in table_name
        -db_file is str in 'sqlite:///name.db'
    """
    db_engine = create_engine(database_file)
    daily_idp.to_sql(
            table_name, con=db_engine, if_exists='append', index=False)


def xlwb_csvs(infile, create_files=False):
    """xlwb_csvs(infile)
        -extract data from excel workbook tabs (tab label YYY-MM-DD)
        -returns the dictionary of pandas objects
        -set create_files=True to create individual csv files
    """
    dict_pdobj = pd.read_excel(infile, sheet_name=None)
    if create_files:  # currently False by default
        for tabdate in dict_pdobj.keys():
            dict_pdobj[tabdate].to_csv(f'IDP_{tabdate}.csv', index=False)

    return dict_pdobj

# Cleaning functions


def cleanIDP(inputfile, idp_date):
    """cleanIDP(inputfile, idp_date)
        - clean-up raw csv data for a single day from inputfile
        - add idp_date (type str formatted 'YYYY-MM-DD')
        - convert 'Time Period' to datetime values
        - returns the cleaned data as a pandas object
    """
    daily_idp = pd.read_csv(inputfile)

    # Filter out unused columns (Open, Past, OSL, ADH, A-Sch Staff) and Summary
    clean_idp = daily_idp.loc[:47, ['Time Period', 'F-Calls Off',
                                    'A-Calls Off', 'Calls Ans',
                                    'HC Required for SL', 'NET Butts in Seats',
                                    'SL-ACD', 'OAHT', 'A-AHT', 'A-ASA']]

    clean_idp.insert(0, 'Date', pd.to_datetime(idp_date, format='%Y-%m-%d'))
    clean_idp['Time Period'] = pd.to_datetime(clean_idp['Time Period'],
                                              format='%H:%M:%S').dt.time

    return clean_idp


def cleanSEG(infile):
    """cleanSEG
        -cleans segment data for off phone activity reporting
        -returns clean pandas object with necessary data
    """
    pass
