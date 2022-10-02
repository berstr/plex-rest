from plexapi.myplex import MyPlexAccount
import json
import os
import sys
from flask import request , jsonify #Flask, jsonify, request
import logging

from modules.rest import health as rest_health
from modules.rest import section as rest_section
from modules.rest import album as rest_album
from modules.rest import video as rest_video
from modules.rest import genre as rest_genre
from modules.rest import recently_added as rest_recently_added
from modules.plex import section as plex_section

import config

config.init()

plex_section.init('Music Carolin')

config.LOGGER.info("STARTUP SERVICE")

config.LOGGER.info("SYNOLOGY_FILESTATION_SERVICE: %s" % (config.SYNOLOGY_FILESTATION_SERVICE))


@config.APP.route('/health')
def health():
    return rest_health.health(request)

@config.APP.route('/section/uuid')
def section_uuid():
    uuid = request.args.get('uuid')
    config.LOGGER.info("GET /section/uuid - uuid: %s" % (uuid))
    result = rest_section.get_by_uuid(uuid)
    config.LOGGER.info("GET /section/uuid - result: %s" % (result['result']))
    return jsonify(result)

@config.APP.route('/section/name')
def section_name():
    name = request.args.get('name')
    config.LOGGER.info("GET /section/name - name: %s" % (name))
    result = rest_section.get_by_name(name)
    config.LOGGER.info("GET /section/name - result: %s" % (result['result']))
    return jsonify(result)    

@config.APP.route('/sections')
def sections():
    config.LOGGER.info("GET /sections")
    result = rest_section.names()
    config.LOGGER.info("GET /sections - result: %s" % (result['result']))
    return jsonify(result)    

@config.APP.route('/items')
def items():
    section_name = request.args.get('section_name')
    details = request.args.get('details')
    config.LOGGER.info("GET /items - section_name: %s - details: %s" % (section_name, details))
    result = rest_section.items(section_name, details)
    config.LOGGER.info("GET /items - result: %s" % (result['result']))
    return jsonify(result)    

@config.APP.route('/item')
def item():
    section_name = request.args.get('section_name')
    key = request.args.get('key')
    config.LOGGER.info("GET /item - section_name: %s - key: %s" % (section_name, key))
    result = rest_section.item(section_name, key)
    config.LOGGER.info("GET /item - result: %s" % (result['result']))
    return jsonify(result)    

@config.APP.route('/scan')
def scan():
    section_name = request.args.get('section_name')
    config.LOGGER.info("GET /scan - section_name: %s" % (section_name))
    result = rest_section.scan(section_name)
    config.LOGGER.info("GET /scan - result: %s" % (result['result']))
    return jsonify(result)    

@config.APP.route('/recently_added')
def recently_added():
    name = request.args.get('section_name')
    limit = request.args.get('limit')
    details = request.args.get('details')
    config.LOGGER.info("GET /recently_added - section_name: %s - details: %s - limit: %s" % (name, details,limit))
    result = rest_recently_added.get(name, details, limit)
    config.LOGGER.info("GET /recently_added - result: %s" % (result['result']))
    return jsonify(result)


@config.APP.route('/genres')
def genres():
    section_name = request.args.get('section')
    config.LOGGER.info("GET /genres - section: %s" % (section_name))
    result = rest_genre.genres(section_name)
    config.LOGGER.info("GET /genres - result: %s" % (result['result']))
    return jsonify(result)

@config.APP.route('/genres/add', methods=['PUT'])
def genres_add():
    try:
        body = request.get_json()
        section_name = body.get('section')
        item_key = body.get('key')
        genres = body.get('genres')
        config.LOGGER.info("PUT /genres/add - section_name: %s - item_key: %s - genres: %s" % (section_name, item_key, genres))
        section_type = rest_section.section_type(section_name)
        if section_type['result'] == 'ok':
            if section_type['type'] == 'MusicSection':
                result = rest_album.genres_add(section_name, item_key, genres)
            elif section_type['type'] == 'MovieSection':
                result = rest_video.genres_add(section_name, item_key, genres)
            else:
                result = {'result':'library section type [%s] not supported' % (section_type)}
        else:
            result = section_type
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'key':item_key, 'genres': genres }
        config.LOGGER.exception(result)
    config.LOGGER.info("PUT /genres/add - result: %s" % (result['result']))
    return jsonify(result)

@config.APP.route('/genres/replace', methods=['PUT'])
def genres_replace():
    try:
        body = request.get_json()
        section_name = body.get('section')
        item_key = body.get('key')
        genres = body.get('genres')
        config.LOGGER.info("PUT /genres/replace - section_name: %s - item_key: %s - genres: %s" % (section_name, item_key, genres))
        section_type = rest_section.section_type(section_name)
        if section_type['result'] == 'ok':
            if section_type['type'] == 'MusicSection':
                result = rest_album.genres_replace(section_name, item_key, genres)
            elif section_type['type'] == 'MovieSection':
                result = rest_video.genres_replace(section_name, item_key, genres)
            else:
                result = {'result':'library section type [%s] not supported' % (section_type)}
        else:
            result = section_type
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'key':item_key, 'genres': genres }
        config.LOGGER.exception(result)
    config.LOGGER.info("PUT /genres/replace - result: %s" % (result['result']))
    return jsonify(result)

