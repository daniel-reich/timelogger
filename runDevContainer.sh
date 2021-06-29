#!/bin/bash

source ./.env
docker run \
    -it \
    -v $(pwd):/app/ \
    -v "${SQLITE_FILEPATH}":/db/ \
    -e JIRA_EMAIL=$JIRA_EMAIL \
    -e JIRA_API_KEY=$JIRA_API_KEY \
    timeloggerdev /bin/bash

