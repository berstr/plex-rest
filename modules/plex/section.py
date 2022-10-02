import sys
import plexapi.exceptions

#from modules.plex import artist as plex_artist
from modules.plex import song as plex_song
from modules.plex import file as plex_file
from modules.plex import folder as plex_folder
from modules.plex import track as track_
from modules.plex import movie as movie_

#from modules.plex import video as plex_video

import config

PlexSections = []

# string    [] sectionNames
def init(sectionNames):
    global PlexSections
    plex_sections = config.PLEX.library.sections()
    for plex_section in plex_sections:
        if plex_section.title in sectionNames:
            instance = __section_instance(plex_section)
            if instance['result'] == 'ok':
                PlexSections.append(instance['instance'])
            else:
                config.LOGGER.error('ERROR - could not instantiate Plex Section - result: {}'.format(instance))
    return PlexSections

# result: model.section.PlexSection
def get_by_name(name: str):
    result = None
    sections = config.PLEX.library.sections()
    #for section in sections:
    #    print(f'Section: {section.title} - Tpye: {type(section).__name__}')
    for section in sections:
        if (section.title == name):
            result = PlexSection(section)
            break
    return result

def scan(title):
        result = None
        return result
'''
        try:
            r = plex_section.section.update()
            result = {'result':'ok'}
        except: # catch *all* exceptions
            exception_type = sys.exc_info()[0]
            exception_value = sys.exc_info()[1]
            result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value}
        return {**result , **{'section':self.title, 'section-type':self.type}}
'''        


def __section_instance(plex_section):
    result = None
    section_type = type(plex_section).__name__
    if section_type == 'MusicSection':
        section = PlexMusicSection(plex_section)
        result = {'result':'ok','instance':section}
    elif section_type == 'MovieSection':
        section = PlexMovieSection(plex_section)
        result = {'result':'ok','instance':section}
    else:
        section_name = plex_section.title
        result = {'result':'unsupported section type: {} , section_name: {}'.format(section_type,section_name),'type':section_type,'name':section_name}
    return result


class PlexSection:

    # section:   plexapi.library.LibrarySection
    def __init__(self, section):
        self.section = section
        self.title = section.title
        self.uuid = section.uuid
        self.key = section.key
        self.locations = section.locations
        self.type = type(section).__name__
        
    # genre_filter:  either 'movie.genre' or 'album.genre'
    def _init_get_genres(self, genre_filter):
        result = []
        plex_genres = self.section.listFilterChoices(genre_filter)
        for genre in plex_genres:
            result.append(genre.title)
        return result


class PlexMovieSection(PlexSection):

    def __init__(self,plex_section):
        super().__init__(plex_section)
        #self.songs = self.__init_get_songs()
        self.genres = super()._init_get_genres('movie.genre')
        self.movies = []
        self.songs = self.movies # in a movie section, a movie is a song

    def json(self):
        return {'title':self.title,'type':self.type, 'key':self.key , 'genres':self.genres, 'songs':self.songs,'files':self.files}

    def add_movie(self,plex_movie):
        result = None
        new_movie = True
        for movie in self.movies:
            if movie.key == plex_movie.key:
                new_movie = False
                break
        if new_movie:
            result = movie_.PlexMovie(plex_movie)
            self.movies.append(result)
        return result

    def __init_get_songs(self):
        result = []
        movies = self.section.all()
        for movie in movies:
            song = plex_song.PlexVideoSong(movie)
            result.append(song)
        return result    


class PlexMusicSection(PlexSection):

    def __init__(self,plex_section):
        super().__init__(plex_section)
        self.genres = PlexSection._init_get_genres(self,'album.genre')
        self.tracks = []
        self.albums = []
        # self.songs = self.albums # in a music section, an album is a song .... self.__init_get_songs()
        self.songs = self.__init_get_songs()
        

    def json(self):
        return {'title':self.title,'type':self.type, 'key':self.key , 'genres':self.genres, 'files':self.files}

    def __init_get_songs(self):
        result = []
        albums = self.section.albums()
        for album in albums:
            song = plex_song.PlexAudioSong(album)
            result.append(song)
        return result
    
    def add_track(self,plex_track):
        result = None
        new_track = True
        for track in self.tracks:
            if track.key == plex_track.key:
                new_track = False
                break
        if new_track:
            result = track_.PlexTrack(plex_track)
            self.tracks.append(result)
        return result

    def _get_folders(self):
        pass


# -----------------------------------

