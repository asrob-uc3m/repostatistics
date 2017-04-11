Repostatistics
----

A tool to extract useful contribution statistics from github repos.

# Dependencies
This project requires Python 3. The required libraries can be installed with pip:

    $ sudo pip3 install -r /path/to/requirements.txt
    
# Usage

1. Install dependencies
2. Copy the `website` folder to the target location
3. Run the repostatistics generator. For the asrob-uc3m organization, the command would be:
```
python3 repostatistics.py asrob-uc3m -a <access_token> -n ASROB -w http://asrob.uc3m.es -o path/to/website/index.html
```
