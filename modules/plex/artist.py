#from modules.plex import section as plex_section


class PlexArtist:

    # artist:   plexapi.audio.Artist
    def __init__(self, artist):
        self.artist = artist
        self.title = artist.title
        self.key = artist.key
        self.genres = []
        for g in artist.genres:
            self.genres.append(g.tag)
        self.tracks = self.__get_tracks(artist)
        self.albums = self.__get_albums(artist)  # [] { title: <string>, key: <string> }

    def json(self):
        return {'artis':self.title,'albums':self.albums,'tracks':self.tracks, 'genres':self.genres,'key':self.key }
    

    # artist:     plexapi.audio.Artist
    # result:    [] String , name of media files disk
    def __get_tracks(self,artist):
        result = []
        tracks = artist.tracks()
        for track in tracks:
            media = track.media
            for single_media in media:
                parts = single_media.parts
                for part in parts:
                    result.append(part.file)
        return result

    # artist:     plexapi.audio.Artist
    # result:    [] { title: <string>, key: <string> }
    def __get_albums(self,artist):
        result = []
        albums = artist.albums()
        for album in albums:
            title = album.title
            key = album.key
            result.append({'title':title,'key':key})
        return result
