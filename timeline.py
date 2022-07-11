import matplotlib.pyplot as plt
import json
from datetime import datetime

#cooldown = 5 #set your cooldown from main script
from main import cooldown
period = 600 #period of ticks in seconds

with open('data.txt', 'r') as f:
    data = f.read().replace('\'', '"')

splitted_data = data.split('\n')
splitted_data.remove('')

thinned_data = []



###data averaging###
summ_temp, summ_hum, counter = 0, 0, 0
lenght = len(splitted_data)
for i in range(0, lenght):
    data_i = json.loads(splitted_data[i])
    summ_temp += float(data_i['t'])
    summ_hum += float(data_i['h'])
    counter += 1
    if (i % (period // cooldown) == 0 and i != 0):
        data_i.update({'t': float(summ_temp / (period // cooldown))})
        data_i.update({'h': float(summ_hum / (period // cooldown))})
        thinned_data.append(data_i)
        summ_temp, summ_hum, counter = 0, 0, 0
    elif i == 0:
        data_i.update({'t': float(summ_temp)})
        data_i.update({'h': float(summ_hum)})
        thinned_data.append(data_i)
        summ_temp, summ_hum, counter = 0, 0, 0
    elif (i == lenght - 1):
        data_i.update({'t': float(summ_temp / ((lenght - 1) % (period // cooldown)))})
        data_i.update({'h': float(summ_hum / ((lenght - 1) % (period // cooldown)))})
        thinned_data.append(data_i)

###w/o averaging
#for i in range(len(splitted_data)):
#    if i % (period // cooldown) == 0:
#summ_tempthinned_data.append(splitted_data[i])

print('Lenght before:', lenght, '\nLenght after:', len(thinned_data))

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
plt.subplots_adjust(top=0.94, bottom=0.295, left=0.065, right=0.985, hspace=0.154, wspace=0.205)
plt.savefig('picture.png')
plt.show()