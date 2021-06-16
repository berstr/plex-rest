## Intro

This service is using the Python Plex API:  

    https://python-plexapi.readthedocs.io/en/latest/

-------------------

## Env Variables

    export NEW_RELIC_LICENSE_KEY=XXXX
    export NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
    export NEW_RELIC_APP_NAME="plex-rest"

    export PLEX_USERNAME=XXXX
    export PLEX_PASSWORD=XXXX
    export PLEX_SERVERNAME=XXXX

SYNOLOGY_FILESTATION_SERVICE is the hostname (IP address) and port number where the synology-filestation runs
Example: <host IP>:<Port>
Default: 'localhost:37082'

    export SYNOLOGY_FILESTATION_SERVICE=XXXX

----------------

## CLI

Manual start from command line:

newrelic-admin run-program python3 plex-rest.py

---------------------

## Docker

X.Y is the image tag

    docker build -t berndstransky/plex-rest:X.Y .

    docker push berndstransky/plex-rest:X.Y

On VM:

    docker run -d --name plex-rest -e NEW_RELIC_LICENSE_KEY -e NEW_RELIC_DISTRIBUTED_TRACING_ENABLED -e NEW_RELIC_APP_NAME -e PLEX_USERNAME -e PLEX_PASSWORD -e PLEX_SERVERNAME -e SYNOLOGY_FILESTATION_SERVICE -v /var/log/container:/logs -p37082:37082 berndstransky/plex-rest:X.Y

On Macbook:

    docker run -d --name plex-rest -e NEW_RELIC_LICENSE_KEY -e NEW_RELIC_DISTRIBUTED_TRACING_ENABLED -e NEW_RELIC_APP_NAME -e PLEX_USERNAME -e PLEX_PASSWORD -e PLEX_SERVERNAME -e SYNOLOGY_FILESTATION_SERVICE -v $(pwd)/logs:/logs -p37082:37082 berndstransky/plex-rest:X.Y