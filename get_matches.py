''' This file uses RitoAPI to get all the match/timeline data for
    the 100,000 matches. The matches we get are from the lists:
    BILGEWATER/br.json, tr.json, na.json, kr.json.....etc.
    It gets the data and stores them 500 matches per file.
'''

from RitoAPI import *
import os
     
chunk = 500
matches = {}

for region in regions.values():
    f = open('BILGEWATER/{region}.json'.format(region=region.upper()))
    matches[region] = json.loads(f.read())
    f.close()
    
    path = 'BILGEWATER/{region}/'.format(region=region)
    print path
    
    if not os.path.exists(path):
        os.mkdir(path)
    
    last_done = -1

    for i in range(len(matches[region])/chunk):
        if not os.path.isfile(path+'%i_%i.json'%(chunk,i)):
            last_done = i
            break
   
    if last_done == -1:
        continue
    
    api = RitoAPI(api_key, region)
    
    for j in range(last_done,len(matches[region])/chunk):
        to_save = {}
        k=chunk*j
        for match in matches[region][chunk*j:chunk*(j+1)]:
            k+=1
            r = api.get_match(match)
            
            to_save[match] = r
            time.sleep(1.2)
            print k
            
        s = json.dumps(to_save)
        filename = path+'%i_%i.json'%(chunk,j)
        f = open(filename, 'w')
        print 'writing out file ' + filename
        f.write(s)
        f.close()
       
