
import json
import random


def shuffle():
    f = open('./utils/shuffle.json', 'r')
    json_content = f.read()
    j = json.loads(json_content)
    max_len = len(j['spinners']) - 1
    i = random.randint(0, max_len)
    return j['spinners'][i]
