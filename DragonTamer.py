import json
import csv
import os
import requests

#📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷
def get_image_urls(json_file_path, csv_file_path, json_key, url_template):
    image_urls = []
    item_names = []
    with open(f'Data/DragonData/{json_file_path}') as f:
        data = json.load(f)
        
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                item_name = row['Name']
                if item_name not in ['TFT12_Yuumi', 'TFT_ElderDragon']:
                    # Yuumi is always paired with Nora, so no reason to collect data on her placements since she breaks graphs.
                    # Elder Dragon is similar to Yuumi but is actually a buff to the player and not a unit.
                    item_names.append(item_name)
                    
                    # Iterate over the keys of data[json_key]
                    for key in data[json_key]:
                        # Check if the key ends with item_name
                        if key.endswith(item_name):
                            item = data[json_key][key]
                            image_urls.append(url_template.format(item['image']['full']))
                            break
    
    return image_urls, item_names

def download_image(url, folder_path, filename):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, filename)
    
    if not os.path.exists(file_path):
        # Download the image
        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")

def download_images(json_file_path, csv_file_path, json_key, url_template, folder_path, verbose=False):
    image_urls, item_names = get_image_urls(json_file_path, csv_file_path, json_key, url_template)
    
    for url, item_name in zip(image_urls, item_names):
        if verbose:
            print(f"Downloading {url} as {item_name}.png")
        # Use the item name from the CSV row as the filename
        filename = f"{item_name}.png"
        download_image(url, folder_path, filename)


def download_all_images():
    csvPlacementFolder = 'Data/csvPlacements/'
    latest_version = get_latest_version()
    json_csv_url_pairs = [
        ('tft-champion.json', f'{csvPlacementFolder}unit_placements.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-champion/{{}}', 'images/champions', True),
        ('tft-item.json', f'{csvPlacementFolder}item_placements.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-item/{{}}', 'images/items', False),
        ('tft-trait.json', f'{csvPlacementFolder}total_trait_placement.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-trait/{{}}', 'images/traits', False),
        ('tft-augments.json', f'{csvPlacementFolder}augment_placements.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-augment/{{}}', 'images/augments', False)
    ]
    json_key = 'data'

    for json_file, csv_file, url_template, folder_path, verbosity in json_csv_url_pairs:
        download_images(json_file, csv_file, json_key, url_template, folder_path, verbosity)



#📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜📜
def get_latest_version():
    url = 'https://ddragon.leagueoflegends.com/api/versions.json'
    response = requests.get(url)
    versions = response.json()
    return versions[0]


def update_all_json_data():
    latest_version = get_latest_version()
    investigate_json(latest_version, 'tft-champion.json')
    investigate_json(latest_version, 'tft-item.json')
    investigate_json(latest_version, 'tft-trait.json')
    investigate_json(latest_version, 'tft-augments.json')

def investigate_json(latest_version, filename):
    if os.path.exists(f'Data/DragonData/{filename}'):
        with open(f'Data/DragonData/{filename}', 'r') as file:
            champion_data = json.load(file)
            
            version = champion_data['version']
            if version != latest_version:
                download_json(latest_version, filename)
            else:
                print(f"{filename} is already up to date.")
    else:
        download_json(latest_version, filename)

def download_json(version, filename):
    url = f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/{filename}'
    response = requests.get(url)
    with open(f'Data/DragonData/{filename}', 'w') as file:
        file.write(response.text)
    print(f"Downloaded {filename}")


def update_all_dragon_data():
    os.makedirs('Data/DragonData', exist_ok=True)

    update_all_json_data()

    download_all_images()
    
    print("All dragon data updated.")
