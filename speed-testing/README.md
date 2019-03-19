### Usage

Python scripts for Greyfish upload and download speed testing  

Requirements:
	* python3
	* Libraries:
		* requests


#### Setup
Modify the python scripts with the server characteristics.  
Create a Greyfish user.

```bash
# Enter server IP, password
vi server_props.py

# Create an user
python3 create_greyfish_user.py
```


#### Testing

Test either upload and/or download of a file.  
Flags:
	-u/--upload: Upload
	-d/--download: Download
	-s/--size: File size in MB

Both *-u*/*-d* flags can be provided at the same time, this will test both cases.  
The program will return a string in the format *file size (MB), time* which can then be piped into a file.

