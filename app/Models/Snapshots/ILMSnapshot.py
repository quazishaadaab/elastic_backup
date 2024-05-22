"""
    Sublass specific to Index Lifecycles
"""
import os
import json
from ..Snapshots.Snapshot import Snapshot
import logging


class ILMSnapshot(Snapshot):
    """
        ILM specific snapshot 
    """
    def __init__(self, dev=False):
        # Get the config variable add append type:dev to it, so we can know if it is a prod or dev snapshotter
        self.config = self.retrieve_config(dev_env=dev)
        self.config.update({"type": dev})

        elastic_url = self.config['elastic_base_url'] + self.config['ilm_endpoint']
        gitlab_url = self.config['gitlab_base_url'] + self.config['gitlab_endpoint']
        Snapshot.__init__(self, elastic_url, gitlab_url)  

    def parse_backup_data(self) -> str:
        """
            Makes the api call gathers the info and then stores it in the
            Snapshot instance.Call parsing function and parse that finite amount. This will also
            output to a file in a directory.
        """
        self.output_to_file(self.backup_data)        

    def output_to_file(self, payload) -> None:
        """
        Parse the object returned by the api to be outputted to a file
        Takes in backupdata file and outputs it to a file. All files are then
        put in a directory.Creates a new folder called ILM that stores all of our backup files (if 
        directory doesnt exist already)
        """
        path = self.config['gitlab_endpoint']
        if not os.path.exists(path):
            os.makedirs(path)
        # Traverses through each ILM object in the payload. ( Objects contain 
        # name of the ILM and config data of the ILM)
        for index_lifecycle in payload:         
            # Creates a new file for each ILM ( file name is the ILM name) and
            # populates it with its config data
            try:
                with open(os.path.join(path, index_lifecycle + ".json"), 'x') as file:
                    file.write(json.dumps(payload[index_lifecycle], indent=2))
            except FileExistsError:
                logging.debug("File Already Exists")