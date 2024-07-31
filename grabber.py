import json
import os
import csv
from datetime import datetime, timedelta

from riotwatcher import RiotWatcher, ApiError, TftWatcher

APIKey = ''
if os.path.exists('APIKey.txt'):
    modification_time = os.path.getmtime('APIKey.txt')

    # Convert the modification time to a datetime object
    modification_datetime = datetime.fromtimestamp(modification_time)

    # Calculate the age of the file
    current_datetime = datetime.now()
    age = current_datetime - modification_datetime

    # Check if the file is less than a day old
    if age > timedelta(days=1):
        print("Update your APIkey! The APIKey.txt is more than a day old, and Riot requires you to regenerate your API key daily. You will likely get a 403 error if you try to use this key. Would you like to proceed anyway? (Y/N)")
        response = input()
        if response.lower() != 'y':
            exit()
    #else:
        #print(f"APIKey.txt is less than a day old. With an age of {age} Proceeding with API key retrieval.")
    with open('APIKey.txt', 'r') as key_file:
        APIKey = key_file.read().strip()
else:
    print("APIKey.txt not found. Please create a file named APIKey.txt with your Riot API key in it.")
    exit()

riot_watcher = RiotWatcher(APIKey)
tft_watcher = TftWatcher(APIKey)

def fetch_and_store_matches(username, region='na1', json_file_path='matches.json', superRegion='AMERICAS', name_to_puuid_file_path='player_data.csv'):
    my_account = riot_watcher.account.by_riot_id(superRegion, username, region)
    me = tft_watcher.summoner.by_puuid(region, my_account['puuid'])
    player_puuid = me['puuid']

    # Load the existing name to puuid mapping if the file exists
    name_to_puuid = {}
    if os.path.exists(name_to_puuid_file_path):
        with open(name_to_puuid_file_path, 'r', newline='') as name_to_puuid_file:
            reader = csv.DictReader(name_to_puuid_file)
            for row in reader:
                name_to_puuid[row['username']] = {
                    'puuid': row['puuid'],
                    'last_updated': row['last_updated']
                }

    # Get the current datetime
    current_time = datetime.now()

    # Check if the username is already in the mapping
    if username in name_to_puuid:
        # Parse the stored datetime
        last_updated = datetime.fromisoformat(name_to_puuid[username]['last_updated'])
        
        # Check if the last update was within the last 3 days
        if current_time - last_updated < timedelta(days=2):
            print(f"{username} was updated within the last 2 days. Not bothering to update data on this user")
            return True
        else:
            # Update the datetime if the last update was more than 3 days ago
            name_to_puuid[username]['last_updated'] = current_time.isoformat()
    else:
        # Add the username, puuid, and current datetime to the mapping
        name_to_puuid[username] = {
            'puuid': player_puuid,
            'last_updated': current_time.isoformat()
        }

    # Write the updated mapping back to the file
    with open(name_to_puuid_file_path, 'w', newline='') as name_to_puuid_file:
        fieldnames = ['username', 'puuid', 'last_updated']
        writer = csv.DictWriter(name_to_puuid_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for name, data in name_to_puuid.items():
            writer.writerow({
                'username': name,
                'puuid': data['puuid'],
                'last_updated': data['last_updated']
            })

    print(f"{username} has been added/updated.")


    # Check if the JSON file already exists
    if os.path.exists(json_file_path):
        # Load existing data
        with open(json_file_path, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, dict):
                    existing_data = {}
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    if player_puuid in existing_data:
        print(f"Data for PUUID {player_puuid} already exists. Skipping update.")
    else:
        matches_ids = tft_watcher.match.by_puuid(region, me['puuid'], count=20)
        matches = [tft_watcher.match.by_id(region, item) for item in matches_ids]

        # Structure the data to include the player's PUUID
        player_data = {player_puuid: matches}

        # Update the existing data with the new player data
        existing_data.update(player_data)

        # Write the updated data to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        print(f"Matches data for {player_puuid} has been written to {json_file_path}")