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
    
    last_done = 0
    for i in range(len(matches[region])/chunk):
        if not os.path.isfile(path+'%i_%i.json'%(chunk,i)):
            last_done = i
            break
    
    api = RitoAPI(api_key, region)
    
    for j in range(last_done,len(matches[region])/chunk):
        to_save = {}
        #print "{num} matches in {region}".format(num=len(matches[region]), region=region)
        k=chunk*j
        for match in matches[region][chunk*j:chunk*(j+1)]:
            k+=1
            r = api.get_match(match)
            
            to_save[match] = r
            #t = time.clock()
            time.sleep(1.2)
            #print "tried to sleep for 2 secs, actually slept for {time} secs".format(time=time.clock()-t)
            print k
            #if i == 50:
            #    break
            
        s = json.dumps(to_save)
        filename = path+'%i_%i.json'%(chunk,j)
        f = open(filename, 'w')
        print 'writing out file ' + filename
        f.write(s)
        f.close()
       
