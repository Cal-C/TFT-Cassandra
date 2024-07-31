import json
import csv
import os
import requests

#📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷📷
def get_champion_image_urls():
    champion_urls = []
    with open('DragonData/tft-champion.json') as f:
        champion_data = json.load(f)
        
        with open('unit_placements.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                champion_name = row['Unit Name']
                
                # Iterate over the keys of champion_data['data']
                for key in champion_data['data']:
                    # Check if the key ends with champion_name
                    if key.endswith(champion_name):
                        champion = champion_data['data'][key]
                        champion_urls.append(f"https://ddragon.leagueoflegends.com/cdn/14.15.1/img/tft-champion/{champion['image']['full']}")
                        break
    
    return champion_urls

def download_champion_image(url, filename):
    folder_path = 'images/champions'
    
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, filename)
    
    if not os.path.exists(file_path):
        # Download the image
        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")

def download_champion_images():
    champion_image_urls = get_champion_image_urls()
    
    for url in champion_image_urls:
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        download_champion_image(url, filename)

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
    investigate_json(latest_version, 'tft-augment.json')

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

    download_champion_images()
    
    print("All dragon data updated.")


update_all_dragon_data()
