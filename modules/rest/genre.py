import config

from modules.plex import genre as plex_genre


def genres(section_name):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not defined'}
    else:
        result = plex_genre.genres(section_name)
    return result