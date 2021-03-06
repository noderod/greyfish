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
   printf "\n All APIs will be started with 4 workers, modify this file if more workers are required\n"
   exit 1
fi


if [ $1 == "-up" ]; then 
  gunicorn -w $greyfish_threads --certfile=certfile.crt --keyfile=keyfile.key -b 0.0.0.0:2443 traffic:app &
  printf "Greyfish APIs are now active\n"
fi


if [ $1 == "-down" ]; then 
   
   pkill gunicorn

   printf "Greyfish APIs have been disconnected\n"
fi
