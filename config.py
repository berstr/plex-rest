from flask import Flask, jsonify, request

from modules.plex import login


import os
import logging
from newrelic.agent import NewRelicContextFormatter
from logging.handlers import RotatingFileHandler

APP = Flask(__name__)

# The following variables should be set through env variables
PLEX_USERNAME = None
PLEX_PASSWORD = None
PLEX_SERVERNAME = None
# Port for the plex-rest service. Defined by env variable PLEX_REST_PORT. Default is 37082
PLEX_REST_PORT = '37082'
SYNOLOGY_FILESTATION_SERVICE = None

# Are being set by the application at runtime:
PLEX_LIBRARY_SECTIONS = {}
LOGGER = None
PLEX = None


# ==========================
# Init of variables
# ==========================


# SYNOLOGY_FILESTATION_SERVICE is the hostname (IP address) and port number where the synology-filestation runs
# Example: 192.168.178.99:8888
SYNOLOGY_FILESTATION_SERVICE=os.environ.get("SYNOLOGY_FILESTATION_SERVICE")
if (SYNOLOGY_FILESTATION_SERVICE == None):
    SYNOLOGY_FILESTATION_SERVICE='localhost:37081'


PLEX_USERNAME=os.environ.get("PLEX_USERNAME")
PLEX_PASSWORD=os.environ.get("PLEX_PASSWORD")
PLEX_SERVERNAME=os.environ.get("PLEX_SERVERNAME")

env=os.environ.get("PLEX_REST_PORT")
if (env != None):
    PLEX_REST_PORT=env


def init():
    init_logger()
    plex_login()

def plex_login():
    global PLEX
    PLEX = login.plex_login(PLEX_USERNAME, PLEX_PASSWORD, PLEX_SERVERNAME)

def init_logger():
    global LOGGER
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler('logs/plex-rest.log', maxBytes=10485760, backupCount=2) # max logfile size: 10MB
    newrelic_formatter = NewRelicContextFormatter()
    file_handler.setFormatter(newrelic_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    LOGGER = logger
