import requests
from config import CLIENT_CONFIG

URL = f'http://{CLIENT_CONFIG.get("host")}:{CLIENT_CONFIG.get("port")}/{CLIENT_CONFIG.get("base_url")}'

def get_warahouse():
    try:
        r = requests.get(URL + '/warehouse')
        return r.json()
    except requests.exceptions.ConnectionError:
        return {'warehouse': []}

def checkout(position):
    r = requests.get(URL + '/checkout', params={'destination': position})

def upload(file_name):
    with open(file_name, 'rb') as fd:
        data = fd.read()
    try:
        r = requests.post(URL + '/upload', data=data)
        return True
    except requests.exceptions.ConnectionError:
        return False

def get_remote():
    try:
        r = requests.get(URL + '/remote')
        return r.json()
    except requests.exceptions.ConnectionError:
        return {'remote': []}

def get_checkout_list():
    try:
        r = requests.get(URL + '/checkout_list')
        return r.json()
    except requests.exceptions.ConnectionError:
        return {'checkout_list': []}

if __name__ == '__main__':
    print(get_warahouse())
