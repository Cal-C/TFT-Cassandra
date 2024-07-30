import json
from collections import defaultdict

def analyze_matches(json_file_path='matches.json', output_file_path='analyzed_data.json'):
    # Load the matches data
    with open(json_file_path, 'r') as json_file:
        players = json.load(json_file)

    # Debugging: Print the keys of the matches dictionary
    print("Keys in matches dictionary:", players.keys())

    # Initialize dictionaries to store total placements and counts for units, traits, and augments
    unit_placements = defaultdict(lambda: {'total_placement': 0, 'count': 0})
    trait_placements = defaultdict(lambda: {'total_placement': 0, 'count': 0})
    augment_placements = defaultdict(lambda: {'total_placement': 0, 'count': 0})

    for player_puuid, matches in players.items():
        # Iterate through each match
        for match in matches:
            # Ensure match['info']['participants'] is a list
            if 'info' not in match or 'participants' not in match['info'] or not isinstance(match['info']['participants'], list):
                print(f"Unexpected data structure in match: {match}")
                continue

            # Iterate through each participant in the match
            for participant_data in match['info']['participants']:
                placement = participant_data['placement']

                # Iterate through each unit in the participant's data
                for unit in participant_data['units']:
                    unit_name = unit['character_id']
                    # Update the total placements and counts in the dictionary
                    unit_placements[unit_name]['total_placement'] += placement
                    unit_placements[unit_name]['count'] += 1

                # Iterate through each trait in the participant's data
                for trait in participant_data['traits']:
                    trait_name = trait['name']
                    # Update the total placements and counts in the dictionary
                    trait_placements[trait_name]['total_placement'] += placement
                    trait_placements[trait_name]['count'] += 1

                # Iterate through each augment in the participant's data
                for augment in participant_data['augments']:
                    augment_name = augment
                    # Update the total placements and counts in the dictionary
                    augment_placements[augment_name]['total_placement'] += placement
                    augment_placements[augment_name]['count'] += 1

    # Prepare the data to be written to the output JSON file
    analyzed_data = {
        'unit_placements': dict(unit_placements),
        'trait_placements': dict(trait_placements),
        'augment_placements': dict(augment_placements)
    }

    # Write the analyzed data to the output JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(analyzed_data, output_file, indent=4)

    print(f"Analyzed data has been written to {output_file_path}")

    return unit_placements, trait_placements, augment_placements

# Example usage:
# unit_placements, trait_placements, augment_placements = analyze_matches('matches.json', 'analyzed_data.json')