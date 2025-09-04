import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['name'].title()}")
        print(f"ID: {data['id']}")
        print("Types:", ", ".join(t['type']['name'] for t in data['types']))
        print("Abilities:", ", ".join(a['ability']['name'] for a in data['abilities'])) 

pokemon_name = "pikachu"
get_pokemon_info(pokemon_name)