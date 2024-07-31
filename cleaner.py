import json
import re

def extract_version(version_string):
    match = re.search(r'\d+\.\d+', version_string)
    return match.group(0) if match else None

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
    
    latest_version = max(versions)
    print(f'Latest version: {latest_version}')
    
    return latest_version

def remove_old_tft_matches():
    latest_version = get_latest_tft_version()
    
    with open('matches.json') as file:
        matches = json.load(file)
    
    updated_matches = {}
    for player_puuid, player_matches in matches.items():
        updated_player_matches = []
        for match in player_matches:
            if 'info' not in match or 'participants' not in match['info'] or not isinstance(match['info']['participants'], list):
                print(f"Unexpected data structure in match: {match}")
                continue
            
            version = extract_version(match['info']['game_version'])
            if version == latest_version:
                updated_player_matches.append(match)
        
        updated_matches[player_puuid] = updated_player_matches
    
    with open('matches.json', 'w') as file:
        json.dump(updated_matches, file, indent=4)