import matplotlib.pyplot as plt
import json
from datetime import datetime

period = 360 #period of ticks in seconds
#cooldown = 5 #set your cooldown from main script
from main import cooldown

with open('data.txt', 'r') as f:
    data = f.read().replace('\'', '"')

splitted_data = data.split('\n')
splitted_data.remove('')

thinned_data = []



###data averaging###
summ_temp, summ_hum = 0, 0
for i in range(1, len(splitted_data)):
    data_i = json.loads(splitted_data[i])
    summ_temp += float(data_i['t'])
    summ_hum += float(data_i['h'])
    if i % (period // cooldown) == 0:
        data_i.update({'t': float(summ_temp / (period // cooldown))})
        data_i.update({'h': float(summ_hum / (period // cooldown))})
        thinned_data.append(data_i)
        summ_temp, summ_hum = 0, 0

###w/o averaging
#for i in range(len(splitted_data)):
#    if i % (period // cooldown) == 0:
#summ_tempthinned_data.append(splitted_data[i])

print('Lenght before:', len(splitted_data), '\nLenght after:', len(thinned_data))


list_data = {'time': [], 'temp': [], 'hum': []}

for once in thinned_data:
    list_data['temp'].append(round(float(once['t']), 1))
    list_data['hum'].append(round(float(once['h']), 1))
    list_data['time'].append(datetime.fromtimestamp(round(float(once['time']), 0)).strftime("%H:%M:%S %d.%m.%Y"))


#print(list_data)

#plt.plot(list_data['time'], list_data['temp'], list_data['hum'])
#plt.plot(list_data['time'], list_data['temp'])

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10, 7))
ax[0].plot(list_data['time'], list_data['temp'])
ax[0].set_xlabel('time')
ax[0].set_ylabel('temperature')
#ax[0].set_ylim([0, max(list_data['temp'])])

ax[1].plot(list_data['time'], list_data['hum'])
ax[1].set_xlabel('time')
ax[1].set_ylabel('humidity')
ax[1].set_ylim([0, 100])

fig.tight_layout()
fig.suptitle('temperature and humidity')
fig.canvas.manager.set_window_title('temptrack')
plt.xticks(rotation=80, ha='right')
plt.subplots_adjust(top=0.92, bottom=0.3, right=0.98)
plt.savefig('picture.png')
plt.show()