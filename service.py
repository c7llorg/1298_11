from datetime import datetime
import client
from config import UPLOAD_FOLDER

def prepare_positions(positions):
    for i in range(len(positions)):
#        positions[i]['id'] = '-'.join(positions[i].get('id'))
        if not positions[i]['name']:
            positions[i]['name'] = '-'
    return positions

def get_positions():
    positions = client.get_warahouse().get('warehouse')
    if not positions:
        return []
    return prepare_positions(positions)

def checkout(n):
    positions = client.get_warahouse()
    position = positions.get('warehouse')[n - 1]['id']
    client.checkout(position)

def upload(data):
    file_name = f'{UPLOAD_FOLDER}/{datetime.now()}.xls'
    with open(file_name, 'wb') as fd:
        fd.write(data)
    if client.upload(file_name):
        return 'Успешно загружено'
    else:
        return 'Произошла ошибка при загрузке'

def get_remote():
    remote = client.get_remote().get('remote')
    if not remote:
        return []
    return remote

def get_checkout_list():
    checkout_list = client.get_checkout_list().get('checkout_list')
    if not checkout_list:
        return []
    return prepare_positions(checkout_list)


