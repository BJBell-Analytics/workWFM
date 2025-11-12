"""workIDP - Routines to help track IDP data and aid data exploration

    Daily data captured from Alvaria "Aspect Workforce"
"""
import pandas as pd
from sqlalchemy import create_engine


def cleanday(inputfile, idp_date):
    """cleanday(inputfile, idp_date)
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

    clean_idp.insert(0, 'Date', pd.to_datetime(idp_date))
    clean_idp['Date'] = pd.to_datetime(clean_idp['Date'],
                                       format='%Y-%m-%d').dt.date
    clean_idp['Time Period'] = pd.to_datetime(clean_idp['Time Period'],
                                              format='%I:%M %p').dt.time

    return clean_idp


def update_idpdb(daily_idp, database_file, table_name):
    """update_idpdb(daily_idp, database_file, table_name)
        -insert daily_idp into the sql database database_file in table_name
        -db_file is str in 'sqlite:///name.db'
    """
    db_engine = create_engine(database_file)
    daily_idp.to_sql(
            table_name, con=db_engine, if_exists='replace', index=False)
