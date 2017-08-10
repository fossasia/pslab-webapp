#!/usr/bin/env bash
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    echo "Not a PR. Skipping surge deployment"
    exit 0
fi

ember build production

export REPO_SLUG_ARRAY=(${TRAVIS_REPO_SLUG//\// })
export REPO_OWNER=${REPO_SLUG_ARRAY[0]}
export REPO_NAME=${REPO_SLUG_ARRAY[1]}

npm i -g surge

export DEPLOY_DOMAIN=https://${REPO_NAME}.surge.sh
surge --project ./dist --domain $DEPLOY_DOMAIN;
