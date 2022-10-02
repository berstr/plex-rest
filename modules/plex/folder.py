import os
import config


#from modules.plex import section as section_

# plexapi.library.Folder class 
# the folder.key attribute for a true folder in the filesystem has the following structure:
# /library/sections/<id>/folder?parent=<id>

def is_subfolder(folder):
    return True
    #return folder.__class__.__name__ == 'Folder'


class PlexFolder:

    # section   modules.plex.PlexSection
    # folder    plexapi.library.Folder()
    def __init__(self, section, plex_folder):
        self.section = section
        self.plex_folder = plex_folder
        self.title = plex_folder.title
        self.key = plex_folder.key
        self.tracks = []
        self.files = []
        self.invalid_entries = [] # a folder should only contain media files, all others go in here (i.e. further folders)
        self._get_folder_contents()


    def _get_folder_contents(self):
        plex_subfolders = self.plex_folder.subfolders()
        for plex_subfolder in plex_subfolders:
            # calling subfolders() for each entry within a folder will determine if it is another folder
            # or a plex track within a music section, or a plex movie within a movie section
            temp = plex_subfolder.subfolders()
            if len(temp) == 0: # empty sub-folder
                self.invalid_entries.append(plex_subfolder)
            elif len(temp) > 1: # sufolder with contents
                self.invalid_entries.append(plex_subfolder)
            else: # len == 1
                if temp[0].__class__.__name__ == 'Track':
                    track = self.section.add_track(temp[0])
                    #print('_get_folder_contents: {}'.format(track.media[0].files[0]))
                    self.tracks.append(track)
                elif temp[0].__class__.__name__ == 'Movie':
                    self.tracks.append(self.section.add_movie(temp[0]))
                else:
                    self.invalid_entries.append(plex_subfolder)
        if len(self.tracks) > 0:
            files = config.PLEX.browse(os.path.dirname(self.tracks[0].media[0].files[0]))
            for file in files:
                if file.path.find('@eaDir') == -1: # @eaDir is from Synology index service to store thumbnails
                    self.files.append(file.path)


    def json(self):
        return {'title':self.title,'key':self.key,'tracks':self.tracks,'files':self.files}
    
'''
    def subfolders(self):
        result = []
        plex_subfolders = self.plex_folder.subfolders()
        for plex_subfolder in plex_subfolders:
            print('PlexFolder.subfolders() - title / key: {} / {}'.format(plex_subfolder.title,plex_subfolder.key ))
            print('PlexFolder.subfolders() - type: {}'.format(plex_subfolder.__class__.__name__))
            if is_subfolder(plex_subfolder):
                result.append(PlexFolder(plex_subfolder))
        return result
'''
