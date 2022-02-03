import requests
import csv

API = "https://www.speedrun.com/api/v1/"

def getRuns(mod,minimo):
    offset = minimo//200
    total = offset*200
    while offset*200 < 10000:
        data = requests.get(f"{API}runs?examiner={mod}&orderby=date&direction=asc&offset={offset * 200}&max=200").json()
        if 'data' not in data:
            offset = 0
            continue
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

moderators = []
with open('moderators.csv','r') as file:
    reader = csv.reader(file,delimiter = ';')
    for moderator in reader:
        moderator[2] = int(moderator[2])
        print(moderator[1] + ', ')
        data = requests.get(f"{API}users/{moderator[0]}").json()["data"]
        if data["location"]:
            flag = f":flag_{data['location']['country']['code']}:"
        else:
            flag = ":united_nations:"
        if flag == ":flag_ca/qc":
            flag = ":flag_ca:"
        elif flag == ":flag_gb/eng:":
            flag = ":flag_gb:"
        moderator.append(flag)
        if moderator[1] == '1':
            continue
        if moderator[2] < 10000:
            moderator[2] = getRuns(moderator[0],moderator[2])
        else:
            moderator[2] = getRuns(moderator[0],9600)
        moderators.append(moderator)
moderators.sort(
    key=lambda x: x[2], reverse=True
)

import datetime

print(moderators)

print(datetime.datetime.now().date())

position = 0
lastValue = float('inf')

for n, i in enumerate(moderators):
    if i[2] != lastValue:
        position = n + 1
    lastValue = i[2]
    print(
        f"`{position}.`{i[3]}`{i[1]} {' ' * (23-len(str(n+1))-len(i[1]))} {i[2]}`"
    )
