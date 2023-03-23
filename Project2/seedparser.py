import collections
import json
import re

sample_folderpath = 'resources'
sample_filepath = sample_folderpath + '/Sanvily.json'

def getJson(filepath : str):
    with open(filepath) as file:
        seed_json : dict = json.load(file)
    return seed_json

def getLocationMap() -> dict:
    return get_sample().location_map

def get_sample():
    return Seed(sample_filepath)

pattern = 'ganon_(.+)\.json'

def getGuid(filepath : str):
    seed_guid = re.search(pattern, filepath).group(1)
    return seed_guid

def remid(oldstr : str):
    newstr = oldstr.split(':')[0]
    return newstr

class Seed():
    seed_guid = ''
    seed_json = ''

    def __init__(self, filepath : str):
        self.seed_guid = getGuid(filepath)
        self.seed_json = getJson(filepath)
        self.seed_metadata = self.seed_json.pop("meta")
        self.seed_number = self.seed_metadata['world_id']

        self.playthrough = self.seed_json.pop("playthrough")
        self.shops = self.seed_json.pop("Shops")
        self.starting_gear = self.seed_json.pop("Equipped")
        self.other_stuff = self.seed_json.pop("Special")
        self.bosses = self.seed_json.pop('Bosses')
        self.playthrough = json.dumps(self.playthrough)

        # self.items = collections.defaultdict(list)
        self.locations = {}
        for region, dic in self.seed_json.items():
            for key, value in dic.items():
                self.locations[remid(key)] = remid(value)