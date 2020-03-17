##########################
# BASICS
# 
# A Debian server with python3 installed, useful only as a cloud storage server
# Not designed for front-end interfaces
#########################

FROM python:3.8.2-buster


# Copies the necessary files
COPY certfile.crt       /grey/certfile.crt
COPY keyfile.key        /grey/keyfile.key
COPY setup.sh           /grey/setup.sh
COPY traffic.py         /grey/traffic.py

# Individual key used to attach node or to give it instructions
ENV NODE_KEY
# Similar to that of the manager node
ENV REDIS_AUTH
# Similar to that of the manager node
ENV orchestra_key
# Similar to that of the manager node
ENV URL_BASE
# Filesystem where all data will stored. For example: /dev/sda1
ENV FILESYSTEM
# Maximum total storage allowed for users in KB, must be a positive integer
ENV MAX_STORAGE




# Installs the necessary packages
# Bash for convenience
RUN mkdir -p /greyfish/sandbox &&\
    pip3 install gunicorn Flask redis requests &&\
    chmod +x /grey/API_Daemon.sh /grey/setup.sh /grey/traffic.py


WORKDIR /greyfish
