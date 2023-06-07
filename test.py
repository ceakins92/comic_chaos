import requests

def getit(name):
    resp = requests.get(f'https://metron.cloud/api/character/?name={name}')
    print(resp)


getit(deadpool)