@config.APP.route('/genres/delete', methods=['PUT'])
def genres_delete():
    try:
        body = request.get_json()
        section_name = body.get('section')
        item_key = body.get('key')
        config.LOGGER.info("PUT /genres/delete - section_name: %s - item_key: %s" % (section_name, item_key))
        section_type = rest_section.section_type(section_name)
        if section_type['result'] == 'ok':
            if section_type['type'] == 'MusicSection':
                result = rest_album.genres_delete(section_name, item_key)
            elif section_type['type'] == 'MovieSection':
                result = rest_video.genres_delete(section_name, item_key)
            else:
                result = {'result':'library section type [%s] not supported' % (section_type)}
        else:
            result = section_type
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'key':item_key }
        config.LOGGER.exception(result)
    config.LOGGER.info("PUT /genres/delete - result: %s" % (result['result']))
    return jsonify(result)


@config.APP.route('/search/artist', methods=['GET'])
def search_artist():
    try:
        body = request.get_json()
        section_name = body.get('section')
        artist_name = body.get('name')
        config.LOGGER.info("GET /search/artist - section_name: %s - name: %s" % (section_name, artist_name ))
        result = rest_search.artist(section_name, artist_name)
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'artist_name':artist_name }
        config.LOGGER.exception(result)
    config.LOGGER.info("ET /search/artist - result: %s" % (result['result']))
    return jsonify(result)


# updates the title, sort and original title of music albums and videos
@config.APP.route('/title', methods=['PUT'])
def set_title():
    try:
        body = request.get_json()
        section_name = body.get('section')
        item_key = body.get('key')
        title = body.get('title')
        config.LOGGER.info("PUT /title - section_name: %s - item_key: %s - title: %s" % (section_name, item_key, title))
        section_type = rest_section.section_type(section_name)
        if section_type['result'] == 'ok':
            if section_type['type'] == 'MusicSection':
                result = rest_album.set_title(section_name, item_key, title)
            elif section_type['type'] == 'MovieSection':
                result = rest_video.set_title(section_name, item_key, title)
            else:
                result = {'result':'library section type [%s] not supported' % (section_type)}
        else:
            result = section_type
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'key':item_key, 'title': title }
        config.LOGGER.exception(result)
    
    config.LOGGER.info("PUT /title - result: %s" % (result['result']))
    return jsonify(result)


# updates the artist of music albums and videos
@config.APP.route('/artist', methods=['PUT'])
def set_artist():
    try:
        body = request.get_json()
        section_name = body.get('section')
        item_key = body.get('key')
        artist = body.get('artist')
        config.LOGGER.info("PUT /artist - section_name: %s - item_key: %s - title: %s" % (section_name, item_key, artist))
        section_type = rest_section.section_type(section_name)
        if section_type['result'] == 'ok':
            if section_type['type'] == 'MusicSection':
                result = rest_album.set_artist(section_name, item_key, artist)
            elif section_type['type'] == 'MovieSection':
                result = rest_video.set_artist(section_name, item_key, artist)
            else:
                result = {'result':'library section type [%s] not supported' % (section_type)}
        else:
            result = section_type
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'key':item_key, 'title': title }
        config.LOGGER.exception(result)
    config.LOGGER.info("PUT /title - result: %s" % (result['result']))
    return jsonify(result)


# updates the artist of music albums and videos
@config.APP.route('/date', methods=['PUT'])
def set_date():
    try:
        body = request.get_json()
        section_name = body.get('section')
        item_key = body.get('key')
        new_date = body.get('date')
        config.LOGGER.info("PUT /date - section_name: %s - item_key: %s - date: %s" % (section_name, item_key, new_date))
        section_type = rest_section.section_type(section_name)
        if section_type['result'] == 'ok':
            if section_type['type'] == 'MusicSection':
                result = rest_album.set_date(section_name, item_key, new_date)
            elif section_type['type'] == 'MovieSection':
                result = rest_video.set_date(section_name, item_key, new_date)
            else:
                result = {'result':'library section type [%s] not supported' % (section_type)}
        else:
            result = section_type
    except: # catch *all* exceptions
        exception_type = str(sys.exc_info()[0])
        exception_value = str(sys.exc_info()[1])
        result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value, 'section_name': section_name, 'key':item_key, 'date': new_date }
        config.LOGGER.exception(result)
    config.LOGGER.info("PUT /date - result: %s" % (result['result']))
    return jsonify(result)
 


if __name__ == "__main__":
    from waitress import serve
    config.LOGGER.info("STARTUP waitress server on port %s ..." % (config.PLEX_REST_PORT))
    serve(config.APP, host="0.0.0.0", port=config.PLEX_REST_PORT)

