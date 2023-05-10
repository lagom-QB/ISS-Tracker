import requests
import pandas as pd
import numpy as np

from prettymaps import *

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm

from geopy.geocoders import Nominatim

plt.rcParams.update({'font.size': 12})

def get_iss_position():
    """Get the current position of the ISS"""
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]
    return lat, lon

def get_iss_astros():
    """Get the astronauts currently in space"""
    response = requests.get("http://api.open-notify.org/astros.json")
    response.raise_for_status()
    names = [person["name"] for person in response.json()["people"]]
    crafts = [person["craft"] for person in response.json()["people"]]
    return names, crafts

def checkOcean(lat, lon):
    ''''Returns True if coordinates are in the ocean, False otherwise'''
    geolocator = Nominatim(user_agent="iss")
    max_attampts = 5
    attempt_count = 0

    while True:
        curr_location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        # print(f"attempt_count: {attempt_count}")
        if curr_location is None:
            # print(f"Location is in the sea")
            return True
        else:
            print(f"Getting address of {curr_location}")
            # Check if the curr_location is in the ocean
            address = curr_location.address.lower()
            # Return true and break out of while if the address contains the word 'ocean' or 'sea' or 'lake' or 'river' or 'bay' or there is no address
            if 'ocean' in address or 'sea' in address:
                # print(f"Attempt: {attempt_count}, \n Address: {curr_location.address}, \n In ocean")
                return True
            else:
                # print(f"Attempt: {attempt_count}, \n Address: {curr_location.address}, \n Not in ocean")
                return False
            
def drawSea(location, people, craft_dict):
    print(f"{location} is in the ocean")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#00aa99')
    # print coordinates at the bottom left
    ax.text(0.63, 0.97, f"({float(location[0])}, {float(location[1])})",
            fontfamily='monospace', fontsize=12)
    ax.text(0.83, 0.95, "In the sea", fontfamily='monospace', fontsize=8)
    ax.tick_params(axis='both', which='both', colors='white', labelsize=6)
    # print the number of people and the names of the people in the bottom left
    ax.text(0.63, 0.17, f"{len(people)} people in the ISS\n",
            fontfamily='monospace', fontsize=10)
    ax.text(0.63, 0.14, "ISS\n", fontfamily='monospace', fontsize=9)
    ax.text(0.83, 0.14, "Shenzhou 15\n", fontfamily='monospace', fontsize=9)
    ax.text(0.63, 0.02, "\n".join(craft_dict['ISS']),
            fontfamily='monospace', fontsize=6)
    ax.text(0.83, 0.10, "\n".join(craft_dict['Shenzhou 15']),
            fontfamily='monospace', fontsize=6)
    ax.tick_params(axis='both', which='both', colors='white', labelsize=6)
    # Remove the border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.savefig('output.jpg', dpi=10, bbox_inches='tight', pad_inches=0,
                facecolor='auto', edgecolor='auto')
    plt.show()

    return #fig, ax No need to return anything !!!

def drawLand(location, radius, plot_layers, plot_style, people, craft_dict):
    fig, ax = plt.subplots(figsize=(8, 6))#
    ax.set_axis_off()
    map = plot(
        query = (float(location[0]), float(location[1])),
        radius = radius,
        layers=plot_layers,
        style=plot_style,
        ax=ax,
        credit=False,
        circle=True,
        dilate=True,
        scale_x=.25,
        scale_y=.25,
    )
    # print the number of people and the names of the people in the bottom left
    ax.text(0.63, 
            0.17, 
            f"{len(people)} people in the ISS\n", 
            bbox=dict(facecolor='red', alpha=0.5), 
            fontfamily = 'monospace', 
            # fontsize=14
             )#,fontsize=16
    ax.text(0.63, 
            0.14, 
            f'ISS\n' ,
            bbox=dict(facecolor='red', alpha=0.5), 
            fontfamily = 'monospace', 
            # fontsize=12
            )#fontsize=14
    ax.text(0.83, 
            0.14, 
            f'Shenzhou 15\n' ,
            bbox=dict(facecolor='red', alpha=0.5), 
            fontfamily = 'monospace', 
            # fontsize=12
            )#fontsize=14
    ax.text(0.63, 
            0.02, 
            "\n".join(craft_dict['ISS']) ,
            bbox=dict(facecolor='red', alpha=0.5), 
            fontfamily = 'monospace', 
            # fontsize=10
            )#fontsize=9
    ax.text(0.83, 
            0.10, 
            "\n".join(craft_dict['Shenzhou 15']) ,
            bbox=dict(facecolor='red', alpha=0.5), 
            fontfamily = 'monospace', 
            # fontsize=10
            )
    ax.tick_params(axis='both', which='both', colors='white', labelsize=1)

    plt.show()
    fig.savefig('output.jpg', dpi=100, pad_inches=0) #papertype='letter',bbox_inches='tight',
    
    return #fig, ax No need to return anything !!!

