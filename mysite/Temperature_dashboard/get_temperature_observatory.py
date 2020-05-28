import requests
import json

def get_json():
    full_json = requests.get('https://www.climadobrasil.com.br/api/v1/get_current_conditions_by_pelmorex_id/BRRO0042')
    full_json = json.loads(full_json.text)
    return full_json['temperature']['c'], full_json['timestamp']['utc']