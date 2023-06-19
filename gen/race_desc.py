import os
import requests
from bs4 import BeautifulSoup
import json


def gen_desc():
    # List of URLs to scrape
    urls = ["https://www.formula1.com/en/racing/2023/Bahrain/Circuit.html", "https://www.formula1.com/en/racing/2023/Saudi_Arabia/Circuit.html", "https://www.formula1.com/en/racing/2023/Australia/Circuit.html", "https://www.formula1.com/en/racing/2023/Azerbaijan/Circuit.html", "https://www.formula1.com/en/racing/2023/Miami/Circuit.html", "https://www.formula1.com/en/racing/2023/Monaco/Circuit.html", "https://www.formula1.com/en/racing/2023/Spain/Circuit.html", "https://www.formula1.com/en/racing/2023/Canada/Circuit.html", "https://www.formula1.com/en/racing/2023/Austria/Circuit.html", "https://www.formula1.com/en/racing/2023/Great_Britain/Circuit.html", "https://www.formula1.com/en/racing/2023/Hungary/Circuit.html", "https://www.formula1.com/en/racing/2023/Belgium/Circuit.html", "https://www.formula1.com/en/racing/2023/Netherlands/Circuit.html", "https://www.formula1.com/en/racing/2023/Italy/Circuit.html", "https://www.formula1.com/en/racing/2023/Singapore/Circuit.html", "https://www.formula1.com/en/racing/2023/Japan/Circuit.html", "https://www.formula1.com/en/racing/2023/Qatar/Circuit.html", "https://www.formula1.com/en/racing/2023/United_States/Circuit.html", "https://www.formula1.com/en/racing/2023/Mexico/Circuit.html", "https://www.formula1.com/en/racing/2023/Brazil/Circuit.html", "https://www.formula1.com/en/racing/2023/Las_Vegas/Circuit.html", "https://www.formula1.com/en/racing/2023/United_Arab_Emirates/Circuit.html", "https://www.formula1.com/en/racing/2022/EmiliaRomagna/Circuit.html", "https://www.formula1.com/en/racing/2022/France/Circuit.html", "https://www.formula1.com/en/racing/2021/Portugal/Circuit.html", "https://www.formula1.com/en/racing/2021/Russia/Circuit.html", "https://www.formula1.com/en/racing/2021/Turkey/Circuit.html", "https://www.formula1.com/en/racing/2020/Germany/Circuit.html", "https://www.formula1.com/en/racing/2020/Sakhir/Circuit.html", "https://www.formula1.com/en/racing/2019/China/Circuit.html"]

    name = ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix", "Azerbaijan Grand Prix", "Miami Grand Prix", "Monaco Grand Prix", "Spanish Grand Prix", "Canadian Grand Prix", "Austrian Grand Prix", "British Grand Prix", "Hungarian Grand Prix", "Belgian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix", "Singapore Grand Prix", "Japanese Grand Prix", "Qatar Grand Prix", "United States Grand Prix", "Mexico City Grand Prix", "São Paulo Grand Prix", "Las Vegas Grand Prix", "Abu Dhabi Grand Prix", "Emilia Romagna Grand Prix", "French Grand Prix", "Portuguese Grand Prix", "Russian Grand Prix", "Turkish Grand Prix", "Eifel Grand Prix", "Sakhir Grand Prix", "Chinese Grand Prix"]

    additional_race_names = {
        "British Grand Prix": "70th Anniversary Grand Prix",
        "Austrian Grand Prix": "Styrian Grand Prix"
    }

    # Path to the directory where you want to save the JSON files and images
    save_directory = 'data'
    image_directory = 'assets/images/track'

    # Create the directories if they don't exist
    os.makedirs(save_directory, exist_ok=True)
    os.makedirs(image_directory, exist_ok=True)

    races_info = {}

    # Iterate over the URLs
    for url, race_name in zip(urls, name):
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the desired information
            circuit_name = soup.find('span', class_='d-none d-lg-block').text.strip()
            image_url = soup.find('div', class_='f1-race-hub--map-container').find('img')['data-src'].replace('.transform/9col/image.png', '')
            image_filename = os.path.basename(image_url)
            first_gp = soup.find('p', string='First Grand Prix').find_next('p', class_='f1-bold--stat').text.strip()
            nb_laps = soup.find('p', string='Number of Laps').find_next('p', class_='f1-bold--stat').text.strip()
            length = soup.find('p', string='Circuit Length').find_next('p', class_='f1-bold--stat').text.strip()
            race_distance = soup.find('p', string='Race Distance').find_next('p', class_='f1-bold--stat').text.strip()
            lap_record = soup.find('p', string='Lap Record').find_next('p', class_='f1-bold--stat').text.strip()
            # owner = soup.find('p', string='Lap Record').find_next('p', class_='f1-bold--stat').find('span').text.strip()
            built_heading = soup.find('h2', string='When was the track built?') or soup.find('h3', string='When was the track built?')
            built = built_heading.find_next('p').text.strip()

            first_gp_heading = soup.find('h2', string='When was its first Grand Prix?') or soup.find('h3', string='When was its first Grand Prix?')
            first_gp_story = first_gp_heading.find_next('p').text.strip()

            circuit_like_heading = first_gp_heading.find_next('h2') or first_gp_heading.find_next('h3')
            circuit_like = circuit_like_heading.find_next('p').text.strip()

            why_go_heading = soup.find('h2', string='Why go?') or soup.find('h3', string='Why go?')
            why_go = why_go_heading.find_next('p').text.strip()

            best_place_heading = soup.find('h2', string='Where is the best place to watch?') or soup.find('h3', string='Where is the best place to watch?')
            best_place = best_place_heading.find_next('p').text.strip()

            lap_record_parts = lap_record.split()
            time = lap_record_parts[0]
            owner = ' '.join(lap_record_parts[1:])

            # Create a dictionary to store the extracted data
            data = {
                'name': circuit_name,
                'image': f'{image_directory}/{image_filename}',
                'first_gp': first_gp,
                'nb_laps': nb_laps,
                'length': length,
                'race_distance': race_distance,
                'lap_record': {'time' :time,
                'owner': owner},
                'built': built,
                'first_gp-story': first_gp_story,
                'like': circuit_like,
                'why': why_go,
                'where': best_place
            }

            races_info[race_name] = data

            if race_name in additional_race_names:
                additional_race_name = additional_race_names[race_name]
                races_info[additional_race_name] = data

            # Download and save the image
            image_save_path = os.path.join(image_directory, image_filename)
            image_response = requests.get(image_url)
            with open(image_save_path, 'wb') as f:
                f.write(image_response.content)
            print(f'Saved data and image from {url}')
        else:
            print(f'Error accessing URL: {url}')
    def replace_weird(data):
        replacements = {
            'Ã¡': 'á',
            'Ã³': "ó",
            'Ã\xad': 'í',
            'â\x80\x99': "'",
            'â\x80\x98': "'",
            'â\x80\x9c': '"',
            'â\x80\x9d': '"',
            'â\x80\x9e': '"',
            'â\x80\x9f': '"',
            'â\x80\x94': '-',
            'â\x80\x93': '-',
            'â\x80¦': '...',
            'â\x80\xa6': '...',
            'â\x80\x9c': '"',
            'â\x80\x9d': '"',
            'â\x80\xa2': '•',
            'â\x80\x9a': ',',
            'â\x80\x9e': '"',
            'â\x80\x9f': '"',
            'â\x80\x9d': '"',
            'â\x80\x98': "'",
            'â\x80\x99': "'",
            'â\x80\x9c': '"',
            'â\x80\x9d': '"',
            'â\x80\x9e': '"',
            'â\x80\x9f': '"',
            'â\x80\x94': '-',
            'â\x80\x93': '-',
            'â\x80¦': '...',
            'â\x80\xa6': '...',
            'â\x80\x99': "'",
            'â\x80\x98': "'",
            'â\x80\x9c': '"',
            'â\x80\x9d': '"',
            'â\x80\x9e': '"',
            'â\x80\x9f': '"',
            'â\x80\x94': '-',
            'â\x80\x93': '-',
            'â\x80¦': '...',
            'â\x80\xa6': '...',
            'â\x80\x99': "'",
            'â\x80\x98': "'",
            'â\x80\x9c': '"',
            'â\x80\x9d': '"',
            'â\x80\x9e': '"',
            'â\x80\x9f': '"',
            'â\x80\x94': '-',
            'â\x80\x93': '-',
            'â\x80¦': '...',
            'â\x80\xa6': '...'
        }

        # Iterate over the replacements and apply them to the text
        if isinstance(data, str):
            # Iterate over the replacements and apply them to the string
            for key, value in replacements.items():
                data = data.replace(key, value)

        elif isinstance(data, dict):
            # Recursively replace characters in dictionary values
            for key, value in data.items():
                data[key] = replace_weird(value)

        return data

    races_info = replace_weird(races_info)
    # Save the data as a JSON file
    json_save_path = os.path.join(save_directory, 'races_desc.json')
    with open(json_save_path, 'w', encoding='utf-8') as f:
        json.dump(races_info, f, indent=4, ensure_ascii=False)

    print("Saved race info")