from RitoAPI import *
import os

brawler_names = {}

def get_items_bought(timeline_json):
    items = []
    for frame in timeline_json['frames']:
        if 'events' in frame:
            for event in frame['events']:
                if event['eventType'] == 'ITEM_PURCHASED':
                    items.append(event['itemId'])
    
    return items
    
def get_brawlers_bought(timeline_json):
    brawlers = []
    items = get_items_bought(timeline_json)
    for item in items:
        if item in range(3611,3615):
            brawlers.append(item)
    
    return brawlers

def get_item_name(items):
    ret = []
    for item in items:
        if item not in brawler_names:
            brawler_names[item] = api.get_item(item)['name']
        ret.append(brawler_names[item])
    return ret

def calc_distro(all_items):
    counts = {}
    for match_items in all_items:
        for brawler in set(match_items[1]):
            if brawler not in counts:
                counts[brawler] = match_items[1].count(brawler)
            else:
                counts[brawler] += match_items[1].count(brawler)
    return counts
    
api = RitoAPI(api_key, 'na')
to_check = []
for region in regions.values():
    path = 'BILGEWATER/{region}/'.format(region=region)
    if os.path.exists(path):
        to_check += map(lambda x: path+x, os.listdir(path))
print to_check

distros = {}
for file in to_check:
    f = open(file)
    data = json.loads(f.read())
    f.close()

    stats = []
    for match in data.values():
        if not match: continue
        if 'timeline' not in match: continue
        
        timeline = match['timeline']
        time = match['matchCreation']
        brawlers_bought = get_brawlers_bought(timeline)
        items = get_item_name(brawlers_bought)
        #print items
        stats.append((time, items))
    
    distro = calc_distro(stats)
    denom = float(sum(distro.values()))
    for key in distro.keys():
        distro[key] /= denom
        
    distros[file] = distro
    
print distros