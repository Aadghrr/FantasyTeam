import requests, json, itertools
from multiprocessing import Process
from collections import defaultdict
import datetime

ep = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(ep)
j = json.loads(r.content)

with open('old/FPL_DATA_'+datetime.datetime.now().strftime('%Y%m%d'),'w') as f:
    f.write(json.dumps(j))

#To reduce number of iterables
MIN_PLAYER_PTS = 35

gk =[[x['web_name'],x['total_points'],x['now_cost'] ] for x in j['elements'] if x['element_type']==1 and x['total_points']>=MIN_PLAYER_PTS]
de = [[x['web_name'],x['total_points'],x['now_cost'] ] for x in j['elements'] if x['element_type']==2 and x['total_points']>=MIN_PLAYER_PTS]
mi = [[x['web_name'],x['total_points'],x['now_cost'] ] for x in j['elements'] if x['element_type']==3 and x['total_points']>=MIN_PLAYER_PTS]
at = [[x['web_name'],x['total_points'],x['now_cost'] ] for x in j['elements'] if x['element_type']==4 and x['total_points']>=MIN_PLAYER_PTS]

gp = itertools.permutations(gk,1)
dp = itertools.permutations(de,4)
mp = itertools.permutations(mi,4)
ap = itertools.permutations(at,2)

dd = defaultdict(list)
squadCodes = {
    3: 'Arsenal',
    7: 'AstonVilla',
    36: 'Brighton',
    90: 'Burnley',
    8: 'Chelsea',
    31: 'CrystalPalace',
    11: 'Everton',
    54: 'Fulham',
    13: 'Leicester',
    2: 'Leeds',
    14: 'Liverpool',
    43: 'ManchesterCity',
    1: 'ManchesterUnited',
    4: 'NewcastleUnited',
    49: 'SheffieldUnited',
    20: 'Southampton',
    6: 'TottenhamHostpur',
    35: 'WestBrom',
    21: 'WestHam',
    39: 'Wolves'}



for i in j['elements']:
    dd[squadCodes[i['team_code']]].append(i)

def getBestPerm(p,val):
    m = 0
    best = []
    for i in p:
      if sum([k[1] for k in i])> m and sum([k[2] for k in i]) < val:
          m = sum([k[1] for k in i])
          best=i
    print(best)
    return

if __name__=='__main__':
    procs = [Process(target=getBestPerm,args=x) for x in [(gp,100),(dp,200),(mp,300),(ap,350)]]
    for proc in procs:
        proc.start()
        proc.join()
