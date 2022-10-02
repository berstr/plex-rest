from plexapi.myplex import MyPlexAccount
#import json
#import os
#import sys
#import re
#from flask import request , jsonify #Flask, jsonify, request
#import logging
#import time

#from modules.rest import health as rest_health
#from modules.rest import section as rest_section
#from modules.rest import album as rest_album
#from modules.rest import video as rest_video
#from modules.rest import genre as rest_genre
#from modules.rest import recently_added as rest_recently_added

from modules.plex import section as plex_section

from modules.scripts import analyse as scripts_analyse

import config

config.init()

def list_ids():
    print(f'----------------------------------------')
    print(f' List IDs')
    print(f'----------------------------------------')
    print('Select the Plex section:')
    section = select_section()
    if (section != None):
        print('')
        tracks = section.all(libtype='track')
        track_ids = []
        for track in tracks:
            track_ids.append(f'{track.ratingKey}/{track.title}')
        albums = section.all(libtype='album')
        album_ids = []
        for album in albums:
            album_ids.append(f'{album.ratingKey}/{album.title}')
        artists = section.all(libtype='artist')
        artist_ids = []
        for artist in artists:
            artist_ids.append(f'{artist.ratingKey}/{artist.title}')

        print(f'tracks:  {track_ids}')
        print(f'albums:  {album_ids}')
        print(f'artists: {artist_ids}')


def select_section():
    result = None
    sections = config.PLEX.library.sections()
    i=1
    for section in sections:
        print(F'{i} - {section.title}')
        i=i+1
    user = input('(enter: no selection) ==> ')
    if (user != ''):
        result = sections[int(user)-1]
    return result

def analyse_tracks():
    print('')
    print(f'----------------------------------------')
    print(f' Analyse Plex Section')
    print(f'----------------------------------------')
    print('')
    print('Select the Plex section:')
    section = select_section()
    if (section != None):
        print('')
        user = input(f'Prompt for user input if Album Year is empty: y/n  (default: n) ==> ')
        empty_year = False
        if (user == 'y'):
            empty_year = True
        print('')
        scripts_analyse.analyse(section, empty_year)

def scan_section():
    print('')
    print(f'----------------------------------------')
    print(f' Scan Plex Section')
    print(f'----------------------------------------')
    print('')
    print('Select the Plex section:')
    section = select_section()
    if (section != None):
        print('')
        print(f'Triggering scan of section: {section.title}  ..... ')
        section.update()
        print('')

def get_item_details():
    print('')
    print(f'----------------------------------------')
    print(f' Get Item Details')
    print(f'----------------------------------------')
    print('')
    print('Select the Plex section:')
    section = select_section()
    print('')
    if (section != None):
        while (True):
            print('')
            key = input('Item key (e to exit menue ) -> ')
            if (key == 'e'):
                return
            if (key != ''):
                item = section.fetchItem("/library/metadata/{0}".format(key))
                if (item != None):
                    print(f'Class: {item}')
                    print(f'Title: {item.title}')


menues = ['Analyse Tracks','Item Details','List IDs','Scan Section']

while (True):
    print('')
    print('===========================')
    print(' MAIN MENUE - PLEX UTILITY')
    print('===========================')
    print('')
    i=1
    for menue in menues:
        print(f'{i} -> {menue}')
        i=i+1
    print('q  ->  quit program')
    print('')
    user = input('==> ')
    print('')

    if (user == '1'):
        analyse_tracks()
    elif (user == '2'):
        get_item_details()
    elif (user == '3'):
        list_ids()
    elif (user == '4'):
        scan_section()
    elif (user == 'q'):
        quit()




