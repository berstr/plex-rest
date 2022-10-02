from plexapi.myplex import MyPlexAccount
#import json
import os
#import sys
#import re
#from flask import request , jsonify #Flask, jsonify, request
#import logging
import requests

#from modules.rest import health as rest_health
#from modules.rest import section as rest_section
#from modules.rest import album as rest_album
#from modules.rest import video as rest_video
#from modules.rest import genre as rest_genre
#from modules.rest import recently_added as rest_recently_added
from modules.plex import section as plex_section
from modules.synology import synology
import config

SECTION = None

def list_section():
    albums = SECTION.fetchItems('album')
    for album in albums:
        tracks = album.tracks()
        for track in tracks:
            print(f'album.title:       {get_album_title(album)}') 
            print(f'album.title.sort:  {get_album_title_sort(album)}') 
            print(f'album.artist:      {get_album_artist_name(album)}')
            print(f'album.year:        {get_album_originallyAvailableAt(album)}')
            print(f'track.title:       {get_track_title(track)}')
            print(f'track.album:       {get_track_album_title(track)}')
            print(f'track.artist:      {get_track_artist_name(track)}')
            print(f'track.album.artist:{get_track_album_artist_name(track)}')
            print(f'artist.sort:       {get_album_artist_name_sort(album)}')
            print(f'filename:          {get_track_file_basename(track)}')
            print(f'path:              {get_track_file_path(track)}')
            print(f'album.id:          {get_album_id(album)}')
            print(f'track.id:          {get_track_id(track)}')
            print(f'album.artist.id:   {get_album_artist_id(album)}')
            print(f'track.artist.id:   {get_track_artist_id(track)}')
            print('----------------------------')

def list_ids():
    tracks = SECTION.all(libtype='track')
    track_ids = []
    for track in tracks:
        track_ids.append(f'{track.ratingKey}/{track.title}')
    albums = SECTION.all(libtype='album')
    album_ids = []
    for album in albums:
        album_ids.append(f'{album.ratingKey}/{album.title}')
    artists = SECTION.all(libtype='artist')
    artist_ids = []
    for artist in artists:
        artist_ids.append(f'{artist.ratingKey}/{artist.title}')

    print(f'tracks:  {track_ids}')
    print(f'albums:  {album_ids}')
    print(f'artists: {artist_ids}')



def synology_list_folder(foldername):
    # path starts with /volume1/music/... , but synology filestation starts with /music/...
    music_share_path = foldername[foldername.index("/",1):]
    #config.LOGGER.info(f"list folder items - folder: {foldername} - share: {music_share_path}")
    res = synology.list_folder(music_share_path)
    #config.LOGGER.info(f"list folder items - res: {res}")
    return res
    

def synology_rename_file(path, new_name):
    # path starts with /volume1/music/... , but synology filestation starts with /music/...
    music_share_path = path[path.index("/",1):]
    result = None
    PARAMS = {
        "path": music_share_path,
        "name": new_name
    }
    URL = 'http://' + config.SYNOLOGY_FILESTATION_SERVICE + '/file/rename'
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200 and r.status_code != 500:
        result = {'result' : "HTTP error - modules.synology.list_files() - path: {} - status code: {}".format(music_share_path,r.status_code)}
    elif r.status_code == 500:
        result = {'result':'ok','files':[]}
    else:
        json_result = r.json()
        if json_result["result"] == 'ok':
            result = {'result':'ok'}
        else:
            result = {'result':'synology photos error','synology':json_result}
    if (result['result'] != 'ok'):
        #print(str(result["synology"]["synology"]["error"]))
        if (str(result["synology"]["synology"]["error"]).find("'code': 414") != -1):
            config.LOGGER.info(f"INFO - file already exists: {new_name}")
            result = {'result':'ok'}
        else:
            config.LOGGER.info(f"ERROR - file rename: {result['result']}")
            config.LOGGER.info(f"        {result}")
    return result




def is_album_in_track_filename(album,track):
    ##file_info = get_track_file_info(track)
    # 1st: the album title and filename are converted into lower case
    # 2nd: often the album title contains something like: Tearin’ Up ... and the filename contains:  Tearin' Up
    # but ’ in album titles (unicode char with code 8217) and ' in filenames (unicode char with code 39) are different - so ’ (unicode 8217) is replaced with ' (uncode 39)
    compare_album_title = album.title.lower().strip().replace(chr(8217),chr(39))
    compare_filename = get_track_file_name(track).lower().strip().replace(chr(8217),chr(39))
    index = compare_filename.find(compare_album_title)
    if (index == -1):
        print(f'DIFFERENCE   album.title  [ {compare_album_title:>60} ]   <NOT WITHIN>   track.filename: [ {compare_filename} ]')
        return False
    else:
        return True

