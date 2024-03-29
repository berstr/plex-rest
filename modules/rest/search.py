import config

from modules.plex import section as plex_section


def artist(section_name, artist_name):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    else:
        if (artist_name == None):
            result = {'result':'error - artist name not defined'}
        else:
            section = plex_section.get_by_name(section_name)
            if section == None:
                result = {'result':'error - cannot find section with name: %s' % (section_name)}
            else:
                result = plex_section.search.artist(artist_name)
    result = {**result , **{'section_name':section_name, 'artist_name':artist_name}}
    return result

def set_date(section_name, album_key, new_date):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (album_key == None):
        result = {'result':'error - album key not defined'}
    elif (new_date == None):
        result = {'result':'error - new date not defined'}
    elif (re.match("^[0-9][0-9][0-9][0-9]-[01][0-9]-[0-9][0-9]$", new_date) == False):
        result = {'result':'error - new date has not a valid date format (YYYY-MM-DD): %s' % (new_date)}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            album_fetch = section.fetchItem(album_key)
            if album_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (album_key)}
            elif album_fetch['result'] != 'ok': 
                result = album_fetch
            else:
                album = album_fetch['item']
                album.set_date(new_date)
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':album_key,'originallyAvailableAt': new_date}}
    return result    

def set_title(section_name, album_key, title):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (album_key == None):
        result = {'result':'error - album key not defined'}
    elif (title == None):
        result = {'result':'error - new album title not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            album_fetch = section.fetchItem(album_key)
            if album_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (album_key)}
            elif album_fetch['result'] != 'ok': 
                result = album_fetch
            else:
                album = album_fetch['item']
                album.set_title(title)
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':album_key,'title': title}}
    return result    

def set_artist(section_name, album_key, artist):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (album_key == None):
        result = {'result':'error - album key not defined'}
    elif (artist == None):
        result = {'result':'error - new album title not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            album_fetch = section.fetchItem(album_key)
            if album_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (album_key)}
            elif album_fetch['result'] != 'ok': 
                result = album_fetch
            else:
                album = album_fetch['item']
                album.set_artist(artist)
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':album_key,'artist': artist}}
    return result        

def genres_add(section_name, album_key, genres):
    print("rest.album.genres_add() - START")
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (album_key == None):
        result = {'result':'error - album key not defined'}
    elif (genres == None):
        result = {'result':'error - new genres not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            album_fetch = section.fetchItem(album_key)
            if album_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (album_key)}
            elif album_fetch['result'] != 'ok': 
                result = album_fetch
            else:
                album = album_fetch['item']
                print("rest.album.genres_add() - call album.genres_add(%s)" % (genres))
                album.genres_add(genres)
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':album_key,'genres': genres}}
    return result       

def genres_delete(section_name, album_key):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (album_key == None):
        result = {'result':'error - album key not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            album_fetch = section.fetchItem(album_key)
            if album_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (album_key)}
            elif album_fetch['result'] != 'ok': 
                result = album_fetch
            else:
                album = album_fetch['item']
                album.genres_delete()
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':album_key}}
    return result       

def genres_replace(section_name, album_key, genres):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    elif (album_key == None):
        result = {'result':'error - album key not defined'}
    elif (genres == None):
        result = {'result':'error - new genres not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - cannot find section with name: %s' % (section_name)}
        else:
            album_fetch = section.fetchItem(album_key)
            if album_fetch == None:
                result = {'result':'error - cannot find album with key: %s' % (album_key)}
            elif album_fetch['result'] != 'ok': 
                result = album_fetch
            else:
                album = album_fetch['item']
                album.genres_replace(genres)
                result = {'result':'ok','album': album.json() }
    result = {**result , **{'section_name':section_name, 'key':album_key,'genres': genres}}
    return result           