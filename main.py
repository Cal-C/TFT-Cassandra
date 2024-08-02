import csv


from grabber import fetch_and_store_matches
from thinker import analyze_matches
from cleaner import remove_old_tft_matches
from DragonTamer import update_all_dragon_data , download_all_images
from grapher import make_graphs


update_all_dragon_data()

usernames_file_path = 'usernames.csv'  


usernames = []

# Read usernames from the CSV file
with open(usernames_file_path, 'r', newline='') as usernames_file:
    reader = csv.reader(usernames_file)
    next(reader)  # Skip the header row
    for row in reader:
        usernames.append(row[0])

print(f'Working on fetching users: {", ".join(usernames)}')

for username in usernames:
    fetch_and_store_matches(username)

remove_old_tft_matches()

download_all_images()


unit_placements, main_trait_placements, side_trait_placements, total_trait_placements, augment_placements, item_placements = analyze_matches('matches.json')

make_graphs()

