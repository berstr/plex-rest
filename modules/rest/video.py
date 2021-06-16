import re
import config

#from modules.plex import video as plex_video
from modules.plex import section as plex_section

def set_date(section_name, video_key, new_date):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (video_key == None):
        result = {'result':'error - video key not defined'}
    elif (new_date == None):
        result = {'result':'error - new date not defined'}
    elif (re.match("^[0-9][0-9][0-9][0-9]-[01][0-9]-[0-9][0-9]$", new_date) == False):
        result = {'result':'error - new date has not a valid date format (YYYY-MM-DD): %s' % (new_date)}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            video_fetch = section.fetchItem(video_key)
            if video_fetch == None:
                result = {'result':'error - cannot find video with key: %s' % (video_key)}
            elif video_fetch['result'] != 'ok': 
                result = video_fetch
            else:
                video = video_fetch['item']
                video.set_date(new_date)
                result = {'result':'ok','video': video.json() }
    result = {**result , **{'section_name':section_name, 'key':video_key,'originallyAvailableAt': new_date}}
    return result    


def set_title(section_name, video_key, title):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (video_key == None):
        result = {'result':'error - video key not defined'}
    elif (title == None):
        result = {'result':'error - new video title not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            video_fetch = section.fetchItem(video_key)
            if video_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (video_key)}
            elif video_fetch['result'] != 'ok': 
                result = video_fetch
            else:
                album = video_fetch['item']
                album.set_title(title)
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':video_key,'title': title}}
    return result    


def set_artist(section_name, video_key, artist):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (video_key == None):
        result = {'result':'error - video key not defined'}
    elif (artist == None):
        result = {'result':'error - new video artist not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            video_fetch = section.fetchItem(video_key)
            if video_fetch == None:
                result = {'result':'error - cannot find video with key: %s' % (video_key)}
            elif video_fetch['result'] != 'ok': 
                result = video_fetch
            else:
                video = video_fetch['item']
                video.set_artist(artist)
                result = {'result':'ok','video': video.json() }
    result = {**result , **{'section_name':section_name, 'key':video_key,'artist': artist}}
    return result        

def genres_add(section_name, video_key, genres):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (video_key == None):
        result = {'result':'error - video key not defined'}
    elif (genres == None):
        result = {'result':'error - new genres not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            video_fetch = section.fetchItem(video_key)
            if video_fetch == None:
                result = {'result':'error - cannot find video with key: %s' % (video_key)}
            elif video_fetch['result'] != 'ok': 
                result = video_fetch
            else:
                video = video_fetch['item']
                video.genres_add(genres)
                result = {'result':'ok','album': video.json() }
    result = {**result , **{'section_name':section_name, 'key':video_key,'genres': genres}}
    return result       

def genres_replace(section_name, video_key, genres):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (video_key == None):
        result = {'result':'error - video key not defined'}
    elif (genres == None):
        result = {'result':'error - new genres not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            video_fetch = section.fetchItem(video_key)
            if video_fetch == None:
                result = {'result':'error - cannot find video with key: %s' % (video_key)}
            elif video_fetch['result'] != 'ok': 
                result = video_fetch
            else:
                video = video_fetch['item']
                video.genres_replace(genres)
                result = {'result':'ok','album': video.json() }
    result = {**result , **{'section_name':section_name, 'key':video_key,'genres': genres}}
    return result       

def genres_delete(section_name, video_key):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (video_key == None):
        result = {'result':'error - video key not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            video_fetch = section.fetchItem(video_key)
            if video_fetch == None:
                result = {'result':'error - cannot find video with key: %s' % (video_key)}
            elif video_fetch['result'] != 'ok': 
                result = video_fetch
            else:
                video = video_fetch['item']
                video.genres_delete()
                result = {'result':'ok','album': video.json() }
    result = {**result , **{'section_name':section_name, 'key':video_key}}
    return result       