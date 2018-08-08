### Portable, transferrable cloud storage

Greyfish is an out of the box, simple cloud storage framework.  
It will store files and directories without changes on the go.  
All your files will remain protected and visible only to you. 



#### Installation

Pocket Reef is designed as a complement to a BOINC server, although it can also be used to store personal data.  


**Instructions**  
* Clone this current directory
* Change directory
* Change the greyfish key (recommended)
* Set up the docker compose

```bash
	git clone https://github.com/noderod/greyfish
	cd greyfish
	# Change the Reef key (recommended)
	vi docker-compose.yml
	docker-compose up -d
```

**Usage**  
To activate or switch off the APIs, enter the docker container and do:  

```bash
	# Enter container
	docker exec -it $CONTAINER bash
	cd /reef
	# Activate
	./API_Daemon.sh -up
	# Deactivate
	./API_Daemon.sh -down
```

Note: deactivating the APIs will not change or delete any data, it will simply no longer be able to accept communications from outside.
