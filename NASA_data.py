"""
This programme tells you about asteroid near misses with Earth.
To use it, you  will need your own api key from NASA.
Go to  https://api.nasa.gov/ and fill in the form ro generate your API key.
Once this is done, it will be emailed to you.
Create a config.py file and write 'api_key = ' then paste your api key inside  ' ' .
You are now ready to run this programme.

"""

import requests  # Fetches the data from the API
import csv  # Needed to create a csv file with the data
from datetime import datetime  # Work with dates
from config import api_key  # Import API key securely


print("Today we're going to look at some asteroid near misses with Earth.")


API_URL = f'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={api_key}'  # API URL

def get_year_input():
    """Ask the user for a valid 4-digit year and return it."""
    while True:
        year = input("What year would you like to check? (YYYY): ")

        if year.isdigit() and len(year) == 4:  # Ensures input is exactly 4 digits
            return int(year)  # Convert to string to integer and return

        else:
            print("Invalid input! Please enter a valid 4-digit year (e.g., 2025).")


def fetch_asteroid_data():
    """Fetch asteroid data from NASA API."""
    print("Fetching asteroid data from NASA...")
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json().get('near_earth_objects', [])  # Returns asteroid data


def filter_asteroids_by_year(asteroids, year):
    """Filter asteroids based on the given year and orbiting Earth."""
    filtered_asteroids = []

    for asteroid in asteroids:
        for approach in asteroid.get('close_approach_data', []):
            date_str = approach['close_approach_date']
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            if date_obj.year == year and approach.get('orbiting_body', '').lower() == "earth":
                asteroid_info = {
                    "Name": asteroid.get('name', 'Unknown'),
                    "Date": date_obj.strftime("%d-%m-%Y"),
                    "Speed (mph)": approach.get('relative_velocity', {}).get('miles_per_hour', 'N/A'),
                    "Miss Distance (miles)": approach.get('miss_distance', {}).get('miles', 'N/A')
                }
                filtered_asteroids.append(asteroid_info)

    return filtered_asteroids  # Returns filtered list

year = get_year_input()  # Get user input for year
asteroids = fetch_asteroid_data()  # Fetch asteroid data from API


filtered_asteroids = filter_asteroids_by_year(asteroids, year)  # Filter data

if filtered_asteroids:
    print(f"\nAsteroid near-misses with Earth in {year}:", "\n")
    for asteroid in filtered_asteroids:
        print(f"{asteroid['Name']} - {asteroid['Date']} - Speed: {asteroid['Speed (mph)']} mph - Miss Distance: {asteroid['Miss Distance (miles)']} miles")


def save_to_csv(filtered_asteroids, year):
    """Save the asteroid data to a CSV file."""
    if not filtered_asteroids:
        print(f"No near misses in {year}. No CSV file will be created.")
        return

    filename = f'asteroids_{year}.csv'
    with open(filename, 'w', newline='') as csv_file:
        fieldnames = ["Name", "Date", "Speed (mph)", "Miss Distance (miles)"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_asteroids)

    print('\n'f"Data saved to {filename}.")


save_to_csv(filtered_asteroids, year)



""" 

This extra, below, is commented out, as the above script works perfectly without this add-on.
However, I had this idea I thought would be a nice addition, so I looked up how to do it and created a seperate script.
It will give you a list of podcasts about asteroids. Feel free to give it a try, 

To run this section, you will need a Spotify Client Id & Client Secret.
Log in to Spoitfy at https://developer.spotify.com/dashboard/create and click "create app" on the dashboard.
Add the keys to your config file, as you did before, this time using client_id and client_secret.

It also uses spotipy, which you may need to install. 
Install it by typing ' pip install spotipy ' into your terminal.

Make sure you have Asteriod_podcasts_list.py from the GitHub Repository.

"""
# Uncomment to try

more_info = input('\n'"Would you like to know more about asteroids? y/n ")

if more_info.lower() == 'y':
    from Asteroid_podcast_list import search_podcasts

else:
    print('\n''Have a nice day! Watch out for Asteroids!!!')