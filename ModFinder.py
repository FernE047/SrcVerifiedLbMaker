import requests
import csv
from time import time
from utils import prettifyTime as pT

def getRuns(mod,minimo):
    offset = minimo//200
    total = offset*200
    while offset*200 < 10000:
        data = requests.get(f"{API}runs?examiner={mod}&orderby=date&direction=asc&offset={offset * 200}&max=200").json()
        if 'data' not in data:
            return 0
        else:
            data = data["data"]
        total += len(data)
        offset += 1
        if len(data) < 200:
            return total
    lastRuns = data.copy()
    offset = 0
    while True:
        data = requests.get(f"{API}runs?examiner={mod}&orderby=date&direction=desc&offset={offset * 200}&max=200").json()["data"]
        offset += 1
        for run in data:
            if run in lastRuns:
                return total
            else:
                total += 1
    return total

API = "https://www.speedrun.com/api/v1/"

minimo = 1650
moderators = [('zx7gd1yx', '1', 22000)] #Mango_man needs to be added manually, because he has more than 20K runs

offset = 0
begin = time()
try:
    while True:
        games = requests.get(f"{API}games?offset={offset*200}&max=200&embed=moderators").json()['data']
        for game in games:
            for moderator in game['moderators']['data']:
                idd = moderator['id']
                if idd not in [a[0] for a in moderators]:
                    names = moderator['names']
                    if 'international' in names:
                        name = names['international']
                    elif 'japanese' in names:
                        name = names['japanese']
                    elif len(names.keys()):
                        name = names[list(names.keys())[0]]
                    else:
                        name = idd
                    if name == '1':
                        continue
                    runs = getRuns(idd,minimo)
                    if runs >= minimo:
                        if len(moderators) >= 201:
                            minimo = min([mod[2] for mod in moderators])
                            moderators.pop([moderators.index(worst) for worst in moderators if worst[2]==minimo][0])
                            minimo = min([mod[2] for mod in moderators])
                        moderators.append((idd,name,runs))
                        print(f"{moderators[-1]},")
        present = 200 * offset + 200
        end = time()
        duration = (end-begin)/present
        missing = duration * (26400-present)
        print(f"{present} : {int(10000*present/28000)/100}% : {minimo} : {pT(missing)}")
        if len(games)<200:
            break
        offset += 1
except:
    print("BACKUP")
print(offset)
print()
print(moderators)
print()
print(minimo)
print()
with open('moderators.csv','w',encoding = 'utf-8',newline='') as file:
    writer = csv.writer(file)
    for moderator in moderators:
        writer.writerow(moderator)
