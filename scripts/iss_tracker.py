import requests
import pandas as pd
import numpy as np

from prettymaps import *

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm

from datetime import date

from geopy.geocoders import Nominatim
from geopy.point import Point
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

plt.rcParams.update({'font.family': ['Arial Unicode MS',
                                     'sans-serif'],
                     'font.monospace': ['Courier New',
                                        'Terminal',
                                        'monospace']})

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
    point = Point(location[0], location[1])
    geolocator = Nominatim(user_agent="iss")
    location_n = geolocator.reverse(point, exactly_one=True)
    
    plt.title(f"Current location of ISS\n{location_n}", fontsize=10, fontweight=700, fontfamily='monospace')

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#00aa99')
    # print coordinates at the bottom left
    ax.text(0.83, 0.95, f"{date.today()}", fontsize=10, fontweight=700, fontfamily='monospace')
    ax.text(0.83, 0.90, "In the sea", fontfamily='monospace', fontsize=8)
    ax.tick_params(axis='both', which='both', colors='white', labelsize=6)

    y_start = 0.37
    # print the number of people and the names of the people in the bottom left
    ax.text(0.63, y_start, f"{len(people)} people in the ISS\n", fontsize=16, fontweight=700, fontfamily='monospace')
    for craft, passengers in craft_dict.items():
        ax.text(0.65, y_start - 0.03, f'{craft}\n', fontsize=12, fontweight=700, fontfamily='monospace')
        for i, passenger in enumerate(passengers):
            text_y = y_start - (0.02 * i)
            ax.text(0.80, text_y, passenger, fontsize=8, fontfamily='monospace')
        ax.tick_params(axis='both', which='both', colors='white', labelsize=.1)
        y_start -= (0.1 + 0.05 * len(passengers))/2
    
    # Remove the border
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.savefig('output.jpg', 
                dpi=300,
                bbox_inches='tight',
                pad_inches=0,
                facecolor='auto',
                edgecolor='auto')
                # papertype='letter')
    plt.show()

    return #No need to return anything !!!

def drawLand(location, radius, plot_layers, plot_style, people, craft_dict):
    fig, ax = plt.subplots(figsize=(6, 10))#
    ax.set_axis_off()
    map = plot(
        query = (float(location[0]), float(location[1])),
        radius = radius,
        layers=plot_layers,
        style=plot_style,
        ax=ax,
        credit=False,
        circle=True,
        # circle_params=circle_params,
        dilate=True,
        scale_x=.75,
        scale_y=.75,
    )

    ax.set_aspect('equal','box')

    geolocator = Nominatim(user_agent="iss")
    location_n = geolocator.reverse(str(location[0]) + ", " + str(location[1]))
    
    plt.title(f"Current location of ISS\n{location_n}", fontsize=10, fontweight=700, fontfamily='monospace')
    # plt.savefig('output.jpg', dpi=100, pad_inches=0) #papertype='letter',bbox_inches='tight',
    plt.savefig('output.jpg', 
                dpi=15,
                bbox_inches='tight',
                pad_inches=0,
                facecolor='auto',
                edgecolor='auto')
                # papertype='letter')
    plt.show()

    return #fig, ax No need to return anything !!!

def drawMapWithPrettymaps(location, radius = 30000):
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
                'primary': 3.7,
                'secondary': 3.5,
                'tertiary': 3.2,
                'residential': 3,
                'service': 1.5,
                'pedestrian': 1.2,
                'footway': 1.2,
            }
        }
        }
    plot_style = {
        # 'padding': 0.1,
        'perimeter': {'fc': '#F2F4CB', 
                      'ec': '#2F3737', 
                      'hatch': 'ooo...',
                      'lw': 1, 
                      'zorder': 7},
        "background": {
            "fc": "#F2F4CB",
            "ec": "#dadbc1",
            "hatch": "o.o.o.",
        },
        "perimeter": {
            "fc": "#F2F4CB",
            "ec": "#dadbc1",
            "lw": 0.8,
            "hatch": "o..o..",
        },
        "green": {
            "fc": "#D0F1BF",
            "ec": "#2F3737",
            "lw": 1.6,
        },
        "forest": {
            "fc": "#64B96A",
            "ec": "#2F3737",
            "lw": 1.6,
        },
        "water": {
            "fc": "#a1e3ff",
            "ec": "#2F3737",
            "hatch": "ooo...",
            "hatch_c": "#85c9e6",
            "lw": 1.6,
        },
        "parking": {
            "fc": "#F2F4CB",
            "ec": "#2F3737",
            "lw": 1.6,
        },
        "streets": {
            "fc": "#2F3737",
            "ec": "#475657",
            "alpha": 1,
            "lw": 0.8,
        },
        "building": {
            "palette": [
                "#FFC857",
                "#E9724C",
                "#C5283D"
            ],
            "ec": "#2F3737",
            "lw": 1.2,
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
# img.savefig('output.jpg', dpi=10,  bbox_inches='tight', pad_inches=1,facecolor='auto', edgecolor='auto', orientation='landscape', papertype='letter')
