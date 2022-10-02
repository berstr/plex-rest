from modules.plex import section as plex_section
from modules.plex import media as media_


class PlexTrack():

    # plex_track:   plexapi.audio.Track
    def __init__(self, plex_track):
        self.track = plex_track
        self.key = plex_track.key
        self.album = plex_track.album()
        self.artist = plex_track.artist()
        self.grandparentKey = plex_track.grandparentKey
        self.grandparentRatingKey = plex_track.grandparentRatingKey
        self.grandparentTitle = plex_track.grandparentTitle
        self.originalTitle = plex_track.originalTitle
        self.parentKey = plex_track.parentKey
        self.parentRatingKey = plex_track.parentRatingKey
        self.parentTitle = plex_track.parentTitle
        self.primaryExtraKey = plex_track.primaryExtraKey
        #self.trackNumber = plex_track.trackNumber
        #self.tracks = self.__get_tracks(plex_track)
        self.media = self._get_media()
        self.type = 'track'

    def _get_media(self):
        result = []
        for media in self.track.media:
            result.append(media_.PlexMedia(media))
        return result

    def json(self):
        return {'key':self.key,'artist':self.artist, 'album':self.album, 'parentKey':self.parentKey, 'parentRatingKey':self.parentRatingKey, 
                'parentTitle':self.parentTitle,'grandparentKey':self.grandparentKey,'grandparentRatingKey':self.grandparentRatingKey,'grandparentTitle':self.grandparentTitle,
                'originalTitle':self.originalTitle, 'primaryExtraKey':self.primaryExtraKey, 'media':self.media }

