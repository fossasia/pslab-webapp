#!/usr/bin/env bash
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    echo "Not a PR. Skipping surge deployment"
    exit 0
fi

ember build --environment=production

export REPO_SLUG_ARRAY=(${TRAVIS_REPO_SLUG//\// })
export REPO_OWNER=${REPO_SLUG_ARRAY[0]}
export REPO_NAME=${REPO_SLUG_ARRAY[1]}

npm i -g surge

# Details of a dummy account. So can be added to vcs.
export SURGE_LOGIN=jithinuser@gmail.com
export SURGE_TOKEN=41d3b52898d9b490a0c45d832e6a03ef

export DEPLOY_DOMAIN=https://${REPO_NAME}.surge.sh
surge --project ./dist --domain $DEPLOY_DOMAIN;
