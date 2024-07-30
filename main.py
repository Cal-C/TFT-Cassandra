from grabber import fetch_and_store_matches
from thinker import analyze_matches


# List of usernames to fetch matches for
usernames = ['MDE', 'BetterThanMDE']

# Loop through each username and call the function
for username in usernames:
    fetch_and_store_matches(username)


unit_placements, trait_placements, augment_placements = analyze_matches('matches.json', 'analyzed_data.json')

print(unit_placements)
print(trait_placements)
print(augment_placements)