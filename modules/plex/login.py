from plexapi.myplex import MyPlexAccount
import config


# username:         String
# password:         String
# plex_server_name:      String , name of the Plex server instance (not hostname)
# result:           plexapi.server.PlexServer
def plex_login(username, password, plex_server_name ):
    config.LOGGER.info("plex_login() - START - plex_server: %s" % (plex_server_name))
    plex_server = MyPlexAccount(username, password)
    result = plex_server.resource(plex_server_name).connect()
    config.LOGGER.info("plex_login() - result: %s" % (result))
    config.LOGGER.info("plex_login() - COMPLETED")
    return result