def __none_to_string(obj):
    if (obj == None):
        return ''
    return obj

#####################
### PLEX TRACK
#####################

def get_track_title(track):
    return  __none_to_string(track.title)

def get_track_id(track):
    return  __none_to_string(track.ratingKey)

def get_track_artist(track):
    return track.artist()

def get_track_artist_name(track):
    return __none_to_string(track.originalTitle)

def get_track_album_title(track):
    return __none_to_string(track.parentTitle)

def set_track_album_title(track,new_title):
    query = {'type':10,'id':track.ratingKey,'album.title.value':new_title,'artist.id.value':track.album().artist().ratingKey,'includeExternalMedia':1}
    print(f'set_album_title - {query}')
    track.edit(**query)
    track.reload()


def get_track_album_artist_name(track):
    return __none_to_string(track.grandparentTitle)

def get_track_artist_name_sort(track):
    try:
        artist = track.artist()
        if (artist==None):
            result = ''
        else:
            result = __none_to_string(artist.titleSort)
    except:
        result = ''
    return result

def get_track_album(track):
    return track.album()

def get_track_artist_id(track):
    return __none_to_string(track.grandparentRatingKey)

def get_track_year(track):
    return __none_to_string(track.year)

def set_track_title(track,new_title):
    query = {'type':10,'id':track.ratingKey,'title.value':new_title,'title.locked':1,'originalTitle.locked':1,'includeExternalMedia':1}
    #print(f'set_track_title - {query}')
    track.edit(**query)
    track.reload()
    

def set_track_album_artist_name(track,new_artist):
    # track album artist
    query = {'type':10,'id':track.ratingKey,'album.id.value':track.album().ratingKey,'artist.title.value':new_artist,'includeExternalMedia':1}
    print(f'set_track_album_artist_name - {query}')
    track.edit(**query)
    track.reload()

def set_track_artist_name(track,new_artist):
    query = {'type':10,'id':track.ratingKey,'originalTitle.value':new_artist,'originalTitle.locked':1,'includeExternalMedia':1}
    #print(f'set_track_artist - {query}')
    track.edit(**query)
    track.reload()


def set_artist_sort(artist,artist_name_sort):
    query = {'type':8,'id':artist.ratingKey,'titleSort.value':artist_name_sort,'titleSort.locked':1,'includeExternalMedia':1}
    artist.edit(**query)
    artist.reload()

#####################
### PLEX ALBUM
#####################

def get_album_title(album):
    return __none_to_string(album.title)

def get_album_title_sort(album):
    return __none_to_string(album.titleSort)

def get_album_id(album):
    return __none_to_string(album.ratingKey)

def get_album_artist_name(album):
    return __none_to_string(album.parentTitle)

def get_album_artist_id(album):
    return __none_to_string(album.parentRatingKey)

def get_album_artist_name_sort(album):
    try:
        artist = album.artist()
        if (artist==None):
            result = ''
        else:
            result = __none_to_string(artist.titleSort)
    except:
        result = ''
    return result

def get_album_originallyAvailableAt(album):
    result = ''
    try: 
        originallyAvailableAt = album.originallyAvailableAt
        print(f'originallyAvailableAt: {originallyAvailableAt}')
        if (originallyAvailableAt == None):
            result = ''
        else:
            result = originallyAvailableAt.strftime("%Y")
    except:
        print(f'originallyAvailableAt: Exception')
        result = ''
    return result


def set_album_title(album,new_title):
    query = {'type':9,'id':album.ratingKey,'title.value':new_title,'titleSort.value':new_title,'artist.id.value':album.artist().ratingKey,'title.locked':1,'titleSort.locked':1,'includeExternalMedia':1}
    print(f'set_album_title - {query}')
    album.edit(**query)
    album.reload()

def set_album_artist(album,new_artist):
    query = {'type':9,'id':album.ratingKey,'artist.title.value':new_artist,'title.value':album.title,'includeExternalMedia':1}
    print(f'set_album_artist - {query}')
    album.edit(**query)
    album.reload()


