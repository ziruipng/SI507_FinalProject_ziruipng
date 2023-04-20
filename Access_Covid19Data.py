import json
import requests

api_key = "f3cec0686fdf444ca63c363cf92b265a"
url = "https://api.covidactnow.org/v2/counties.json?apiKey=" + api_key


def AccessData(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data


covid_json = AccessData(url)

with open('Covid19Data.json', 'w') as f:
    json.dump(covid_json, f, indent = 4)
