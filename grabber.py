import json
import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError, TftWatcher
from datetime import datetime, timedelta


APIKey = 'RGAPI-d75a075e-c977-4069-9f2f-cca213cef63e'

riot_watcher = RiotWatcher(APIKey)
tft_watcher = TftWatcher(APIKey)

def fetch_and_store_matches(username, region='na1', json_file_path='matches.json', superRegion='AMERICAS', name_to_puuid_file_path='name_to_ids.txt'):
    my_account = riot_watcher.account.by_riot_id(superRegion, username, region)
    me = tft_watcher.summoner.by_puuid(region, my_account['puuid'])
    player_puuid = me['puuid']

    # Load the existing name to puuid mapping if the file exists
    if os.path.exists(name_to_puuid_file_path):
        with open(name_to_puuid_file_path, 'r') as name_to_puuid_file:
            name_to_puuid = json.load(name_to_puuid_file)
    else:
        name_to_puuid = {}

    # Get the current datetime
    current_time = datetime.now()

    # Check if the username is already in the mapping
    if username in name_to_puuid:
        # Parse the stored datetime
        last_updated = datetime.fromisoformat(name_to_puuid[username]['last_updated'])
        
        # Check if the last update was within the last 3 days
        if current_time - last_updated < timedelta(days=3):
            print(f"{username} was updated within the last 3 days. Not bothering to update data on this user")
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
    with open(name_to_puuid_file_path, 'w') as name_to_puuid_file:
        json.dump(name_to_puuid, name_to_puuid_file, indent=4)

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