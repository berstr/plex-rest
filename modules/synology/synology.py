import os
import requests

import config

def synology_share_path(path):
    dir = os.path.dirname(path)
    return dir[dir.find('/music'):]

def list_folder(foldername, filter=None, files_only=True):
    config.LOGGER.info("list_folder() - foldername: %s - filter: %s - files_only: %s" % (foldername, filter, files_only))
    f = synology_share_path(foldername)
    print("list_folder() - share name: ", f)
    result=[]
    PARAMS = {
        "path": f
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