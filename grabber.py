import json
import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError, TftWatcher

APIKey = 'RGAPI-d75a075e-c977-4069-9f2f-cca213cef63e'

riot_watcher = RiotWatcher(APIKey)
tft_watcher = TftWatcher(APIKey)

def fetch_and_store_matches(username, region='na1', json_file_path='matches.json', superRegion='AMERICAS'):
    my_account = riot_watcher.account.by_riot_id(superRegion, username, region)
    me = tft_watcher.summoner.by_puuid(region, my_account['puuid'])
    player_puuid = me['puuid']

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

# Example usage:
fetch_and_store_matches('MDE')