def set_album_date(album,year):
    if (year == ''):
        originallyAvailableAt = ''
    else: 
        originallyAvailableAt = f'{year}-01-01'
    query = {'type':9,'id':album.ratingKey,'originallyAvailableAt.value': originallyAvailableAt,'title.locked':1,'originallyAvailableAt.locked':1,'includeExternalMedia':1}
    print(f'set_album_date - {query}')
    album.edit(**query)
    album.reload()



def set_album_title_sort(album,album_title_sort):
    query = {'type':9,'id':album.ratingKey,'titleSort.value':album_title_sort,'titleSort.locked':1,'includeExternalMedia':1}
    #print(f'set_album_title_sort - {query}')
    album.edit(**query)
    album.reload()

#####################
### PLEX ARTIST
#####################

def get_artist_title(artist_obj):
    return artist_obj.title

def set_artist_title(artist_obj,new_artist):
    query = {'type':8,'id':artist_obj.ratingKey,'title.value':new_artist,'titleSort.value':new_artist,'title.locked':1,'titleSort.locked':1,'includeExternalMedia':1}
    print(f'set_artist_title - {query}')
    artist_obj.edit(**query)
    artist_obj.reload()


#####################
### PLEX TRACK FILE
#####################

def __get_track_part_filepath(track):
    return track.media[0].parts[0].file # only looking at the first part file of the first track media - as most or all tracks should have 1 media and within, 1 part object

def get_track_file_path(track):
    return __get_track_part_filepath(track)

def get_track_file_dirname(track):
    return os.path.dirname(__get_track_part_filepath(track))

def get_track_file_basename(track):
    return os.path.basename(__get_track_part_filepath(track))

def get_track_file_name(track):
    filename_ext = os.path.splitext(os.path.basename(__get_track_part_filepath(track)))
    return filename_ext[0]

def get_track_file_ext(track):
    filename_ext = os.path.splitext(os.path.basename(__get_track_part_filepath(track)))
    return filename_ext[1]

def build_new_filename(album, track, new_artist, new_title):
    originallyAvailableAt = get_album_originallyAvailableAt(album)
    if (originallyAvailableAt != ''):
        year = f' - ({originallyAvailableAt})'
    else:
        year = ""
    return f'{new_artist.strip()} - {new_title.replace(":",",").strip()}{year}{get_track_file_ext(track)}'

def build_new_filename2(artist,title,year,ext):
    if (year != ''):
        year = f' - ({year})'
    return f'{artist.strip()} - {title.replace(":",",").strip()}{year}{ext}'



##################################################


# checks if album and track title are the same, and if the album title is contained in the filename
def compare_album_track_file(album,track,empty_year):
    result = True
    ##album_title = album.title
    #if (album_title != None):
    #    album_title = album_title
    ##album_title_sort = album.titleSort
    #if (album_title_sort != None):
    #    album_title_sort = album_title_sort

    ##track_title = track.title
    #if (track_title != None):
    #    track_title = track_title.lower()
    ##track_album_title = track.parentTitle
    #if (track_album_title != None):
    #    track_album_title = track_album_title.lower()

    ##track_artist = track.originalTitle
    #if (track_artist != None):
    #    track_artist = track_artist.lower()
    ##album_artist_name = get_album_artist_name(album) # = album.parentTitle

    ##if (track.artist() != None):
    ##    artist_title = track.artist().title 
    ##    artist_title_sort = track.artist().titleSort
    
    ##track_album_artist = track.grandparentTitle
    #if (track_album_artist != None):
    #    track_album_artist = track_album_artist.lower()

    if (get_album_title(album) != get_track_title(track)): 
        print(f'DIFFERENCE   album.title: [ {get_album_title(album):>60} ]  !=  track.title: [ {get_track_title(track)} ]')
        #print(f'DIFFERENCE   album.title: [ {album_title:>60} ]  !=  track.title: [ {track_title} ]')
        result = False
    if (get_album_title(album) != get_album_title_sort(album)): 
        print(f'DIFFERENCE   album.title: [ {get_album_title(album):>60} ]  !=  album.title.sort: [ {get_album_title_sort(album)} ]')
        # print(f'DIFFERENCE   album.title: [ {album_title:>60} ]  !=  album.title.sort: [ {album_title_sort} ]')
        result = False
    if (get_album_title(album) != get_track_album_title(track)): 
        print(f'DIFFERENCE   album.title: [ {get_album_title(album):>60} ]  !=  track.album.title: [ {get_track_album_title(track)} ]')
        #print(f'DIFFERENCE   album.title: [ {album_title:>60} ]  !=  track.album.title: [ {track_album_title} ]')
        result =  False
    if (get_album_artist_name(album) != get_album_artist_name_sort(album)):
        print(f'DIFFERENCE  album.artist.name [ {get_album_artist_name(album):>60} ]  !=  album.artist.name.sort: [ {get_album_artist_name_sort(album)} ]')
        #print(f'DIFFERENCE  artist.title [ {artist_title:>60} ]  !=  artist.title.sort: [ {artist_title_sort} ]')
        result =  False
    if (get_track_artist_name(track) != get_album_artist_name(album)):
        print(f'DIFFERENCE  track.artist [ {get_track_artist_name(track):>60} ]  !=  album.artist: [ {get_album_artist_name(album)} ]')
        #print(f'DIFFERENCE  album.artist [ {album_artist_name:>60} ]  !=  track.artist: [ {track_artist} ]')
        result =  False
    if (get_track_artist_name(track) != get_track_album_artist_name(track)):
        print(f'DIFFERENCE   track.artist: [ {get_track_artist_name(track):>60} ]  !=  track.album.artist: [ {get_track_album_artist_name(track)} ]')
        result =  False

    if (empty_year == True):
        year = get_album_originallyAvailableAt(album)
        if (year == ''):
            print(f'DIFFERENCE   [ album.year not set ]')
            result =  False

    if (is_album_in_track_filename(album,track) == False):
        result = False
    
    return result





