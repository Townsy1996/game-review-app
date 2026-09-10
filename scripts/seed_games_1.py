import requests
from dotenv import load_dotenv
import os

games = [
    {
        "title": "Yakuza 0 Director's Cut",
        "platforms": ["PC", "PlayStation 5", "Xbox Series S/X"],
        "genres": ["Action", "RPG", "Fighting"],
        "release_date": "2025-06-05",
        "developer": "RGG Studio",
        "publisher": "Sega",
        "age_rating": "PEGI 18",
        "description": "Discover the decadence and danger of 1980's Japan as you fight like hell through its neon-lit entertainment districts in the definitive edition of the action-adventure crime drama that created yakuza legends.",
        "is_multiplayer": False,
        "is_couch_coop": False,
        "cover_image_url": "yakuza_0_dummy_jpeg",
    },
    {
        "title": "Halo: Campaign Evolved",
        "platforms": ["Xbox Series S/X", "PC", "PlayStation 5"],
        "genres": ["Adventure", "Shooter"],
        "release_date": "2026-07-28",
        "developer": "Halo Studios",
        "publisher": "Xbox Game Studios",
        "age_rating": "PEGI 16",
        "description": "Halo: Campaign Evolved is a faithful yet modernized remake of Halo: Combat Evolved’s campaign, rebuilt from the ground up.",
        "is_multiplayer": True,
        "is_couch_coop": True,
        "cover_image_url": "dummy-halo-cover.jpeg",
    },
    {
        "title": "Red Dead Redemption 2",
        "platforms": [
            "PC",
            "PlayStation 4",
            "PlayStation 5",
            "Xbox One",
            "Xbox Series S/X",
        ],
        "genres": ["Action", "Adventure", "Shooter"],
        "release_date": "2018-10-26",
        "developer": "Rockstar Games",
        "publisher": "Rockstar Games",
        "age_rating": "PEGI 18",
        "description": "Arthur Morgan and the Van der Linde Gang are outlaws on the run. With federal agents and bounty hunters massing on their heels, the gang must rob, steal, and fight their way across the rugged heartland in order to survive.",
        "is_multiplayer": True,
        "is_couch_coop": False,
        "cover_image_url": "red_dead_2_dummy_jpeg",
    },
    {
        "title": "Elden Ring",
        "platforms": [
            "PC",
            "PlayStation 4",
            "PlayStation 5",
            "Xbox One",
            "Xbox Series S/X",
            "Nintendo Switch 2",
        ],
        "genres": ["Action", "RPG"],
        "release_date": "2022-02-25",
        "developer": "FromSoftware",
        "publisher": "Bandai Namco Entertainment",
        "age_rating": "PEGI 16",
        "description": "THE CRITICALLY ACCLAIMED FANTASY ACTION RPG. Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become an Elden Lord in the Lands Between.",
        "is_multiplayer": True,
        "is_couch_coop": False,
        "cover_image_url": "elden_ring_dummy.jpeg",
    },
    {
        "title": "Cyberpunk 2077",
        "platforms": [
            "PC",
            "PlayStation 4",
            "PlayStation 5",
            "Xbox One",
            "Xbox Series S/X",
            "Nintendo Switch 2",
        ],
        "genres": ["Action", "RPG", "Shooter"],
        "release_date": "2020-12-10",
        "developer": "CD Projekt Red",
        "publisher": "CD Projekt",
        "age_rating": "PEGI 18",
        "description": "Cyberpunk 2077 is an open-world, action-adventure RPG set in the dark future of Night City — a dangerous megalopolis obsessed with power, glamor, and ceaseless body modification.",
        "is_multiplayer": False,
        "is_couch_coop": False,
        "cover_image_url": "cyberpunk_2077_dummy_jpeg",
    },
]

load_dotenv()
SEED_USER = os.environ.get("SEED_USERNAME")
SEED_PASSWORD = os.environ.get("SEED_PASSWORD")


def get_access_token():
    payload = {"username": SEED_USER, "password": SEED_PASSWORD}
    url = "http://127.0.0.1:8000/users/token"
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()

        print(f"Success! Token retrieved")
        return data.get("access_token")
    else:
        print(f"Failed ({response.status_code}):", response.text)
        return None


def seed_games(access_token):

    url = "http://127.0.0.1:8000/games/"
    headers = {"Authorization": f"Bearer {access_token}"}

    for game in games:
        response = requests.post(url, json=game, headers=headers)
        if response.status_code == 201:
            print(f"Created: {game['title']}")
        else:
            print(
                f"Failed ({response.status_code}) for {game['title']}: {response.text}"
            )


if __name__ == "__main__":
    token = get_access_token()
    if token:
        seed_games(token)
    else:
        print("Could not authenticate — aborting seed.")
