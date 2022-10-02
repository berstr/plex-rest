import os
import re


# Container object for all MediaPart objects. Provides useful data about the video or audio this media belong to such as video framerate, resolution, etc.
class PlexMedia:

    # plex_media:   plexapi.media.Media
    def __init__(self, plex_media):
        self.plex_media = plex_media
        self.title = plex_media.title
        self.id = plex_media.id
        self.files = []
        for part in plex_media.parts:
            self.files.append(part.file)

    def json(self):
        return {'title':self.title, 'id':self.id,'files':self.files }


  