#!/bin/bash


# Starts or ends the Reef communication APIs


if [ $# -eq 0 ]; then
   printf "No arguments provided, use -h flag for help\n"
   exit 1
fi


if [ $1 == "-h" ]; then
   printf "Automatic API daemon set-up\n"
   printf "Use flag -up to set-up the APIs\n"
   printf "Use flag -down to cancel the APIs\n"
   print "\n All APIs will be started with 4 workers, modify this file if more workers are required\n"
   exit 1
fi


if [ $1 == "-up" ]; then 
  gunicorn -w 4 -b 127.0.0.1:2000 grey_regular:grey_regular &
  gunicorn -w 4 -b 127.0.0.1:2001 gget_all:grey_getall &
  gunicorn -w 4 -b 127.0.0.1:2002 push_all:grey_pushall &
  gunicorn -w 4 -b 127.0.0.1:2003 new_user:grey_nu &


   printf "Greyfish APIs are now active\n"
fi


if [ $1 == "-down" ]; then 
   
   pkill gunicorn

   printf "Greyfish APIs have been disconnected\n"
fi
