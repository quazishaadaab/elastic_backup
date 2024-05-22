"""
    subclass specific to Index Templates
"""
import os
import json
from ..Snapshots.Snapshot import Snapshot
import logging


class IndexTemplateSnapshot(Snapshot):
    """
        Index Template specific snapshot 
    """
    def __init__(self, dev=False):
        # Get the config variable add append type:dev to it, so we can know if it is a prod or dev snapshotter
        self.config = self.retrieve_config(dev_env=dev)
        self.config.update({"type": dev})

        elastic_url = self.config['elastic_base_url'] + self.config['index_template_endpoint']
        gitlab_url = self.config['gitlab_base_url'] + self.config['gitlab_endpoint']
        Snapshot.__init__(self, elastic_url, gitlab_url)

    def parse_backup_data(self) -> str:
        """
            Makes the api call gathers the info and then stores it in the
            Snapshot instance
        """
        bucket = self.backup_data["index_templates"]

        # Call parsing function and parse that finite amount. This will also 
        # output to a file in a directory.
        self.output_to_file(bucket)        
    
    def output_to_file(self, payload) -> None:
        """
        Parse the object returned by the api to be outputted to a file
        Takes in backupdata file and outputs it to a file. All files are then 
        put in a directory.
        """
        # Creates a new folder called IndexTemplates to store all the backup
        # data

        path = self.config['gitlab_endpoint']
        if not os.path.exists(path):
            os.makedirs(path)
        # Loops through each watcher object in bucket
        for index_template in payload:
            # Write to file and store it in the directory just made
            try:
                with open(os.path.join(path, index_template["name"] + ".json"),'x') as file:
                    file.write(json.dumps(index_template["index_template"], indent=2))
            except FileExistsError:
                logging.debug("File Already Exists")  