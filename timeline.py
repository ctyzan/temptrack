import matplotlib.pyplot as plt
import json
from datetime import datetime

period = 150 #period of ticks in seconds
cooldown = 5 #set your cooldown from main script
#from main import cooldown

with open('data.txt', 'r') as f:
    data = f.read().replace('\'', '"')

splitted_data = data.split('\n')
splitted_data.remove('')

thinned_data = []

for i in range(len(splitted_data)):
    if i % (period // cooldown) == 0:
        thinned_data.append(splitted_data[i])


print('Lenght before:', len(splitted_data), '\nLenght after:', len(thinned_data))


list_data = {'time': [], 'temp': [], 'hum': []}

for once in thinned_data:
    once_dict = json.loads(once)
    list_data['temp'].append(round(float(once_dict['t']), 1))
    list_data['hum'].append(round(float(once_dict['h']), 0))
    list_data['time'].append(datetime.fromtimestamp(round(float(once_dict['time']), 0)).strftime("%H:%M:%S %d.%m.%Y"))


#print(list_data)

#plt.plot(list_data['time'], list_data['temp'], list_data['hum'])
#plt.plot(list_data['time'], list_data['temp'])

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(list_data['time'], list_data['temp'])
ax[0].set_xlabel('time')
ax[0].set_ylabel('temperature')

ax[1].plot(list_data['time'], list_data['hum'])
ax[1].set_xlabel('time')
ax[1].set_ylabel('humidity')

fig.tight_layout()
fig.suptitle('temperature and humidity')
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(top=0.92, bottom=0.3, right=0.98)
plt.show()
