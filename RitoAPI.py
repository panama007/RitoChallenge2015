''' This file contains a RitoAPI class used to interact with the Riot API
    there are methods declared for getting matches/items/summoner's, as well
    as constants for the regions, and urls(only used in here).
'''


import requests
import json
import time

api_key = 'd381a6e7-8837-49d7-9264-945feda46dfc'

url = {'base' : 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
       'static' : 'https://global.api.pvp.net/api/lol/static-data/{region}/{url}',
       'summoner_by_name' : 'v{version}/summoner/by-name/{names}',
       'summoner_by_id' : 'v{version}/summoner/{ids}',
       'match' : 'v{version}/match/{id}',
       'item' : 'v{version}/item/{id}'}

api_versions = {'summoner' : '1.4',
                'match' : '2.2',
                'item' : '1.2'}
             
regions = {'north_america' : 'na',
           'brazil' : 'br',
           'europe_north_east' : 'eune',
           'europe_west' : 'euw',
           'korea' : 'kr',
           'latin_america_north' : 'lan',
           'latin_america_south' : 'las',
           'oceania' : 'oce',
           'russia' : 'ru',
           'turkey' : 'tr'}

class RitoAPI(object):
    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region
        
    def _request(self, api_url, params={}, base='base'):
        print api_url
        args={'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        if base == 'base':
            response = requests.get(url[base].format(proxy=self.region,
                                                     region=self.region,
                                                     url=api_url),
                                    params=args)
        elif base == 'static':
            response = requests.get(url[base].format(region=self.region,
                                                     url=api_url),
                                    params=args)
        #print response.status_code
        if response.status_code == 429:
            print 'hit user limit? {bool}, waiting 5 seconds'.format(bool=('Retry-After' in response.headers or 'Retry-After'.lower() in response.headers))
            time.sleep(5)
            self._request(api_url)
        else:
            try:
                r = response.json()
            except:
                print response
                return
            print "sending response for " + api_url
            return response.json()
            
    def get_summoners(self, summoners, name=True):
        if type(summoners) == type([]): summoners = ','.join(summoners)
        if name:
            api_url = url['summoner_by_name'].format(version=api_versions['summoner'],
                                                     names=summoners)
        else:
            api_url = url['summoner_by_id'].format(version=api_versions['summoner'],
                                                   ids=summoners)
        return self._request(api_url)       
        
    def get_match(self, id):
        api_url = url['match'].format(version=api_versions['match'],
                                      id=id)
        return self._request(api_url, params={'includeTimeline':'true'})
        
    def get_item(self, id):
        api_url = url['item'].format(version=api_versions['item'],
                                     id=id)
        return self._request(api_url, base='static')
