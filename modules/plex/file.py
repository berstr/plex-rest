import os
import re


class PlexFile:

    # path:   filesystem path to song track, e.g. /volume1/music/tmp/music/Adele/Adele - Hello (2015).mp3
    def __init__(self, path):
        self.song = None
        self.path = path
        self.dir = os.path.dirname(path)
        temp = os.path.splitext(os.path.basename(path))
        self.filename = temp[0]
        self.ext = temp[1]
        self.artist = ''
        self.title=''
        self.year=''
        pattern = '^(.*) \- (.*) \((.*)\)$'
        m = re.match(pattern,self.filename)
        if (m != None) and (m.group() == self.filename) and (len(m.groups()) == 3):
            self.artist = m.group(1)
            self.title=m.group(2)
            self.year=m.group(3)
            self.valid_filename = True
        else:
            self.valid_filename = False

    def json(self):
        return {'path':self.path, 'filename':self.filename,'valid_filename':self.valid_filename, 'artist':self.artist,'title':self.title,'year':self.year }

    def set_title(self,new_title):
        query = {'title.value': new_title, 'title.locked': 1}
        self.album.edit(**query)
        self.album.reload()
        self.title = new_title
        self.titleSort = new_title
        return self.json()

    def has_extension(path):
        temp = os.path.splitext(os.path.basename(path))
        if temp[1] != '':
            return True
        else:
            return False



  