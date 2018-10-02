#!/bin/bash


# Creates the databases:
#  | -greyfish:  Contains all greyfish data
#  | -user_data: Only refers to those users and the time of signing up or deleting their accounts
#  | -common:    Generic file/dir uploads and downloads
#  | -deletes:   Deleted file/dir
#  | -overhaul:  Only covers users who have completely updated their repo using the appropriate command

curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "greyfish"'
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "user_data"'
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "common"'
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "deletes"'
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "overhaul"'
printf "Created InfluxDB databases\n"

rm -- "$0"
