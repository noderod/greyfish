#!/bin/bash


# Creates the databases:
#  | -greyfish:  Contains all greyfish data
#  | -user_data: Only refers to those users and the time of signing up or deleting their accounts
#  | -common:    Generic file/dir uploads and downloads
#  | -deletes:   Deleted file/dir
#  | -overhaul:  Only covers users who have completely updated their repo using the appropriate command

curl -G http://localhost:8086/query -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_USER_PASSWORD --data-urlencode "q=CREATE DATABASE greyfish"
curl -G http://localhost:8086/query -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_USER_PASSWORD --data-urlencode "q=CREATE DATABASE user_data"
curl -G http://localhost:8086/query -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_USER_PASSWORD --data-urlencode "q=CREATE DATABASE common"
curl -G http://localhost:8086/query -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_USER_PASSWORD --data-urlencode "q=CREATE DATABASE deletes"
curl -G http://localhost:8086/query -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_USER_PASSWORD --data-urlencode "q=CREATE DATABASE overhaul"

/grey/API_Daemon.sh -up

# Deletes itself
rm -- "$0"