def sanatize(text):
    if (text != None):
        return text.replace(":",",").replace("/",";").strip()
    else:
        return ''

def get_new_metadata_from_user(track,album):
    result = None
    print('')
    print(f'Set the new values for title, artist and year.')
    print(f'Enter  "e"   at any time to exit this menue and start again for this track.')
    print(f'Artist:')
    print(f'      1  (album)  ->  {sanatize(get_album_artist_name(album))}')
    print(f'      2  (track)  ->  {sanatize(get_track_artist_name(track))}')
    print(f'      <Enter>     ->  user defined')
    user = input('==> ')
    if (user == 'e'):
        return False
    elif (user == '1'):
        artist = sanatize(get_album_artist_name(album))
    elif (user =='2'):
        artist = sanatize(get_track_artist_name(track))
    else:
        artist = input(f'Artist: ')

    print(f'Title:')
    print(f'      1  (album)       ->  {sanatize(get_album_title(album))}')
    print(f'      2  (track)       ->  {sanatize(get_track_title(track))}')
    print(f'      3  (track.album) ->  {sanatize(get_track_album_title(album))}')
    print(f'      <Enter>     ->  user defined')
    user = input('==> ')
    if (user == 'e'):
        return False
    elif (user == '1'):
        title = sanatize(get_album_title(album))
    elif (user =='2'):
        title = sanatize(get_track_title(track))
    elif (user =='3'):
        title = sanatize(get_track_album_title(album))
    else:
        title = input(f'Title: ')

    current_year = get_album_originallyAvailableAt(album)
    if (current_year != ''):
        #current_year = current_year.strftime("%Y")
        print(f'Year:')
        print(f'      1  (album)  ->  {current_year}')
        print(f'      <Enter>     ->  user defined')
        user = input('==> ')
        if (user == 'e'):
            return False
        elif (user == '1'):
            year = current_year
        else:
            year = input(f'Year: ')
    else:
        print(f'Year:')
        year = input(f'      enter new year, or leve it blank  -> ')

    return {'artist':artist,'title':title,'year':year}



