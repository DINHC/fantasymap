import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from login import postgres_username, postgres_password
from tables import LocationMetadata
import re

db_string = f'postgresql://{postgres_username}:{postgres_password}@localhost/fantasymap'

db = create_engine(db_string, echo=True)
Session = sessionmaker(bind=db)

locations_filepath = 'Sanvily.json'

def cleanJson(json):
     return re.sub('\/\/.*\n','',str(json))

with open(locations_filepath) as lfile:
    content = lfile.read()
    overworld_locations : dict = json.loads(cleanJson(content))

dlocations_filepath = 'resources\Sanvily.json'

def repregion(content):
    pattern = "(^[ \t]*)(\"[\w+\' ]+\"): {"
    def repl(m):
        tabs = m.group(1)
        front = tabs+'{'
        region = m.group(2)
        return f'{front}\n{tabs}\t\"region\": {region},'
    return re.sub(pattern, repl, content, flags =re.MULTILINE)

with open(dlocations_filepath, 'r') as dfile:
    dcontent = dfile.read()
    dungeon_locations : dict = json.loads(cleanJson(content))

def makeLocationMetadata():
    ###################
    # Start of Session
    ###################
    session = Session()

    ##########
    # Location Data
    ##########
    table = LocationMetadata.__table__

    # table.drop(db)
    # table.create(db)

    def add_loc_from_region(region : dict):
        region_name = region['name']
        print(f'Region: {region_name}')
        if type(region) == dict and 'children' in region.keys(): 
            for child in region['children']:
                add_loc_from_region(child)
        elif 'map_locations' in region.keys(): 
            location = region['name']
            print(f'\t\tLocation: {location}')
            geography = region['map_locations']
            print(f'\t\tGeography: {geography}')
            point = geography[0]
            sections = region['sections']
            print(f'\t\tSections: {sections}')
            count = 0
            rules = []
            for section in sections:
                if 'item_count' in section.keys():
                    count+= section['item_count']
                if 'access_rules' in section.keys(): 
                    rules.extend(section['access_rules'])
                data = { 'location': location,
                    'x':point['x'], 
                    'y':point['y'], 
                    'map' : point['map'],
                    'requirements' : rules,
                    'region' : region_name,
                    'count' : count
                }
        else:
            print(f"Bad Location? {region['name']}")

    for region in overworld_locations:
        add_loc_from_region(region)
    for region in dungeon_locations:
        add_loc_from_region(region)

    session.commit()
    ##########
    # Commit/End Location Data
    ##########


    session.close()
    ###################
    # Session Closed
    ###################