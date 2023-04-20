import csv
import json

# ### Census Data
# Import Census Data in CSV format and convert it to JSON format according to column names.

file1 = open('CensusData.csv')
census_csv = csv.reader(file1, delimiter=',')

# +
county_dic = []

for row in census_csv:
    if row[1] == 'ID': 
        continue
        
    county = {}
    if len(row[1]) == 4:  
        county['fips'] = '0' + row[1]
    else:
        county['fips'] = row[1]
    county['percent_white']   = float(row[12])
    county['percent_black']   = float(row[13])
    county['percent_native']  = float(row[14])
    county['percent_asian']   = float(row[15])
    county['percent_island']  = float(row[16])
    county['percent_other']   = float(row[17])
    county['percent_poverty'] = float(row[18])
    
    county_dic.append(county)
# -

county_dic

# ### Covid19 Data
# Import Covid19 Data in JSON format.

file2 = open('Covid19Data.json')
covid_json = json.load(file2)
# covid_json

for county in county_dic:
    for fip in covid_json:
        if fip['fips'] == county['fips']:
            county['state'] = fip['state']
            county['name'] = fip['county']
            county['population'] = fip['population']
            if fip['metrics']['vaccinationsCompletedRatio']:
                county['percent_vaccinated'] = round(fip['metrics']['vaccinationsCompletedRatio'] * 100, 2)
            else:
                county['percent_vaccinated'] = None
            
            if fip['actuals']['cases'] and fip['actuals']['deaths']:
                county['percent_case'] = round(float(fip['actuals']['cases']) / fip['population'] * 100, 2)
                county['percent_death'] = round(float(fip['actuals']['deaths']) / fip['population'] * 100, 2)
            else:
                county['percent_case'] = None
                county['percent_death'] = None
            break

with open('CombinedData.json', 'w') as file3:
    json.dump(county_dic, file3, indent = 3)

f = open('CombinedData.json')
json.load(f)
