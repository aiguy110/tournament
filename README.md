# Overview
A small web app for running pool tournaments in the Florida Polytechnic dorms.

## Requirements
* Python 3.4+ (might work with older versions as well)
* Flask (python package)

  If you have never used the Flask package before, you can install it with

      python3 -m pip install Flask

(If you do not have access to the python3 command from your command line, refer to [this link for Windows](https://superuser.com/questions/143119/how-to-add-python-to-the-windows-path)),
or on Linux Debian run `sudo apt install python3 python3-pip` to get Python 3 and pip)

## Usage
1. Change the contents of **players.txt** to contain the players in your tournament.
2. In the root folder of this project, run `python3 server.py`.
3. Visit http://localhost:5000 in any web browser running on the same computer as the server.  