'''
#item_key = "43526"
#item = plex_section.fetchItem("/library/metadata/{0}".format(item_key))

#print(item)
#print(item.title)
#print(item.key)

def list_items(section,item_type):
    items = section.all(libtype=item_type)
    i=1
    for item in items:
        if (item_type == 'artist'):
            parent_id = '              '
        elif (item_type == 'album'):
            parent_id = f'(artist) {item.parentRatingKey}'
        elif (item_type == 'track'):
            parent_id = f'(album) {item.parentRatingKey}'
        print(f'[{i:02} : {item_type:6}] - id: {item.ratingKey:6} - parent id: {parent_id:14} - title: {item.title:30} - type: {type(item)}')
        i = i+1



list_items(plex_section, 'track')
list_items(plex_section, 'album')
list_items(plex_section, 'artist')

print('')
# config.LOGGER.info("trigger library scan ... ")
# plex_section.update()
# time.sleep(3)
# input('To start scanning the tracks, hit enter ...')

scan_tracks.analyse_metadata(plex_section)

quit()


track_key = "43406"
track = plex_section.fetchItem("/library/metadata/{0}".format(track_key))

print(track.title)
print(track.key)

track_key = "29659"
track = plex_section.fetchItem("/library/metadata/{0}".format(track_key))

print(track.title)
print(track.key)






track_key = "37172"

track = plex_section.fetchItem("/library/metadata/{0}".format(track_key))
config.LOGGER.info("item: %s" % (track))
config.LOGGER.info("track: %s  -  artist: %s - grandparentTitle: %s - parentRatingKey: %s - grandparentRatingKey: %s - key: %s - ratingKey: %s - key: %s" % (track.title,track.originalTitle,track.grandparentTitle,track.parentRatingKey,track.grandparentRatingKey,track.key,track.ratingKey,track.key))
album = track.album()
originallyAvailableAt = album.originallyAvailableAt
config.LOGGER.info("album: %s  -  artist: %s - parentRatingKey: %s - originallyAvailableAt: %s" % (album.title,album.parentTitle,album.parentRatingKey,album.originallyAvailableAt))
config.LOGGER.info(f"album tracks: {album.tracks()}")


# albums = plex_section.albums()








tracks = []
albums = plex_section.albums()
i=1
for album in albums:
    config.LOGGER.info("[{0}] album: {1}".format(1,album.title)
        i=i+1
        tracks = album.tracks()
        t=1
        for track in tracks:
            config.LOGGER.info("       [%d -%s] track: %s  -  artist: %s - track.grandparentTitle: %s - parentRatingKey: %s - grandparentRatingKey: %s - key: %s - ratingKey: %s - key: %s" % (i,t,track.title,track.originalTitle,track.grandparentTitle,track.parentRatingKey,track.grandparentRatingKey,track.key,track.ratingKey,track.key))
            t = t+1


track_key = "37172"

track = plex_section.fetchItem("/library/metadata/{0}".format(track_key))
config.LOGGER.info("item: %s" % (track))
config.LOGGER.info("track: %s  -  artist: %s - grandparentTitle: %s - parentRatingKey: %s - grandparentRatingKey: %s - key: %s - ratingKey: %s - key: %s" % (track.title,track.originalTitle,track.grandparentTitle,track.parentRatingKey,track.grandparentRatingKey,track.key,track.ratingKey,track.key))
album = track.album()
originallyAvailableAt = album.originallyAvailableAt
config.LOGGER.info("album: %s  -  artist: %s - parentRatingKey: %s - originallyAvailableAt: %s" % (album.title,album.parentTitle,album.parentRatingKey,album.originallyAvailableAt))
#config.LOGGER.info("%s" % (album.originallyAvailableAt.strftime("%Y")))
#x = '{price}-01-01 00:00:00'.format(price=album.originallyAvailableAt.strftime("%Y"))
#config.LOGGER.info("%s" % (x))


new_album_from_track(track)

config.LOGGER.info("AFTER CHANGE")

track1 = plex_section.fetchItem("/library/metadata/{0}".format(track_key))
config.LOGGER.info("item: %s" % (track1))
config.LOGGER.info("track: %s  -  artist: %s - grandparentTitle: %s - parentRatingKey: %s - grandparentRatingKey: %s - key: %s - ratingKey: %s - key: %s" % (track.title,track.originalTitle,track.grandparentTitle,track.parentRatingKey,track.grandparentRatingKey,track.key,track.ratingKey,track.key))
album = track1.album()
set_album_date(album, originallyAvailableAt)
config.LOGGER.info("album: %s  -  artist: %s - parentRatingKey: %s - originallyAvailableAt: %s" % (album.title,album.parentTitle,album.parentRatingKey,album.originallyAvailableAt))


quit()


list_album(plex_section)

albums = plex_section.albums()
a=1
t=1
for album in albums:
    tracks = album.tracks()
    for track in tracks:
        if (track.title == album.title):
            config.LOGGER.info("[%d] - FALSE - change album for track: %s  -  album: %s - track artist: %s - album artist: %s" % (a,track.title,album.title, track.originalTitle,album.parentTitle))
        else: 
            config.LOGGER.info("[%d] - TRUE  - change album for track: %s  -  album: %s - track artist: %s - album artist: %s" % (a,track.title,album.title, track.originalTitle,album.parentTitle))
            #set_album(album,track.ratingKey,track.title)
            #set_album(track,track.ratingKey,track.title)
            if (t==3):
                quit
            t=t+1

        a=a+1

config.LOGGER.info("after updating section and tracks")

#list_album(plex_section)

'''

