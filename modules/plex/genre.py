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


'''
# result: { string : <plexapi.media.Genre> }
def genres(section_name):
    result = {}
    section = plex_section.get_by_name(section_name)
    if section != None:
        result = plex_section.genres()
    else:
        result = {'result':'error - section with name %s not found' % (section_name), 'name': section_name}
        #alben = plex_album.albums(section)
        # for album in alben:
        #    for genre in album.genres:
        #        if genre not in result:
        #            result[genre.tag] = genre
    return result

'''