from modules.plex import section as plex_section


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


# result:   [] { title, key }
def album_names(section_name):
    result = []
    section = plex_section.get_by_name(section_name)
    if section == None:
        result = None
    else:
        for album in section.albums():
            result.append({'title':album.title , 'key':album.key})
    return result

def title(album):
    return album.title

def key(album):
    return album.key

class PlexAlbum:

    # album:   plexapi.audio.Album
    def __init__(self, album, details='no'):
        self.album = album
        self.tracks = self.__get_tracks(album)
        self.title = album.title
        self.artist = album.artist().title
        self.ratingKey = album.artist().ratingKey
        self.titleSort = album.titleSort
        self.year = album.year
        temp = album.originallyAvailableAt
        if temp != None:
            self.originallyAvailableAt = temp.strftime("%Y-%m-%d")
        else:
            self.originallyAvailableAt = None
        self.key = self.album.key
        self.details = details
        self.genres = []
        #print(album.genres)
        for g in album.genres:
            self.genres.append(g.tag)

    def json(self):
        return {'title':self.title,'titleSort':self.titleSort, 'artist':self.artist,'genres':self.genres,'tracks':self.tracks, 'year':self.year,'originallyAvailableAt':self.originallyAvailableAt, 'key':self.key }
    
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

    # album:     plexapi.audio.Album
    # result:    [] String , name of media files disk
    def __get_tracks(self,album):
        result = []
        tracks = album.tracks()
        for track in tracks:
            media = track.media
            for single_media in media:
                parts = single_media.parts
                for part in parts:
                    result.append(part.file)
        return result

