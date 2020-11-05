# Plot COVID-19
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# python libs
import pandas as pd
from pathlib import Path

# local modules
from covid19_dashboard.data_parser.world_pop import get_world_pop

_debug_lib = True
_lib_path = str(Path(__file__).parent)

def parse_timeseries_csv(data_set, country_list=None):

    valid_names = {'confirmed', 'deaths', 'recovered'}
    if (data_set not in valid_names):
        print("error, data_set" + data_set + "does not exist")
        exit(5)

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
    df = df.rename_axis('', axis='columns') 

    df['Date'] =  pd.to_datetime(df['Date'])

    # 3. Melt
    var_name = data_set.capitalize()
    df = df.melt(id_vars=['Date'],
            var_name='Country',
            value_name=var_name)

    # df is now in LONG format, with numerical index
    # HEADER
    # idx, date, country, $var_name: [Confirmed | Deaths | Recovered]

    ##### Debug
    # if (_debug_lib):
    #     debugcsv = _lib_path+'/debug/clean_covid_'+ data_set +'.csv'
    #     # printing country names only.
    #     df.sort_index().to_csv(debugcsv, columns=[], header=False)

    return df

def get_covid_data_primary():

    # Long Format
    # orig_var_list = ['confirmed', 'deaths', 'recovered']
    # df_list = []

    # for var in orig_var_list:
    #     dfx = parse_timeseries_csv(var)
    #     # dfx['Var'] = var.capitalize()
    #     df_list.append(dfx)
    # return pd.concat(df_list, axis=0, ignore_index=True)

    # Wide Format

    df_conf = parse_timeseries_csv('confirmed')
    df_deat = parse_timeseries_csv('deaths')
    df_rec = parse_timeseries_csv('recovered')

    df_merged = pd.merge(df_conf, df_deat, on=['Country', 'Date'], copy=False)
    df_merged = pd.merge(df_merged, df_rec, on=['Country', 'Date'], copy=False)

    return df_merged


# def create_flat_df(country_df, world_pop_df):
#     reg_df = pd.merge(world_pop_df.loc[: , ["UN_Region"]], country_df, left_index=True, right_index=True, how='inner').groupby("UN_Region").sum()
#     con_df = pd.merge(world_pop_df.loc[: , ["Continent"]], country_df, left_index=True, right_index=True, how='inner').groupby("Continent").sum()
#     df_merged = pd.concat([country_df, reg_df, con_df], axis=0)
#     return df_merged


def get_covid_data_all():
    df_covid_pri = get_covid_data_primary() # Mixed/Wide Format: (Country + Date) -> conf, deaths, rec
    df_world_pop = get_world_pop()          # Long Format:       (Country) -> un_region, continent 

    # 1. Merge with population df

    # reg_df = pd.merge(world_population_df.loc[: , ["UN_Region"]], country_df, left_index=True, right_index=True, how='inner').groupby("UN_Region").sum()
    # con_df = pd.merge(world_population_df.loc[: , ["Continent"]], country_df, left_index=True, right_index=True, how='inner').groupby("Continent").sum()
    # df_merged = pd.concat([country_df, reg_df, con_df], axis=0)

    # df_merged = pd.merge(df_world_pop.loc[: , ["UN_Region"]], country_df, left_index=True, right_index=True, how='inner')


    print(df_covid_pri)
    print(df_world_pop)
    df_countries = pd.merge(df_covid_pri, df_world_pop,  on='Country', how='inner')

    # 2. Generate Sum Rows for Continent & Region, 

    # df_regions    = df_merged.groupby(['UN_Region', 'Date'], as_index=False).sum()

    # debugcsv = _lib_path+'/debug/OOPS.csv'
    # df_merged.to_csv(debugcsv)
    # print(df_merged)

    # TODO: Research on possible bug/issue with categorical
    df_regions = df_countries.groupby(['UN_Region', 'Date'], as_index=False).agg(
                        {
                        'Population_2019': 'sum',
                        'Confirmed': 'sum',
                        'Deaths': 'sum',
                        'Recovered': 'sum',
                        'Continent' : 'first'
                        })
    
    df_continents = df_countries.groupby(['Continent', 'Date'], as_index=False).agg(
                        {'Population_2019': 'sum',
                        'Confirmed': 'sum',
                        'Deaths': 'sum',
                        'Recovered': 'sum'
                        })

    # 3. Add new column entry type

    df_countries['Entry_Type'] = "country"
    df_countries.rename(columns={'Country': 'Location'}, inplace=True)

    df_regions['Entry_Type'] = "un_region"
    df_regions.rename(columns={'UN_Region': 'Location'}, inplace=True)

    df_continents['Entry_Type'] = "continent"
    df_continents.rename(columns={'Continent': 'Location'}, inplace=True)

    # 4. Concat 
    df = pd.concat([df_countries, df_regions, df_continents], ignore_index=True, copy=False)

    debugcsv = _lib_path+'/debug/ALL.csv'
    df.to_csv(debugcsv)

    print(df)
    return df


if __name__ == '__main__':

    get_covid_data_all()
    
    # regions1 = df_full.groupby(["UN_Region", 'Date', 'Var'], as_index=False, dropna=False).sum()
    # print(regions1)

    # regions2 = df_full.groupby(["UN_Region", 'Date', 'Var'], as_index=True).sum()
    # print(regions2)

    exit()
