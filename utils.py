import json


def encode_to_json(data: dict):
    json_data = json.dumps(data)
    return bytes(json_data, 'utf-8')


def decode_json(data):
    return json.loads(data)
