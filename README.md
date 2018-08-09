### Portable, transferrable cloud storage

Greyfish is an out of the box, simple cloud storage framework.  
It will store files and directories without changes on the go.  
All your files will remain protected and visible only to you. 



#### Installation

Pocket Reef is designed as a complement to a BOINC server, although it can also be used to store personal data.  


**Instructions**  
* Clone this current directory
* Change directory
* Change the greyfish key (recommended) and influxdb password setup
* Enter the URL or IP of the machine without http:// (i.e. google.com instead of http://google.com/)
* Set up the docker compose

```bash
	git clone https://github.com/noderod/greyfish
	cd greyfish
	# Change the Greyfish key (recommended)
	vi docker-compose.yml
	# Change the influxdb log credentials and the URL/IP
	vi credentials.yml
	docker-compose up -d

	docker exec -it $influxdb_container bash
	influxdb /init-influxdb.sh
```

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


#### Usage 

The Greyfish APIs can be called from any system as long as the greyfish key is known.  


```bash
	
	gk=$Greyfish_Key # Set up in the docker-compose.yml

	# Create a new user
	curl http://$SERVER_IP:2003/grey/create_user/$gk/$USER_ID
	# Deelte a user
	curl http://$SERVER_IP:2003/grey/delete_user/$gk/$USER_ID


	# Get a JSON object of all user files
	curl http://$SERVER_IP:2000/grey/all_user_files/$gk/$USER_ID
	curl http://$SERVER_IP:2001/grey/all_user_files/$gk/$USER_ID

	# Get contents of an entire directory in JSON (using ++ instead of / for paths)
	curl http://$SERVER_IP:2000/grey/user_files/$gk/$USER_ID/PATH++TO++DIR
	# Upload one file (will create the directory if needed
	curl -F file=@$LOCAL_PATH_TO_FILE http://$SERVER_IP:2000/grey/upload/$gk/$USER_ID/PATH++TO++DIR
	# Deletes a file
	curl http://$SERVER_IP:2000/grey/delete_file/$gk/$USER_ID/$FILENAME/PATH++TO++DIR
	# Returns a file
	curl http://$SERVER_IP:2000/grey/grey/$gk/$USER_ID/$FILENAME/PATH++TO++DIR
	# Uploads a directory (must be compressed into .tgz or .tar.gz), if it already exists, it substitutes all files inside
	curl -F file=@$LOCAL_PATH_TO_TAR http://$SERVER_IP:2000/grey/upload_dir/$gk/$USER_ID/PATH++TO++DIR
	# Dowloads a directory as a .tar.gz file
	curl http://$SERVER_IP:2000/grey/grey_dir/$gk/$USER_ID/$FILENAME/PATH++TO++DIR

	# Gets all the data currently in the user directory
	curl http://$SERVER_IP:2001/grey/get_all/$gk/$USER_ID
	# Replaces all current data
	curl -F file=@$TARRED_CONTENT  http://$SERVER_IP:2002/grey/push_all/$gk/$USER_ID


``` 

