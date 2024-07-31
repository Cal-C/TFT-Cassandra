import json
import csv
from collections import defaultdict

def analyze_matches(json_file_path='matches.json', unit_output_file='unit_placements.csv', trait_output_file='trait_placements.csv', augment_output_file='augment_placements.csv'):
    # Load the matches data
    with open(json_file_path, 'r') as json_file:
        players = json.load(json_file)

    # Debugging: Print the keys of the matches dictionary
    print("Number of keys in matches dictionary after reading", json_file_path, ":", len(players.keys()))

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

    # Function to sort and write data to CSV
    def write_sorted_csv(output_file, header, data_dict):
        sorted_data = sorted(data_dict.items(), key=lambda item: round(item[1]['total_placement'] / item[1]['count'], 2))
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for name, data in sorted_data:
                average_placement = round(data['total_placement'] / data['count'], 2)
                writer.writerow([name, average_placement, data['total_placement'], data['count']])

    # Write unit placements to CSV
    write_sorted_csv(unit_output_file, ['Unit Name', 'Average Placement', 'Total Placement', 'Count'], unit_placements)

    # Write trait placements to CSV
    write_sorted_csv(trait_output_file, ['Trait Name', 'Average Placement', 'Total Placement', 'Count'], trait_placements)

    # Write augment placements to CSV
    write_sorted_csv(augment_output_file, ['Augment Name', 'Average Placement', 'Total Placement', 'Count'], augment_placements)

    print(f"Unit placements have been written to {unit_output_file}")
    print(f"Trait placements have been written to {trait_output_file}")
    print(f"Augment placements have been written to {augment_output_file}")

    return unit_placements, trait_placements, augment_placements