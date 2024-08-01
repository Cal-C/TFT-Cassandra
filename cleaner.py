import json
import re
import os

from collections import defaultdict



def extract_version(version_string):
    match = re.search(r'\d+\.\d+', version_string)
    return match.group(0) if match else None

def version_numbers(version_string):
    major, minor = map(int, version_string.split('.'))
    return (major, minor)

def get_latest_tft_version():
    with open('matches.json') as file:
        matches = json.load(file)
    
    versions = set()
    for player_puuid, player_matches in matches.items():
        for match in player_matches:
            if 'info' not in match or 'participants' not in match['info'] or not isinstance(match['info']['participants'], list):
                print(f"Unexpected data structure in match: {match}")
                continue
            
            for participant_data in match['info']['participants']:
                version = extract_version(match['info']['game_version'])
                if version:
                    versions.add(version)
    
    latest_version = max(versions, key=version_numbers)
    print(f'Latest version: {latest_version}')
    
    return latest_version

def remove_old_tft_matches():
    latest_version = get_latest_tft_version()
    
    with open('matches.json') as file:
        matches = json.load(file)
    
    updated_matches = {}
    matches_from_old_version = {}
    for player_puuid, player_matches in matches.items():
        updated_player_matches = []
        for match in player_matches:
            if 'info' not in match or 'participants' not in match['info'] or not isinstance(match['info']['participants'], list):
                print(f"Unexpected data structure in match: {match}")
                continue
            
            version = extract_version(match['info']['game_version'])
            if version == latest_version:
                updated_player_matches.append(match)
            else:
                if player_puuid not in matches_from_old_version:
                    matches_from_old_version[player_puuid] = []
                matches_from_old_version[player_puuid].append(match)
        
        updated_matches[player_puuid] = updated_player_matches
    
    #remove users with no matches
    updated_matches = {player_puuid: player_matches for player_puuid, player_matches in updated_matches.items() if player_matches}

    
    with open('matches.json', 'w') as file:
        json.dump(updated_matches, file, indent=4)

    matches_by_version_and_player = defaultdict(lambda: defaultdict(list))

    for player_puuid, old_version_matches in matches_from_old_version.items():
        for match in old_version_matches:
            version = extract_version(match['info']['game_version'])
            if version:
                matches_by_version_and_player[version][player_puuid].append(match)

    if not os.path.exists('OldMatches'):
        os.makedirs('OldMatches')
        
    # Write the grouped matches to files
    for version, players_matches in matches_by_version_and_player.items():
        filename = f"OldMatches/matches_{version}.json"
        with open(filename, 'w') as file:
            json.dump(players_matches, file, indent=4)