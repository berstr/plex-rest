from modules.plex import section as plex_section


# result: [ string ] list of genre names ; [] if no genres exist
def genres(section_name):
    section = plex_section.get_by_name(section_name)
    if section != None:
        genres = section.genres
        result = {'result':'ok', 'genres': genres, 'section': section_name}
    else:
        result = {'result':'error - section with name %s not found' % (section_name), 'section': section_name}
    return result

#from modules.plex import section as plex_section


class PlexGenre:

    # genre:    plexapi.media.Genre
    def __init__(self, genre):
        self.plex_genre = genre
        self.genre = genre.tag
        self.key = genre.key

    def json(self):
        return {'genre':self.genre,'key':self.key }
    

