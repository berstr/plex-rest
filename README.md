## Intro

This service is using the Python Plex API:

    https://python-plexapi.readthedocs.io/en/latest/

---

## Env Variables

    export NEW_RELIC_LICENSE_KEY=XXXX
    export NEW_RELIC_APP_NAME=XXXX

    export NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=XXX
    export NEW_RELIC_INFINITE_TRACING_TRACE_OBSERVER_HOST=<Trace Observer Host>

    export NEW_RELIC_APPLICATION_LOGGING_ENABLED=true
    export NEW_RELIC_APPLICATION_LOGGING_FORWARDING_ENABLED=true

    export PLEX_USERNAME=XXXX
    export PLEX_PASSWORD=XXXX
    export PLEX_SERVERNAME=XXXX

---

## CLI

Manual start from command line:

newrelic-admin run-program python3 plex-rest.py

---

## Docker

X.Y is the image tag

    docker build -t bstransky/plex-rest:X.Y .

    docker push bstransky/plex-rest:X.Y

On VM:

    docker run -d --name plex-rest -e NEW_RELIC_LICENSE_KEY -e NEW_RELIC_DISTRIBUTED_TRACING_ENABLED -e NEW_RELIC_INFINITE_TRACING_TRACE_OBSERVER_HOST -e NEW_RELIC_APP_NAME -e NEW_RELIC_APPLICATION_LOGGING_ENABLED -e NEW_RELIC_APPLICATION_LOGGING_FORWARDING_ENABLED -e PLEX_USERNAME -e PLEX_PASSWORD -e PLEX_SERVERNAME -e SYNOLOGY_FILESTATION_SERVICE -v /var/log/container:/logs -p37082:37082 bstransky/plex-rest:X.Y
