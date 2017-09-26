#!/bin/bash

redis-server&
service mongodb start
service nginx start
uwsgi --ini /safer-tags/deploy/uwsgi.ini&
