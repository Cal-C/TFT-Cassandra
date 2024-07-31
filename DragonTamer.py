import json
import csv
import os
import requests

#📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷
def get_image_urls(json_file_path, csv_file_path, json_key, url_template):
    image_urls = []
    with open(f'DragonData/{json_file_path}') as f:
        data = json.load(f)
        
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            first_row = next(csv_reader)
            
            for row in csv_reader:
                item_name = row['Name']
                
                # Iterate over the keys of data[json_key]
                for key in data[json_key]:
                    # Check if the key ends with item_name
                    if key.endswith(item_name):
                        item = data[json_key][key]
                        image_urls.append(url_template.format(item['image']['full']))
                        break
    
    return image_urls

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

def download_images(json_file_path, csv_file_path, json_key, url_template, folder_path):
    image_urls = get_image_urls(json_file_path, csv_file_path, json_key, url_template)
    
    for url in image_urls:
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        download_image(url, folder_path, filename)

def download_all_images():
    latest_version = get_latest_version()
    json_csv_url_pairs = [
        ('tft-champion.json', 'unit_placements.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-champion/{{}}', 'images/champions'),
        ('tft-item.json', 'item_placements.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-item/{{}}', 'images/items'),
        ('tft-trait.json', 'total_trait_placement.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-trait/{{}}', 'images/traits'),
        ('tft-augments.json', 'augment_placements.csv', f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/tft-augment/{{}}', 'images/augments')
    ]
    json_key = 'data'

    for json_file, csv_file, url_template, folder_path in json_csv_url_pairs:
        download_images(json_file, csv_file, json_key, url_template, folder_path)



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
    if os.path.exists(f'DragonData/{filename}'):
        with open(f'DragonData/{filename}', 'r') as file:
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
    with open(f'DragonData/{filename}', 'w') as file:
        file.write(response.text)
    print(f"Downloaded {filename}")


def update_all_dragon_data():
    update_all_json_data()

    download_all_images()
    
    print("All dragon data updated.")


update_all_dragon_data()
