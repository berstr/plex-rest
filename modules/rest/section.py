import config

#from modules.plex import section as plex_section
from modules.plex import section as plex_section

def item(section_name, key):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not set'}
    elif key == None:
        result = {'result':'error - item key value not defined'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - section cannot be found', 'section':section_name}
        else:
            result = section.fetchItem(key)
            # if fetch was successful, the result will contain a PlexAlbum or PlexVideo objet.
            # these must be first converted into JSON before sending a HTTP reply
            if result['result'] == 'ok':
                result['item'] = result['item'].json()
    return result


def items(section_name, details):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not set','section':section_name, 'details':details}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - section cannot be found', 'section':section_name, 'details':details}
        else:
            config.LOGGER.info("rest.section: %s" % (section))
            result = section.songs
            # if details are requested, the result will contain PlexAlbum or PlexVideo objects
            # these must be first converted into JSON before sending a HTTP reply
            if details == 'yes':
                json_items = []
                for item in result['items']:
                    json_items.append(item.json())
                result['items'] = json_items
    return result

def names():
    result = None
    sections = []
    for section in plex_section.sections():
        sections.append(section.title)
    result = {'result':'ok', 'sections': sections }
    return result

def scan(section_name):
    result = None
    if (section_name == None):
        result = {'result':'error - parameter [section_name] not set'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - section cannot be found', 'section_name':section_name}
        else:
            result = section.scan()
    return result

def section_type(section_name):
    if (section_name == None):
        result = {'result':'error - parameter [section_name] not set'}
    else:
        section = plex_section.get_by_name(section_name)
        if section == None:
            result = {'result':'error - section cannot be found', 'section_name':section_name}
        else:
            result = {'result':'ok', 'section_name':section_name, 'type': section.type }
    config.LOGGER.info("rest.section.section_type() - result %s" % (result))
    return result


def get_by_name(name):
    result = None
    if (name == None):
        result = {'result':'error - parameter [section_name] not set'}
    else:
        section = plex_section.get_by_name(name)
        if (section != None):
            result = {'result':'ok', 'section': section.title, 'uuid':section.uuid}
        else:
            result = {'result':'error - section with name %s not found' % (name), 'name': name}
    config.LOGGER.info("rest.section.by_name() - result %s" % (result))
    return result



def get_by_uuid(uuid):
    result = None
    if (uuid == None):
        result = {'result':'error - section uuid not set'}
    else:
        section = plex_section.get_by_uuid(uuid)
        if (section != None):
            result = {'result':'ok', 'section': section.title, 'uuid':section.uuid}
        else:
            result = {'result':'error - section with uuid %s not found' % (uuid), 'uuid': uuid}
    config.LOGGER.info("rest.section.by_uuid() - result %s" % (result))
    return result
