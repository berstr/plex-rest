def title(video):
    return video.title

def key(video):
    return video.key

class PlexVideo:

    # album:   plexapi.audio.Album
    def __init__(self, video):
        self.video = video
        self.title = video.title
        self.titleSort = video.titleSort
        self.originalTitle = video.originalTitle
        self.key = video.key
        # Movies do not have artists - we always use the first name in the Writers field
        temp = self.video.writers
        if (temp != None and len(temp) > 0):
            self.artists = []
            for a in temp:
                self.artists.append(a.tag)
        else:
            self.artists = [None]
        self.year = self.video.year
        temp = video.originallyAvailableAt
        if temp != None:
            self.originallyAvailableAt = temp.strftime("%Y-%m-%d")
        else:
            self.originallyAvailableAt = None
        self.tracks = video.locations
        self.genres = []
        for g in video.genres:
            self.genres.append(g.tag)

    def artist(self):
        return self.artists[0]

    def set_title(self,new_title):
        query = {'title.value': new_title, 'titleSort.value':new_title, 'originalTitle.value':new_title, 'title.locked': 1}
        self.video.edit(**query)
        self.video.reload()
        self.title = new_title
        self.titleSort = new_title
        self.originalTitle = new_title
        return self.json()

    def set_artist(self,new_artist):
        self.__remove_all_artist()
        query = {'writer[0].tag.tag': new_artist, 'writer.locked':1} 
        self.video.edit(**query)
        self.video.reload()
        self.artists = [new_artist]
        return self.json()

    def set_artist(self,new_artist):
        self.__remove_all_artist()
        query = {'writer[0].tag.tag': new_artist, 'writer.locked':1} 
        self.video.edit(**query)
        self.video.reload()
        self.artists = [new_artist]
        return self.json()

#     originallyAvailableAt.value=2016-11-11
    def set_date(self, new_date):
        query = {'originallyAvailableAt.value': new_date, 'title.locked': 1, 'originallyAvailableAt.locked' : 1} 
        self.video.edit(**query)
        self.video.reload()
        self.originallyAvailableAt = new_date
        self.year = new_date[:4]
        return self.json()

    def json(self):
        return {'title':self.title,'titleSort':self.titleSort,'originalTitle':self.originalTitle,'artist':self.artists[0], 'genres':self.genres , 'year':self.year, 'originallyAvailableAt':self.originallyAvailableAt, 'tracks':self.tracks, 'key':self.key }

    def __remove_all_artist(self):
        artists_string = ",".join(self.artists)
        query = {'writer[].tag.tag-': artists_string}
        self.video.edit(**query)
        self.video.reload()
        self.artists = [None]

