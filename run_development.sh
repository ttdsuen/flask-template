#!/bin/sh

if [ ! -d venv ]; then
    python3 -m venv venv
    . venv/bin/activate
fi

[ ! -d logs ] && mkdir logs

export FLASK_APP=app
export FLASK_ENV=development
flask run
