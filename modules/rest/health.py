from flask import jsonify
import config

def health(request):
    config.LOGGER.info("GET /health")
    result = { 'result' : 'ok' , 'service' : 'plex rest'}
    return jsonify(result)