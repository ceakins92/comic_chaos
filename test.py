import hashlib
from pendulum import time
import requests

def get_marvel_character(name):
    public_key = ''
    private_key = ''
    ts = str(time.time())
    hash = hashlib.md5()
    hash.update(ts.encode('utf-8'))
    hash.update(private_key.encode('utf-8'))
    hash.update(public_key.encode('utf-8'))
    params = {
        'apikey': public_key,
        'ts': ts,
        'hash': hash.hexdigest(),
        'name': name
    }
    response = requests.get('http://gateway.marvel.com/v1/public/characters', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
new_search = get_marvel_character()
print(new_search(deadpool))













