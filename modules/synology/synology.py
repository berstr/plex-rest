import os
import requests

import config

def synology_share_path(path):
    dir = os.path.dirname(path)
    return dir[dir.find('/music'):]


def get_folder_items(folder_id):
    result = None
    items = []
    PARAMS = {
        "id": folder_id
    }
    URL = 'http://' + config.SYNOLOGY_PHOTO_SERVICE + '/folder/items'
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200 and r.status_code != 500:
        result = {'result' : "HTTP error - GET /folder/items: folder_id: {}) - status code: {}".format(folder_id,r.status_code)}
    elif r.status_code == 500:
        result = {'result':'ok','items':[]}
    else:
        json_result = r.json()
        if json_result["result"] == 'ok':
            result = {'result':'ok','items':json_result['items']}
        else:
            result = {'result':'synology photos error','synology':json_result}
    return result


def list_folder(foldername, filter=None, files_only=True):
    #config.LOGGER.info("list_folder() - foldername: %s - filter: %s - files_only: %s" % (foldername, filter, files_only))
    result=[]
    PARAMS = {
        "path": foldername
    }
    URL = 'http://' + config.SYNOLOGY_FILESTATION_SERVICE + '/folder/list'
    r = requests.get(url=URL, params=PARAMS)
    if (r.status_code == 200):
        data = r.json()
        if (data["result"] == 'ok'):    
            for file in data['synology']['data']['files']:
                tmp = None
                if (files_only==True):
                    if (file["isdir"] == False):
                        tmp = file
                else:
                    tmp = file
                if (tmp != None):
                    if (filter != None):
                        if (tmp["name"].find(filter) != -1):
                            result.append(tmp["name"])
                    else:
                            result.append(tmp["name"])
        else:
            config.LOGGER.error("ERROR: synology-filestation /folder/list - response code: {}".format(data["result"]))
    else:
        config.LOGGER.error("ERROR: synology-filestation service - response code: {}".format(r.status_code))
        
    return result