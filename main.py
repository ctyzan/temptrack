import requests, json, time

while True:
    str_data = requests.get('http://192.168.1.109/json', timeout=5).text
    data = json.loads(str_data)

    current_time = {'time': str(round(time.time(), 2))}
    data.update(current_time)

    with open('data.txt', mode='a') as f:
        f.write(str(data) + '\n')

    print(data)
    time.sleep(5)