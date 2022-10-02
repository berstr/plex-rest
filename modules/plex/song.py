#from modules.plex import section as plex_section



class PlexSong:

    def __init__(self, plex_song):
        self.plex_song = plex_song


    # plex_song:   plexapi.audio.Album or plexapi.video.Movie
    def __init__(self, plex_song):
        self.plex_song = plex_song
        self.title = plex_song.title
        self.genres = []
        for g in plex_song.genres:
            self.genres.append(g.tag)
        self.rating = plex_song.rating
        self.year = plex_song.year
        temp = plex_song.originallyAvailableAt
        if temp != None:
            self.originallyAvailableAt = temp.strftime("%Y-%m-%d")
        else:
            self.originallyAvailableAt = None
        self.key = plex_song.key

    
    def set_title(self,new_title):
        query = {'title.value': new_title, 'titleSort.value':new_title, 'artist.id.value': self.ratingKey, 'title.locked': 1}
        self.album.edit(**query)
        self.album.reload()
        self.title = new_title
        self.titleSort = new_title
        return self.json()

    def set_artist(self,new_artist):
        query = {'artist.title.value': new_artist, 'title.value':self.title} #, 'artist.title.locked': 1}
        self.album.edit(**query)
        self.album.reload()
        self.artist = new_artist
        return self.json()

    #     originallyAvailableAt.value=2016-11-11
    def set_date(self, new_date):
        query = {'originallyAvailableAt.value': new_date} 
        self.album.edit(**query)
        self.album.reload()
        self.originallyAvailableAt = new_date
        self.year = new_date[:4]
        return self.json()


    # genres:  string - list of comma separated genres, e.g. "Pop , Rock , Blues"
    def genres_add(self, genres):
        genres_a = [x.strip() for x in genres.split(',')]
        for genre in genres_a:
            if (len(genre) > 0) and ((genre in self.genres) == False):
                # for multiple tags at once, you could also say:
                # originallyAvailableAt.locked=1 , genre.locked=1 , genre[0].tag.tag=Pop , genre[1].tag.tag=Rock , genre[2].tag.tag=Blues
                query = {'genre[0].tag.tag': genre, 'genre[0].tag.tag.locked': 1}
                self.album.edit(**query)
                self.album.reload()
                self.genres.append(genre)
        return self.json()

    def json(self):
        return {'title':self.title,'type':self.type, 'artist':self.artist,'genres':self.genres,'tracks':self.tracks, 'year':self.year, 'key':self.key }


    # genres:  string - list of comma separated genres, e.g. "Pop , Rock , Blues"
    def genres_replace(self, genres):
        self.genres_delete()
        self.genres_add(genres)
        return self.json()

    def genres_delete(self):
        if len(self.genres) > 0:
            genres_string = ",".join(self.genres)
            query = {'genre[].tag.tag-': genres_string}
            self.album.edit(**query)
            self.album.reload()
            self.genres = []
        return self.json()



class PlexAudioSong(PlexSong):

    # album:   plexapi.audio.Album
    def __init__(self, plex_album):
        self.album = plex_album
        #self.album = plex_track.album()
        self.tracks = self.__get_tracks(self.album)
        self.artist = self.__get_artist(self.album)
        self.type = 'audio'
        super().__init__(self.album)

    def jsonx(self):
        return {'title':self.title, 'artist':self.artist,'genres':self.genres,'tracks':self.tracks, 'year':self.year, 'key':self.key }

    def __get_artist(self, plex_album):
        result = None
        try:
            #result = plex_album.artist().title
            result = plex_album.parentTitle
        except:
            result = 'Unknown'
        return result



    # album:     plexapi.audio.Album
    # result:    [] String , name of media files disk
    def __get_tracks(self,plex_album):
        result = []
        tracks = plex_album.tracks()
        for track in tracks:
            media = track.media
            for single_media in media:
                parts = single_media.parts
                for part in parts:
                    result.append({'file':part.file, 'artist':track.originalTitle,'album':track.parentTitle,'albumKey':track.parentKey,'mediaTitle':single_media.title,'mediaPartKey':part.key})
        return result



class PlexVideoSong(PlexSong):

    # album:   plexapi.video.Movie
    def __init__(self, plex_movie):
        self.tracks = self.__get_tracks(plex_movie)
        self.artist = self.__get_writer(plex_movie) # the first writer in the writers tag field will be the song artist
        self.type = 'video'
        super().__init__(plex_movie)

    def jsonx(self):
        return {'title':self.title, 'artist':self.artist,'genres':self.genres,'tracks':self.tracks, 'year':self.year,'originallyAvailableAt':self.originallyAvailableAt, 'key':self.key }
 
    def __get_writer(self,plex_movie):
        result = None
        writers = plex_movie.writers
        if len(writers) > 0:
            result = writers[0].tag
        return result

    # album:     plexapi.audio.Album
    # result:    [] String , name of media files disk
    def __get_tracks(self,plex_movie):
        result = []
        media = plex_movie.media
        for single_media in media:
            parts = single_media.parts
            for part in parts:
                result.append(part.file)
        return result




class PlexTrackSong():

    # album:   plexapi.audio.Track
    def __init__(self, plex_track):
        self.track = plex_track
        self.album = plex_track.album()
        #self.artist = plex_track.artist()
        self.grandparentKey = plex_track.grandparentKey
        self.grandparentRatingKey = plex_track.grandparentRatingKey
        self.grandparentTitle = plex_track.grandparentTitle
        self.originalTitle = plex_track.originalTitle
        self.parentKey = plex_track.parentKey
        self.parentRatingKey = plex_track.parentRatingKey
        self.parentTitle = plex_track.parentTitle
        self.primaryExtraKey = plex_track.primaryExtraKey
        #self.trackNumber = plex_track.trackNumber
        self.tracks = self.__get_tracks(plex_track)
        self.type = 'track'


    def json(self):
        return {'originalTitle':self.originalTitle, 'album':self.album, 'parentKey':self.parentKey,'tracks':self.tracks, 'parentRatingKey':self.parentRatingKey, 
                'parentTitle':self.parentTitle,'grandparentKey':self.grandparentKey,'grandparentRatingKey':self.grandparentRatingKey,'grandparentTitle':self.grandparentTitle,
                'primaryExtraKey':self.primaryExtraKey }

    # album:     plexapi.audio.Track
    # result:    [] String , name of media files disk
    def __get_tracks(self,plex_track):
        result = []
        media = plex_track.media
        for single_media in media:
            parts = single_media.parts
            for part in parts:
                    result.append({'file':part.file, 'artist':plex_track.originalTitle,'album':plex_track.parentTitle,'albumKey':plex_track.parentKey,'mediaTitle':single_media.title,'mediaPartKey':part.key})
        return result





