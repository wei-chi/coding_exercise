#!/usr/bin/env bash
./wait-for-it.sh db:3306 -- echo "db is ready"

flask db init
flask db migrate
flask db upgrade
nginx -g "daemon off;" | uwsgi --ini uwsgi.ini