def change_metadata(track,album,title,artist,year):
    result = None
    title = sanatize(title)
    artist = sanatize(artist)
    #file_info = get_track_file_info(track)
    new_filename = build_new_filename2(artist,title,year,get_track_file_ext(track))
    print('')
    print(f'New settings:')            
    print(f'  artist:     {artist}') 
    print(f'  title:      {title}')
    print(f'  year:       {year}')
    print(f'  filename:   {new_filename}')
    user = input('Change to new settings y/n -> ')
    if (user == 'y'):
        print('')
        print(f"CHANGE  filename:           {get_track_file_basename(track):>60}   =>   {new_filename}  -  [{get_track_file_path(track)}])")
        rename_result = synology_rename_file(get_track_file_path(track), new_filename)
        #input('next step -> ')
        if (rename_result['result'] == 'ok'):
            list_ids()
            input(' next -> ')
            if (get_track_album_title(track) != title):
                print(f"CHANGE     track.album.title: {get_track_album_title(track):>60} => {title}")
                set_track_album_title(track,title)
                album = get_track_album(track)
            else:
                print(f"NO CHANGE  track.album.title: {get_track_album_title(track):>60} => {title}")
 
            #if (get_album_title(album) != title):
            #    print(f"CHANGE     album.title: {get_album_title(album):>60} => {title}")
            #    set_album_title(album,title)
            #else:
            #    print(f"NO CHANGE  album.title: {get_album_title(album):>60} => {title}")

            list_ids()

            input(' next -> ')
            if (get_album_artist_name(album) != artist):
                print(f"CHANGE     album.artist.title: {get_album_artist_name(album):>60} => {artist}")
                set_album_artist(album,artist)
            else:
                print(f"NO CHANGE  album.artist.title: {get_album_artist_name(album):>60} => {artist}")
            list_ids()
            
            input(' next -> ')
            artist_obj = album.artist()
            if (get_artist_title(artist_obj) != artist):
                print(f"CHANGE     artist.title: {get_artist_title(artist_obj):>60} => {artist}")
                set_artist_title(artist_obj,artist)
            else:
                print(f"NO CHANGE  artist.title: {get_artist_title(artist_obj):>60} => {artist}")
            list_ids()

            input(' next -> ')
            #track_obj = album.track()
            #print(f"CHANGE     track.title:        {get_track_title(track):>60}   =>   {title}")
            #print(f"CHANGE     track.title:        {get_track_title(track_obj):>60}   =>   {title}")
            if (get_track_title(track) != title):
                print(f"CHANGE     track.title:        {get_track_title(track):>60}   =>   {title}")
                set_track_title(track,title)
            else:
                print(f"NO CHANGE  track.title:        {get_track_title(track):>60}   =>   {title}")
            list_ids()

            input(' next -> ')
            if (get_track_artist_name(track) != artist):
                print(f"CHANGE     track.artist:        {get_track_artist_name(track):>60}   =>   {artist}")                  
                set_track_artist_name(track,artist)
            else:
                print(f"NO CHANGE  track.artist:        {get_track_artist_name(track):>60}   =>   {artist}")                  
            list_ids()

            input(' next -> ')
            current_year = get_album_originallyAvailableAt(album)
            print(f'album.id:  {get_album_id(album)}')
            print(f'album.year:  {current_year}')
            print(f'track.id: {get_track_id(track)}')
            print(f'track.year:  {get_track_year(track)}')

            # the actions above might create a new album associated with the track
            new_album = get_track_album(track)
            current_year = get_album_originallyAvailableAt(new_album)
            print(f'new_album.id:  {get_album_id(new_album)}')
            print(f'new_album.year:  {get_album_originallyAvailableAt(new_album)}')

            if (current_year != year):
                print(f"CHANGE     year:               {current_year:>60}   =>   {year}" )
                set_album_date(new_album,year)
            else:
                print(f"NO CHANGE  year:               {current_year:>60}   =>   {year}" )

            #if (current_year != year):
            #    print(f"CHANGE     year:               {current_year:>60}   =>   {year}" )
            #    set_album_date(album,year)
            #else:
            #    print(f"NO CHANGE  year:               {current_year:>60}   =>   {year}" )

            # input(' done -> ')

        else:
            print(f"ABORTED  error with file renaming")
            print(f'{rename_result}')

