import sys
import plexapi.exceptions

from modules.plex import album as plex_album
from modules.plex import video as plex_video

import config

# result: [] plexapi.LibrarySection
def sections():
    return config.PLEX.library.sections()

# result:   [] string
def section_names():
    result = []
    for section in config.PLEX.library.sections():
        result.append(section.title)
    return result

# result: model.section.PlexSection
def get_by_uuid(uuid: str):
    result = None
    for section in sections():
        if (section.uuid == uuid):
            result = PlexSection(section)
            break
    return result

# result: model.section.PlexSection
def get_by_name(name: str):
    result = None
    sections = config.PLEX.library.sections()
    for section in sections:
        if (section.title == name):
            result = PlexSection(section)
            break
    return result




class PlexSection:

    # section:   plexapi.library.LibrarySection
    def __init__(self, section):
        self.section = section
        self.title = section.title
        self.uuid = section.uuid
        self.type = type(section).__name__
        if self.type == 'MovieSection':
            self.genres = [f.title for f in  section.listFilterChoices('movie.genre')]
        else:
            self.genres = [f.title for f in  section.listFilterChoices('album.genre')]

    def json(self):
        return {'title':self.title,'type':self.type, 'uuid':self.uuid , 'genre':self.genre}
    
    def scan(self):
        result = None
        try:
            r = self.section.update()
            result = {'result':'ok'}
        except: # catch *all* exceptions
            exception_type = sys.exc_info()[0]
            exception_value = sys.exc_info()[1]
            result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value}
        return {**result , **{'section':self.title, 'section-type':self.type}}
        
    def items(self,details = 'no'):
        return self.search(None, 'titleSort', details)

    '''    
    def genres(self):
        result = None
        genres = {}
        alben = plex_album.albums(self.section)
        for album in alben:
            for genre in album.genres:
                if genre not in result:
                    genres[genre.tag] = genre
        return {'result':'ok', **genres}
    '''

    def search(self, limit, sortBy, details = 'no'):
        config.LOGGER.info("model.section.PlexSection.search() - limit: %s - sortBy: %s - details: %s - section.type: %s" % (limit, sortBy, details, self.type))
        result = None
        try:
            items = []
            # calls the Plex API search()
            if self.type == 'MovieSection':
                if limit == None:
                    plex_movies = self.section.searchMovies(sort='titleSort')
                else:
                    plex_movies = self.section.searchMovies(maxresults=limit, sort='titleSort')
                for plex_movie_ in plex_movies:
                    if details == 'yes':
                        items.append(plex_video.PlexVideo(plex_movie_))
                    else:
                        items.append({'title':plex_video.title(plex_movie_), 'key':plex_video.key(plex_movie_)})
                result = { 'result':'ok', 'items':items, 'count':len(items)}
            elif self.type == 'MusicSection':
                if limit == None:
                    plex_albums = self.section.searchAlbums(sort='titleSort')
                else:
                    plex_albums = self.section.searchAlbums(maxresults=limit, sort='titleSort')
                for plex_album_ in plex_albums:
                    if details == 'yes':
                        items.append(plex_album.PlexAlbum(plex_album_))
                    else:
                        items.append({'title':plex_album.title(plex_album_), 'key':plex_album.key(plex_album_)})
                result = { 'result':'ok', 'items':items,'count':len(items)}
            else:
                result = {'result':'unsupported plex section type: %s - section: %s' % (self.type, self.title)}
        except: # catch *all* exceptions
            exception_type = str(sys.exc_info()[0])
            exception_value = str(sys.exc_info()[1])
            result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value}
        
        return {**result , **{'section':self.title, 'section-type':self.type}}

    
    # item_key:         string      -   plex key for an item, e.g. /library/metadata/23065
    def fetchItem(self, item_key):
        result = None
        try:
            # this calls the Plex API function fetchItem()
            plex_item = self.section.fetchItem(item_key)
            if plex_item != None:
                if self.type == 'MovieSection':
                    model_item = plex_video.PlexVideo(plex_item)
                elif self.type == 'MusicSection':
                    model_item = plex_album.PlexAlbum(plex_item)
                result = {'result':'ok', 'item': model_item}
            else:
                result = {'result':'plex cannot find item with key: %s' % (item_key), 'section':self.title, 'section-type':self.type,'key': item_key}
        except plexapi.exceptions.NotFound as e:
            result = {'result':'plex exception: item not found'}
        except: # catch *all* exceptions
            exception_type = str(sys.exc_info()[0])
            exception_value = str(sys.exc_info()[1])
            result = {'result':'plex exception: %s' % (exception_type), 'key': item_key, 'section':self.title, 'section-type':self.type, 'exception-type':exception_type, 'exception_value':exception_value}
        result = {**result , **{'section':self.title, 'section-type':self.type,'key': item_key}}
        return result



