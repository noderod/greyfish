### Distributed Greyfish

--------------

#### Installation (distributed)

Pull this directory and modify environmental variables:
```bash
git clone https://github.com/noderod/greyfish
cd greyfish/cloud-distributed/manager-node

# Change the greyfish, Redis, InfluxDB credentials and other environmental variables
vi .env.yml
```

Obtain a certificate file (*.crt*) and private key (*.key*), make sure they are named *certfile.crt* and *keyfile.key*, respectively.  
If none are available, execute the following commands and answer the prompts as appropriate:
```bash
# Based on https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
# Creates a certificate valid for 365 days
openssl req -newkey rsa:2048 -nodes -keyout keyfile.key -x509 -days 365 -out certfile.crt
```

Start manager node:
```bash
docker-compose up -d
```

To rebuild greyfish after changes in the code:
```bash
# Bring down the containers
docker-compose down
# Build and start containers
docker-compose up -d --build
```



#### Instructions (distributed)

To activate or switch off the APIs, enter the docker container and do:  

```bash
# Enter container
docker exec -it managernode_greyfish_1 bash
cd /grey
# Start the needed databases and assign permission (APIs will not be started)
/grey/setup.sh
# Activate (change the number of threads if needed, standard is 4)
./API_Daemon.sh -up
# Deactivate
./API_Daemon.sh -down
```

Note: deactivating the APIs will not change or delete any data, it will simply no longer be able to accept communications from outside.



#### Data Persistance (distributed)



#### Usage (distributed)

The Greyfish APIs can be called from any system as long as the greyfish key is known.  
Note that, if creating a private key and certicate (as described above), the *--insecure* flag may be required for the *curl* commands.


```bash
gk=$Greyfish_Key # Set up in the docker-compose.yml
SERVER_IP=$URL_or_IP # Without ports or /
# Create a new user
curl -X POST -H "Content-Type: application/json" -d '{"gkey":"'"$gk"'", "user_id":"'"$USER_ID"'"}' \
	https://$SERVER_IP:2443/grey/create_user
# Delete a user
curl -X POST -H "Content-Type: application/json" -d '{"gkey":"'"$gk"'", "user_id":"'"$USER_ID"'"}' \
	https://$SERVER_IP:2443/grey/delete_user
```


#### Acknowledgements

All current Greyfish servers used for testing are setup using the Jetstream \[1\]\[2\] and Chameleon\[3\] systems. We are grateful to XSEDE for providing the allocation required for implementing this project. This project is generously supported through the National Science Foundation (NSF) award \#1664022.  




#### References

\[1\] Stewart, C.A., Cockerill, T.M., Foster, I., Hancock, D., Merchant, N., Skidmore, E., Stanzione, D., Taylor, J., Tuecke, S., Turner, G., Vaughn, M., and Gaffney, N.I., Jetstream: a self-provisioned, scalable science and engineering cloud environment. 2015, In Proceedings of the 2015 XSEDE Conference: Scientific Advancements Enabled by Enhanced Cyberinfrastructure. St. Louis, Missouri.  ACM: 2792774.  p. 1-8. http://dx.doi.org/10.1145/2792745.2792774 


\[2\] John Towns, Timothy Cockerill, Maytal Dahan, Ian Foster, Kelly Gaither, Andrew Grimshaw, Victor Hazlewood, Scott Lathrop, Dave Lifka, Gregory D. Peterson, Ralph Roskies, J. Ray Scott, Nancy Wilkins-Diehr, "XSEDE: Accelerating Scientific Discovery", Computing in Science & Engineering, vol.16, no. 5, pp. 62-74, Sept.-Oct. 2014, doi:10.1109/MCSE.2014.80


\[3\] Chameleon: a Scalable Production Testbed for Computer Science Research, K. Keahey, P. Riteau, D. Stanzione, T. Cockerill, J. Mambretti, P. Rad, P. Ruth,	book chapter in "Contemporary High Performance Computing: From Petascale toward Exascale, Volume 3",  Jeffrey Vetter ed., 2017 