'''
            print(f"CHANGE  track.title:        {get_track_title(track):>60}   =>   {title}")
            input('execute step -> ')
            set_track_title(track,title)
            list_ids()

            input(' next -> ')
            #print(f"CHANGE  album.artist: {album.parentTitle:30} => {artist}")
            #set_album_artist(track,artist)

            print(f"CHANGE  album.title.sort:   { get_album_title_sort(album):>60}   =>   {title}")
            input('execute step -> ')
            set_album_title_sort(album,title)
            list_ids()

            print(f"CHANGE  track.album.title:  {get_track_album_title(album):>60}   =>   {title}")
            input('execute step -> ')
            set_album_title(track,title)
            list_ids()

            #artist_obj = track.artist()
            #artist_title_sort = track.artist().titleSort
            print(f"CHANGE  track.artist.sort:  {get_track_artist_name_sort(track):>60}   =>   {artist}" )
            input('execute step -> ')
            set_artist_sort(track,artist)
            list_ids()

            print(f"CHANGE  album.artist: {get_album_artist_name(album):>60}   =>   {artist}" )
            input('execute step -> ')
            set_track_album_artist_name(track,artist)
            #set_album_artist(album, artist)
            list_ids()

            print(f"CHANGE  track.artist:       {get_track_artist_name(track):>60}   =>   {artist}" )
            input('execute step -> ')
            set_track_artist_name(track,artist)
            list_ids()


            #print(f"CHANGE  track.album.artist: {get_track_album_artist_name(track):>60}   =>   {artist}" )
            #input('execute step -> ')
            #set_track_album_artist_name(track,artist)


            current_year = get_album_originallyAvailableAt(album)
            print(f"CHANGE  year:               {current_year:>60}   =>   {year}" )
            input('execute step -> ')
            set_album_date(track,year)
            result = True
        else:
            print(f"ABORTED  error with file renaming")
            print(f'{rename_result}')
            result = False

    #print('')
    #input('Next Track -> <Enter>')
    #print('')
    return result
'''


def sync_metadata(album,track):
    while (True):
        print('')
        #file_info = get_track_file_info(track)
        print(f'album.title:       {get_album_title(album)}') 
        print(f'album.title.sort:  {get_album_title_sort(album)}') 
        print(f'album.artist:      {get_album_artist_name(album)}')
        print(f'album.year:        {get_album_originallyAvailableAt(album)}')
        print(f'track.title:       {get_track_title(track)}')
        print(f'track.album:       {get_track_album_title(track)}')
        print(f'track.artist:      {get_track_artist_name(track)}')
        print(f'track.album.artist:{get_track_album_artist_name(track)}')
        print(f'artist.sort:       {get_album_artist_name_sort(album)}')
        print(f'filename:          {get_track_file_basename(track)}')
        print(f'path:              {get_track_file_path(track)}')
        print(f'album.id:          {get_album_id(album)}')
        print(f'track.id:          {get_track_id(track)}')
        print(f'album.artist.id:   {get_album_artist_id(album)}')
        print(f'track.artist.id:   {get_track_artist_id(track)}')


        print('Folder contents:')
        folder_content = synology_list_folder(get_track_file_dirname(track))
        for f in folder_content:
            print(f'  {f}')

        metadata = get_new_metadata_from_user(track,album)

        if (metadata != False):
            change_metadata(track,album,metadata["title"],metadata["artist"],metadata["year"])

        print(f'<any>  -  Next , go to next track')
        print(f'r      -  Repeat current track')
        print(f'q      -  Quit program')
        user = input('==> ')

        if (user == 'r'):
            continue
        elif (user == 'q'):
            quit()
        else:
            break



# this function goes through all track and compares the track title and album title.
# if these are different, then a new album is created with the name of the track title.
# if present, the year of the original album is capture and set in the newly created album.
# if an album has multiple tracks, then multiple new albums are created.
def analyse(plex_section, empty_year=False):
    global SECTION
    SECTION = plex_section

    print(f"FETCHING all tracks in PLEX section {plex_section.title}  ...")
    tracks = plex_section.all(libtype='track')
    tracks_len = len(tracks)
    print("DONE fetching all tracks: {0}".format(tracks_len))

    list_ids()


    t=1
    x=0
    found = False
    for track in tracks:
        num_of_tracks=0
        try:
            num_of_tracks = len(track.album().tracks())
        except:
           print(f"[TOTAL:{tracks_len} - CURRENT:{t} - CHANGED:{x}]  FATAL - could not get all tracks for track.title: {track_title} - track.title: {track.parentTitle}")
           input('hit enter to continue')

        if (num_of_tracks > 0):
            track_title = track.title
            album = track.album()
            album_title = album.title
            #file_info = get_track_file_info(track)

            print(f"[TOTAL:{tracks_len} - CURRENT:{t} - CHANGED:{x}] ANALYSE  track.title: {track_title}  |  album.title: {album_title}  |  track.filename: {get_track_file_basename(track)}  |  num of media: {len(track.media)}")
            print('')

            if (compare_album_track_file(album,track, empty_year) == False):
                sync_metadata(album,track)
                x=x+1
        t=t+1

        print('################################################################')
        print('')