def drawMapWithPrettymaps(location, radius = 15000):
    '''Returns a map of the location with prettymaps or Just a blue map and the coordinates if the location is in the ocean'''
    if location is None:
        raise ValueError("Location cannot be None")
    plot_layers = {
        'green': {
            'tags': {
                'landuse': 'grass',
                'natural': ['island', 'wood'],
                'leisure': 'park'
            }
        },
        'forest': {
            'tags': {
                'landuse': 'forest'
            }
        },
        'water': {
            'tags': {
                'natural': ['water', 'bay']
            }
        },
        'parking': {
            'tags': {
                'amenity': 'parking',
                'highway': 'pedestrian',
                'man_made': 'pier'
            }
        },
        'streets': {
            'width': {
                'motorway': 5,
                'trunk': 4,
                'primary': 3.5,
                'secondary': 3,
                'tertiary': 2.5,
                'residential': 2,
                'service': 1.5,
                'pedestrian': 1,
                'footway': 1,
            }
        }
        }
    plot_style = {
        'padding': 0.01,
        'perimeter': {'fc': '#F2F4CB', 'ec': '#2F3737', 'hatch': 'ooo...','lw': 4, 'zorder': 7},
        "background": {
            "fc": "#F2F4CB",
            "ec": "#dadbc1",
            "hatch": "ooo...",
        },
        "perimeter": {
            "fc": "#F2F4CB",
            "ec": "#dadbc1",
            "lw": 0,
            "hatch": "ooo...",
        },
        "green": {
            "fc": "#D0F1BF",
            "ec": "#2F3737",
            "lw": 1,
        },
        "forest": {
            "fc": "#64B96A",
            "ec": "#2F3737",
            "lw": 1,
        },
        "water": {
            "fc": "#a1e3ff",
            "ec": "#2F3737",
            "hatch": "ooo...",
            "hatch_c": "#85c9e6",
            "lw": 1,
        },
        "parking": {
            "fc": "#F2F4CB",
            "ec": "#2F3737",
            "lw": 1,
        },
        "streets": {
            "fc": "#2F3737",
            "ec": "#475657",
            "alpha": 1,
            "lw": 0,
        },
        "building": {
            "palette": [
                "#FFC857",
                "#E9724C",
                "#C5283D"
            ],
            "ec": "#2F3737",
            "lw": 0.5,
        }}

        # Check if the location is in the ocean
    people, crafts = get_iss_astros()
    
    # Combine into a dictionary with the craft as the key and the people as the value
    craft_dict = {}
    for craft, person in zip(crafts, people):
        if craft not in craft_dict:
            craft_dict[craft] = []
        craft_dict[craft].append(person)
    # print(craft_dict)
    if not checkOcean(location[0], location[1]):
        print(f"{location} is not in the ocean")
        # Draw a map with just the coordinates
        figure = drawLand(location, radius, plot_layers, plot_style, people, craft_dict)
    else:
        figure = drawSea(location, people, craft_dict)
    return figure

location = get_iss_position()
# location = ('38.6910', '75.9310') #Definitely not in the sea
# location = ('-44.4614', '-30.4322') #Definitely in the sea

drawMapWithPrettymaps(location)
# img, ax = drawMapWithPrettymaps(location)
# img.savefig('output.jpg', dpi=10,  bbox_inches='tight', pad_inches=1,
#           facecolor='auto', edgecolor='auto', orientation='landsca #papertype='letter',pe')