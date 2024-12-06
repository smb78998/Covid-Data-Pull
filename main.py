import csv
import requests
import pandas as pd
from datetime import datetime, timedelta

# dates
start_date = datetime(2023, 3, 1)
end_date = datetime(2023, 12, 31)

cities_data = []

# loop and collect data
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    print(f"Fetching data for date: {date_str}")

    url = f'https://covid-api.com/api/reports?date={date_str}&q=US%20Florida'
    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()  #

        if data['data']:
            for record in data['data']:
                region = record.get('region', {})
                cities = region.get('cities', [])

                # Extract city-related data
                for city in cities:
                    city_info = {
                        'city_name': city['name'],
                        'date': city['date'],
                        'fips': city['fips'],
                        'lat': city['lat'],
                        'long': city['long'],
                        'confirmed': city['confirmed'],
                        'deaths': city['deaths'],
                        'confirmed_diff': city['confirmed_diff'],
                        'deaths_diff': city['deaths_diff'],
                        'last_update': city['last_update']
                    }
                    cities_data.append(city_info)
        else:
            print(f"No data available for {date_str}")
    else:
        print(f"Error fetching data: {response.status_code}")

    # next date
    current_date += timedelta(days=1)

# to excel
if cities_data:
    df = pd.DataFrame(cities_data)
    df.to_excel('Florida2023V2.xlsx', index=False)
    print("Excel file has been created.")
else:
    print("No data was collected.")
