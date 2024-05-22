"""
    Orchestrates taking a Snapshot for Elastic
    
    Classes:
        ELKSnapshotter
    Functions:
        get_elk_api_token()
        set_elk_api_token(token)
        take_snapshot(SnapShot)
"""

import requests
import json
import os
import logging
from requests.exceptions import ConnectionError
from ..Snapshotter.Snapshotter import Snapshotter
from dotenv import load_dotenv


class ELKSnapshotter(Snapshotter):
    """
        All functionality related to taking an ELK Snapshot 
    """
    def __init__(self) -> None:
        # Loads environment variables that were defined in the CI file.
        load_dotenv()
        # Conditional statement that checks if backup is for prod or dev.
        if (self.config['type'] == True):
            elk_api_token = os.getenv('elk_api_token_dev')
        elif (self.config['type'] == False):
            elk_api_token = os.getenv('elk_api_token')
        else:
            logging.debug("Need to include dev flag(true or false) to assign correct elk api token")
        Snapshotter.__init__(self, elk_api_token)

    @Snapshotter.api_token.getter
    def elk_api_token(self):
        """api token for authenticating with nbd elk"""
        return self.api_token

    @elk_api_token.setter
    def elk_api_token(self, token):
        self.api_token = token

    def take_snapshot(self, url, body) -> str:
        """
            Makes the api call gathers the info and then stores it in the Snapshot 
            instance
        """
        # Gets the certificate path from env variable
        bell_ca_cer = os.getenv("bell_ca_cer")
        
        if (body):
            #This is the bulk of the backup data which is the result of appending pagination results multiple times.
            load = {"hits": []}

            try:
                # First get max count of documents to backup,which is stored in max. We need this for our pagination, to set an end value.
                payload_temp = requests.get(url=url, verify=bell_ca_cer, headers={'Authorization': f"ApiKey {self.elk_api_token}"}, timeout=120)
                hits_temp = payload_temp.json()
                max = hits_temp["count"]
                # Loop through 20 new pages each time.
                for start in range(0, max, 20):
         
                    # Window goes from 0 -> next 100 documents , 20 -> next 100 documents , 40 -> next 100 documents ...etc
                    body = {
                        "from": start,
                        "size": 100
                    }
                # Get pagination results, and store it in payload1. This needs to be parsed.
                    payload1 = requests.get(url=url, json=body, verify=bell_ca_cer, headers={'Authorization': f"ApiKey {self.elk_api_token}"}, timeout=120)
                    logging.debug(type(payload1))
                # Parse the results and store it in hits.
                    hits = payload1.json()
                # Append flight of 20 backup data in load.
                    for data in hits["watches"]:
                        # Dictionaries being stored in an array
                        load["hits"].append(data)
            except ConnectionError:
                logging.debug("File Already Exists")
            return load
        else:
            try:
                payload = requests.get(url=url, verify=bell_ca_cer, headers={'Authorization': f"ApiKey {self.elk_api_token}"}, timeout=120)
                logging.debug(type(payload))
                return payload.json()
            except ConnectionError:
                logging.debug("File Already Exists")