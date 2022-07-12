import matplotlib.pyplot as plt
import json
from datetime import datetime
import math
import argparse

#cooldown = 5 #set your cooldown from main script
from main import cooldown


parser = argparse.ArgumentParser(description='Graph generator ')
parser.add_argument('-s', '--show-graph', default=1,
                    help='1 — show temp and hum graph, 0 — not',
                    choices=['1', '2'])
parser.add_argument('-p', '--period', type=int,
                    help='Period of ticks in seconds', metavar='seconds',
                    default=600)
parser.add_argument('-t', '--ticks', default=75,
                    help='Count of ticks on the graph', metavar='tickrate')
parser.add_argument('-m', '--method', default=2,
                    help='Select method for averaging. 1 — by period, 2 — ticks',
                    choices=['1', '2'])
parser.add_argument('-o', '--output', metavar='filename',
                    help='Filename for graph (jpg or png)')
parser.add_argument('-d', '--datafile', metavar='filename', default = 'data.txt',
                    help='Filename for specific datafile',)


args = parser.parse_args()

period = int(args.period) #period of ticks in seconds
ticks = int(args.ticks)
method = int(args.method) #method for averaging by period(1) or ticks(2), ticks works and looks better i think
show_graph = int(args.show_graph)
datafile = args.datafile
filename = args.output



if period < cooldown:
    raise ValueError('The period cannot be less than a cooldown')

with open(datafile, 'r') as f:
    data = f.read().replace('\'', '"')

splitted_data = data.split('\n')
try:
    splitted_data.remove('')
except:
    pass

clear_splitted_data = []

def filter_data():
    errors_count = 0
    for once in splitted_data:
        try:
            data = json.loads(once)
            if (('t' in data) and ('h' in data) and ('time' in data)) and (data['t'] != 'nan' and data['h'] != 'nan'):
                clear_splitted_data.append(data)
            else:
                raise
        except:
            errors_count += 1
    
    print('Invalid lines in data.txt:', errors_count)

start_filtering_time = datetime.now()
filter_data()
print('Time spent on filtering: ', datetime.now() - start_filtering_time)

lenght = len(clear_splitted_data)
thinned_data = []

###data averaging###
def averaging_by_period():
    summ_temp, summ_hum = 0, 0
    for i in range(0, lenght):
        data_i = clear_splitted_data[i]
        summ_temp += float(data_i['t'])
        summ_hum += float(data_i['h'])
        if (i % (period // cooldown) == 0 and i != 0):
            data_i.update({'t': float(summ_temp / (period // cooldown))})
            data_i.update({'h': float(summ_hum / (period // cooldown))})
            thinned_data.append(data_i)
            summ_temp, summ_hum = 0, 0
        elif i == 0:
            data_i.update({'t': float(summ_temp)})
            data_i.update({'h': float(summ_hum)})
            thinned_data.append(data_i)
            summ_temp, summ_hum = 0, 0
        elif (i == lenght - 1):
            data_i.update({'t': float(summ_temp / ((lenght - 1) % (period // cooldown)))})
            data_i.update({'h': float(summ_hum / ((lenght - 1) % (period // cooldown)))})
            thinned_data.append(data_i)

def averaging_by_ticks():
    ticks_step = math.floor(lenght / ticks)
    summ_temp_for_tick, summ_hum_for_tick = 0, 0
    for step in range((ticks - 1) * ticks_step):
        data_tick_step = clear_splitted_data[step]
        summ_temp_for_tick += float(data_tick_step['t']) 
        summ_hum_for_tick += float(data_tick_step['h']) 
        if step % ticks_step == ticks_step - 1:
            thinned_data.append({'t': summ_temp_for_tick / ticks_step,
                                'h': summ_hum_for_tick / ticks_step,
                                'time': data_tick_step['time']})
            summ_temp_for_tick, summ_hum_for_tick = 0, 0
    #for the last tick if ticks_step*ticks < lenght
    counter = 0
    for step in range((ticks - 1) * ticks_step, lenght):
        data_tick_step = clear_splitted_data[step]
        summ_temp_for_tick += float(data_tick_step['t']) 
        summ_hum_for_tick += float(data_tick_step['h']) 
        counter += 1
    thinned_data.append({'t': summ_temp_for_tick / counter,
                            'h': summ_hum_for_tick / counter,
                            'time': data_tick_step['time']})

###fail edition
#def averaging_by_ticks():
#    ticks_step = math.ceil(lenght / ticks)
#    #ticks_step = lenght // ticks
#    counter = 0
#    for tick in range(ticks):
#        summ_temp_for_tick, summ_hum_for_tick = 0, 0
#        if counter + ticks_step < lenght or lenght % ticks == 0:
#            for tick_step in range(ticks_step):
#                data_tick_step = json.loads(splitted_data[counter])
#                summ_temp_for_tick += float(data_tick_step['t']) 
#                summ_hum_for_tick += float(data_tick_step['h'])
#                counter += 1
#            print(counter)
#        elif counter >= lenght - lenght % ticks_step:
#            last_ticks_counter = 0
#            for tick_step in range(lenght - lenght % ticks_step, lenght):
#                data_tick_step = json.loads(splitted_data[tick_step])
#                summ_temp_for_tick += float(data_tick_step['t']) 
#                summ_hum_for_tick += float(data_tick_step['h'])
#                last_ticks_counter += 1
#            ticks_step = last_ticks_counter
#        thinned_data.append({'t': summ_temp_for_tick / ticks_step,
#                             'h': summ_hum_for_tick / ticks_step,
#                             'time': data_tick_step['time']})        

###legacy
#for i in range(len(splitted_data)):
#    if i % (period // cooldown) == 0:
#        thinned_data.append(splitted_data[i])

start_averaging_time = datetime.now()
if method == 1:
    averaging_by_period()
elif method == 2:
    averaging_by_ticks()
print('Time spent on averaging: ', datetime.now() - start_averaging_time)

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
plt.subplots_adjust(top=0.94,
                    bottom=0.295,
                    left=0.065,
                    right=0.985,
                    hspace=0.154,
                    wspace=0.205)

if filename != None:
    plt.savefig(filename)
if show_graph == 1:
    plt.show()
