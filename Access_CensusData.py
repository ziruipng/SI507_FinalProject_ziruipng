# ### Access Census Data 

import requests
import zipfile
import io
import geopandas as gpd

url = "https://www2.census.gov/geo/tiger/TIGER_DP/2020ACS/ACS_2020_5YR_COUNTY.gdb.zip"
response = requests.get(url)

# Download Census Data and Unzip it
if response.status_code == 200: # Check the response status code to make sure the request was successful
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall()
    print("Successfully downloaded and decompressed!")
else:
    print("Failed to save file!")

# Convert Layer Attribute in gdb to CSV file
gdb_layer = gpd.read_file('ACS_2020_5YR_COUNTY.gdb', driver = 'FileGDB', layer = 'ACS_2020_5YR_COUNTY')
csv_path = 'CensusData/county.csv'
gdb_layer.drop(columns = 'geometry').to_csv(csv_path, index = False)

gdb_layer = gpd.read_file('ACS_2020_5YR_COUNTY.gdb', driver = 'FileGDB', layer = 'X02_RACE')
csv_path = 'CensusData/race.csv'
gdb_layer.drop(columns = 'geometry').to_csv(csv_path, index = False)

gdb_layer = gpd.read_file('ACS_2020_5YR_COUNTY.gdb', driver = 'FileGDB', layer = 'X17_POVERTY')
csv_path = 'CensusData/poverty.csv'
gdb_layer.drop(columns = 'geometry').to_csv(csv_path, index = False)

gdb_layer = gpd.read_file('ACS_2020_5YR_COUNTY.gdb', driver = 'FileGDB', layer = 'X19_INCOME')
csv_path = 'CensusData/income.csv'
gdb_layer.drop(columns = 'geometry').to_csv(csv_path, index = False)

# ### Combine CSV files

import csv
import pandas as pd
import numpy as np

# +
'''
ID|Geographic Identifier
NAME|Short Name
GEOID|Unique Identifier of Summary Level, Characteristic Iteration, US, State, County, Tract, Block Group Code

B02001e1|RACE - Universe:  Total population - Total: -- (Estimate)
B02001e2|RACE - Universe:  Total population - Total:  White alone -- (Estimate)
B02001e3|RACE - Universe:  Total population - Total:  Black or African American alone -- (Estimate)
B02001e4|RACE - Universe:  Total population - Total:  American Indian and Alaska Native alone -- (Estimate)
B02001e5|RACE - Universe:  Total population - Total:  Asian alone -- (Estimate)
B02001e6|RACE - Universe:  Total population - Total:  Native Hawaiian and Other Pacific Islander alone -- (Estimate)

B17001e2|POVERTY STATUS IN THE PAST 12 MONTHS BY SEX BY AGE: Income in the past 12 months below poverty level: Population for whom poverty status is determined -- (Estimate)

B19113e1|MEDIAN FAMILY INCOME IN THE PAST 12 MONTHS (IN 2020 INFLATION-ADJUSTED DOLLARS): Median family income in the past 12 months (in 2020 inflation-adjusted dollars): Families -- (Estimate)
'''
county = pd.read_csv("CensusData/county.csv")
county = county.rename(columns={"GEOID": "ID", "GEOID_Data": "GEOID"})
county = county[['ID','NAME', 'GEOID']]

race = pd.read_csv("CensusData/race.csv")
race = race[['GEOID', 'B02001e1', 'B02001e2', 'B02001e3', 'B02001e4', 'B02001e5', 'B02001e6']]

poverty = pd.read_csv("CensusData/poverty.csv")
poverty = poverty[['GEOID', 'B17001e2']]

income = pd.read_csv("CensusData/income.csv")
income = income[['GEOID', 'B19113e1']]

census = county.merge(race,on="GEOID").merge(poverty,on="GEOID").merge(income,on="GEOID")
# -

pop_total   = census['B02001e1']
pop_white   = census['B02001e2']
pop_black   = census['B02001e3']
pop_native  = census['B02001e4']
pop_asian   = census['B02001e5']
pop_island  = census['B02001e6']
pop_poverty = census['B17001e2']

ratio_white   = np.array(pop_white) / np.array(pop_total)
ratio_black   = np.array(pop_black) / np.array(pop_total)
ratio_native  = np.array(pop_native) / np.array(pop_total)
ratio_asian   = np.array(pop_asian) / np.array(pop_total)
ratio_island  = np.array(pop_island) / np.array(pop_total)
ratio_poverty = np.array(pop_poverty) / np.array(pop_total)

percent_white   = np.round(ratio_white * 100, 2)
percent_black   = np.round(ratio_black * 100, 2)
percent_native  = np.round(ratio_native * 100, 2)
percent_asian   = np.round(ratio_asian * 100, 2)
percent_island  = np.round(ratio_island * 100, 2)
percent_poverty = np.round(ratio_poverty * 100, 2)

'''
census['ratio_white']   = ratio_white
census['ratio_black']   = ratio_black
census['ratio_native']  = ratio_native
census['ratio_asian']   = ratio_asian
census['ratio_island']  = ratio_island
census['ratio_other']   = 1 - ratio_white - ratio_black - ratio_native - ratio_asian - ratio_island
census['ratio_poverty'] = ratio_poverty
'''

census['percent_white']   = percent_white
census['percent_black']   = percent_black
census['percent_native']  = percent_native
census['percent_asian']   = percent_asian
census['percent_island']  = percent_island
census['percent_other']   = 100 - percent_white - percent_black - percent_native - percent_asian - percent_island
census['percent_poverty'] = percent_poverty


census.to_csv("CensusData.csv")
