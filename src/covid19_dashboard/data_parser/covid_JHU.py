# Plot COVID-19
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# python libs
import pandas as pd
from pathlib import Path

# _debug_lib = True
# _lib_path = str(Path(__file__).parent)

def parse_timeseries_csv(data_set, country_list=None):

    valid_names = {'confirmed', 'deaths', 'recovered'}
    if (data_set not in valid_names):
        print("error, data_set" + data_set + "does not exist")
        exit(5)

    # file_name = _lib_path+'/data/time_series_covid19_' + data_set + '_global.csv'
    JHU_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
    JHU_url += 'time_series_covid19_' + data_set + '_global.csv'
    df = pd.read_csv(JHU_url, parse_dates=True)
    df = df.drop(columns= ['Lat','Long'])

    # Clean data s1: For simplicity, data from "overseas territories" will not be used. 
    # Applies for= 'Denmark', 'France', 'Netherlands', 'United Kingdom'
    # examples: Province/State,Country/Region,
    #   keep: ',Denmark,'
    #   drop: 'Greenland,Denmark,'
    #   keep: 'Beijing,China', Chongqing,China, ...
    df = df[ ~(df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) |
              (df['Province/State'].isna()) ]
    ## Less efficient, drop..
    # df.drop(df[ (df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) &
    #             (df['Province/State'].notna()) ].index, axis=0, inplace=True)

    # Clean data s2: Drop following entries:
    # * Diamond Princess
    # * MS Zaandam
    df = df[ ~(df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) )]
    # using drop
    # df.drop( df[ df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) ].index, axis=0, inplace=True)

    # Clean data s3: merge multi-region countries
    df = df.drop(columns= ['Province/State'])
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.groupby('Country').sum() # IMPLICIT INDEX CHANGE TO Country

    # Clean data s4: Modify some particular names...
    # to be fixed:    
    fix_these = {
        'US' : 'USA',
        'Korea, South' : 'South Korea',
        'Taiwan*' : 'Taiwan',
        'West Bank and Gaza' : 'Palestine'
    }
    df = df.rename(index=fix_these)

    ##### Data is now clean
    # df is now in WIDE format, with Country as index
    # HEADER
    # country, date-0, date-1, ..... date-N

    ##### Convert to long/tidy format, numerical index
    # 1. Transpose
    df = df.T
    # Now the index are the dates

    # 2. Reset index to default (numerical) and fix axis' names
    df = df.rename_axis('Date', axis='index')
    df.reset_index(inplace=True)
    # df = df.rename_axis('idx', axis='index')  # unnecessary, due to following melt

    df['Date'] =  pd.to_datetime(df['Date'])

    # 3. Melt
    df = df.melt(id_vars=['Date'],
            var_name='Country',
            value_name='Value')

    # df is now in LONG format, with numerical index
    # HEADER
    # idx, date, country, value

    ##### Debug
    # if (_debug_lib):
    #     debugcsv = _lib_path+'/debug/clean_covid_'+ data_set +'.csv'
    #     # printing country names only.
    #     df.sort_index().to_csv(debugcsv, columns=[], header=False)

    return df

def get_clean_covid_data():
    orig_var_list = ['confirmed', 'deaths', 'recovered']
    df_list = []

    for var in orig_var_list:
        dfx = parse_timeseries_csv(var)
        dfx['Var'] = var.capitalize()
        df_list.append(dfx)

    return pd.concat(df_list, axis=0, ignore_index=True)

if __name__ == '__main__':

    df_full = get_clean_covid_data()
    print(df_full)

    exit()
