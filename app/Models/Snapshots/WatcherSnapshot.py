"""
    subclass specific to watchers
"""
import os
import json
from ..Snapshots.Snapshot import Snapshot
import logging


class WatcherSnapshot(Snapshot):
    """
        Watcher specific snapshot
    """
    def __init__(self, dev=False):
        # Get the config variable add append type:dev to it, so we can know if it is a prod or dev snapshotter
        self.config = self.retrieve_config(dev_env=dev)
        self.config.update({"type": dev})
        elastic_url = self.config['elastic_base_url'] + self.config['elastic_endpoint']
        gitlab_url = self.config['gitlab_base_url'] + self.config['gitlab_endpoint']
        Snapshot.__init__(self, elastic_url, gitlab_url)  

    def parse_backup_data(self) -> str:
        """
            Makes the api call gathers the info and then stores it in the Snapshot 
            instance
        """      
        # Gets a finite amount of backup data (100) and then parse it. Move on to the next 100. (Pagination)
        self.take_snapshot(body=True)
        self.output_to_file()
    
    def output_to_file(self) -> None:
        """
        Parse the object returned by the api to be outputted to a file
        Takes in backup data and outputs it to a file. All files are then put in a directory.
        """
        # Retrives total payload of watchers
        bucket = self.backup_data['hits']
        # Creates a new folder called watcher-backup to store all the backup data
        path = self.config['gitlab_endpoint']
        if not os.path.exists(path):
            os.makedirs(path)
        # Loops through each watcher object in bucket
        for watcher in bucket:
            #Create a new file with name as watcher id and populate the file with the watcher's config data. Store file in the folder that was just created.
            try:
                with open(os.path.join(path, watcher["_id"] + ".json"),'x') as file:
                    file.write(json.dumps(watcher, indent=2))
            except FileExistsError:
                logging.debug("File Already Exists")