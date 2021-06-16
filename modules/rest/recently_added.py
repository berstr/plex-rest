import os

from modules.synology import synology
from modules.plex import section as plex_section

import config

def get(section_name, details, limit):
    result = None
    if (section_name == None):
        result = {'result':'error - section name not set'}
    else:
        section = plex_section.get_by_name(section_name)
        if (section != None):
            config.LOGGER.info("recently_added.by_name() - found section with name: %s" % (section.title))
            if (limit==None):
                limit = 10
                config.LOGGER.info("recently_added.request() - set limit to default value: %s" % (limit))
            else:
                limit = int(limit)
            result = section.search(limit, 'addedAt')
        else:
            result = {'result':'error - section with name %s not found' % (section_name), 'section_name': section_name}
    return result
