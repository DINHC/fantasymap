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

pattern = 'Sanvily.json'

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
        # self.shops = self.seed_json.pop("Shops")
        # self.starting_gear = self.seed_json.pop("Equipped")
        # self.other_stuff = self.seed_json.pop("Special")
        # self.bosses = self.seed_json.pop('Bosses')
        self.playthrough = json.dumps(self.playthrough)

        self.population = self.seed_json.pop("populationRate")
        self.urban = self.seed_json.pop("urbanization")
        self.lat = self.seed_json.pop("latitude0")  
        self.tempeq = self.seed_json.pop("temperatureEquator")
        self.tempo = self.seed_json.pop("temperaturePole")
        self.prec = self.seed_json.pop("prec")
        self.options= self.seed_json.pop("options")
        self.military = self.seed_json.pop("military")
        # self.archers = self.seed_json.pop("archers")
        # self.artillery = self.seed_json.pop("artillery")
        # self.cavalary = self.seed_json.pop("cavalry")
        # self.fleet = self.seed_json.pop("fleet")
        self.coords = self.seed_json.pop("coords")
        self.cells = self.seed_json.pop("cells")
        self.c = self.seed_json.pop("c")
        self.p = self.seed_json.pop("p")
        self.g = self.seed_json.pop("g")
        self.h = self.seed_json.pop("h")
        self.area = self.seed_json.pop("area")
        self.f = self.seed_json.pop("f")
        self.t = self.seed_json.pop("t")
        # self.shops = self.seed_json.pop("Shops")
        # self.shops = self.seed_json.pop("Shops")
        self.playthrough = json.dumps(self.playthrough)





        # self.items = collections.defaultdict(list)
        self.locations = {}
        for region, dic in self.seed_json.items():
            for key, value in dic.items():
                self.locations[remid(key)] = remid(value)