'''

class PlexSection:

    # section:   plexapi.library.LibrarySection
    def __init__(self, section):
        self.section = section
        self.title = section.title
        self.uuid = section.uuid
        self.key = section.key
        self.location = section.locations[0]
        self.type = type(section).__name__
        #self.files = self.__init_get_files()

    def folders(self):
        result = []
        folders = self.section.folders()
        for folder in folders:
            if plex_folder.is_subfolder(folder):
                result.append(plex_folder.PlexFolder(folder))
        return result


    def songs(self):
        result = []
        plex_folders = self.section.folders()
        for plex_folder in plex_folders:
            result.append(plex_folder.PlexFolder(plex_folder))
        return result


    def __init_get_files(self):
        result = []
        locations = self.section.locations
        for location in locations:
            artist_folders = config.PLEX.browse(location)
            for artist_folder in artist_folders:
                song_files = config.PLEX.browse(artist_folder.path)
                for song_file in song_files:
                    if plex_file.PlexFile.has_extension(song_file.path):
                        result.append(plex_file.PlexFile(song_file.path))
        return result

    
    def xsearch_artist(self,name):
        result = None
        if self.type == 'MovieSection':
            self.genres = [f.title for f in  section.listFilterChoices('movie.genre')]
        else:
            plex_search = self.section.search(title=name,libtype='artist',sort='titleSort')
        artists = []
        for artist in plex_search: 
            artists.append(plex_artist.PlexArtist(artist))
        if len(artists) > 0:
            result['result'] = 'ok'
        else:
            result['result'] = f'no artist with name: {name}'
        return result

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


    # Returns an array of PlexAlbum objects that match the artist string:
    # {'title': 'Hello', 'titleSort': 'Hello', 'artist': 'Adele', 'genres': ['Hard Rock', 'Blues'], 
    # 'tracks': ['/volume1/music/tmp/music/Adele/Adele - Hello (2015).mp3'], 
    # 'year': 2012, 'originallyAvailableAt': '2012-07-07', 'key': '/library/metadata/25431'}
    # artists = music_section.section.search(libtype='artist', sort='addedAt', title='Adele') #filters={"artist.title": "Adele"}))


    def search_artist(self, artist, sortBy='addedAt'):
        config.LOGGER.info("model.section.PlexSection.search_artist() - artist: %s - sortBy: %s - section.type: %s" % (artist, sortBy, self.type))
        result = []

        try:
            artists = []
            # calls the Plex API search()
            if self.type == 'MovieSection':
                if limit == None:
                    plex_movies = self.section.searchMovies(sort=sortBy)
                else:
                    plex_movies = self.section.searchMovies(maxresults=limit, sort='titleSort')
                for plex_movie_ in plex_movies:
                    if details == 'yes':
                        items.append(plex_video.PlexVideo(plex_movie_))
                    else:
                        items.append({'title':plex_video.title(plex_movie_), 'key':plex_video.key(plex_movie_)})
                result = { 'result':'ok', 'items':items, 'count':len(items)}
            elif self.type == 'MusicSection':
                search_result = self.section.search(libtype='artist', sort=sortBy, title=artist)
                for artist in search_result:
                    artists.append({plex_album.PlexAlbum(item)
                    'title':plex_album.title(plex_album_), 'key':plex_album.key(plex_album_)})
                result = { 'result':'ok', 'items':items,'count':len(items)}
            else:
                result = {'result':'unsupported plex section type: %s - section: %s' % (self.type, self.title)}
        except: # catch *all* exceptions
            exception_type = str(sys.exc_info()[0])
            exception_value = str(sys.exc_info()[1])
            result = {'result':'plex exception: %s' % (exception_type), 'exception-type':exception_type, 'exception_value':exception_value}
        
        return {**result , **{'section':self.title, 'section-type':self.type}}



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
                    #plex_albums = self.section.searchAlbums(sort='titleSort')
                    plex_albums = self.section.searchAlbums(sort='addedAt')
                    
                else:
                    #plex_albums = self.section.searchAlbums(maxresults=limit, sort='titleSort')
                    plex_albums = self.section.searchAlbums(maxresults=limit, sort='addedAt')
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



'''

# --------------------------------------

'''
# section_name: string
# result:       [] modules.model.PlexAlbum
def albums(section_name):
    result = []
    section = plex_section.by_name(section_name)
    if section == None:
        result = None
    else:
        for album in section.albums():
            model_album = PlexAlbum(album)
            result.append(model_album.json())
    return result


def xget_artists(section):
    result = {}
    for song in section.songs:
        if not song.artist in result.keys():
            result[song.artist] = []
    for song in section.songs:
        result[song.artist].append(song)
    return result

def xget_all_artists():
    result = {}
    artists = []
    all_artists = []
    for section in PlexSections:
        all_artists.append(get_artists(section))
    print(all_artists)

    for section_artists in all_artists:
        # inti the result array
        for artist in section_artists.keys(): # each key is the name of the artist
            if not artist in result.keys():
                result[artist] = []
        print('result after inti: {}'.format(result))
        for artist in section_artists.keys(): # each key is the name of the artist
            print(' -- artist: {}'.format(artist))
            print(' ---- songs: {}'.format(section_artists[artist]))
            for song in section_artists[artist]:
                result[artist].append(song)
    return result


def xby_name(section_name):
    result = None
    for section in PlexSections:
        if section.title == section_name:
            result = section
            break
    return result


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
    #for section in sections:
    #    print(f'Section: {section.title} - Tpye: {type(section).__name__}')
    for section in sections:
        if (section.title == name):
            result = PlexSection(section)
            break
    return result

'''