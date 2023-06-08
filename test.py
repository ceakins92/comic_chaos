import hashlib
from pendulum import time
import requests

def get_marvel_character(name):
    public_key = '105d96a57df71042ffdfc572b7195cf5'
    private_key = 'e917c38970ddb27117e675af6518098d573d06c4'
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













