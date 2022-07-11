import requests, json, time

url = 'http://192.168.1.109/json'
cooldown = 5


if __name__ == '__main__':
    while True:
        str_data = requests.get(url, timeout=10).text
        data = json.loads(str_data)
        if data['t'] != 'nan' and data['h'] != 'nan':
            current_time = {'time': str(round(time.time(), 2))}
            data.update(current_time)

            with open('data.txt', mode='a') as f:
                f.write(str(data) + '\n')

            print(data)
        time.sleep(cooldown)