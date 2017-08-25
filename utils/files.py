import json
import os


def open_json_file(path):
    path = os.path.abspath('') + path
    file = open(path, 'r')
    print('opened file in %s' %(path))
    danmu = json.loads(file.read())
    file.close()
    return danmu

def write_json_file(path, content):
    path = os.path.abspath('') + path
    file = open(path, 'w+')
    file.write(json.dumps(content))
    print('written into file in %s' % (path))
    file.close()