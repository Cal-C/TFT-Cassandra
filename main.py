import csv


from grabber import fetch_and_store_matches
from thinker import analyze_matches


usernames_file_path = 'usernames.csv'  


usernames = []

# Read usernames from the CSV file
with open(usernames_file_path, 'r', newline='') as usernames_file:
    reader = csv.reader(usernames_file)
    next(reader)  # Skip the header row
    for row in reader:
        usernames.append(row[0])

print(usernames)


# Loop through each username and call the function
for username in usernames:
    fetch_and_store_matches(username)


unit_placements, trait_placements, augment_placements = analyze_matches('matches.json', 'analyzed_data.json')
