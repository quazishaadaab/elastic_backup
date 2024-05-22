"""
    subclass specific to logstash pipelines
"""

import os
from ..Snapshots.Snapshot import Snapshot


class LogstashSnapshot(Snapshot):
    """
        Logstash specific snapshot. for dev backup, set dev flag = True
    """

    def __init__(self, dev=False):
        # Get the config variable add append type:dev to it, so we can know if it is a prod or dev snapshotter
        self.config = self.retrieve_config(dev_env=dev)
        self.config.update({"type": dev})
        elastic_url = self.config['elastic_base_url'] + self.config['elastic_endpoint']
        gitlab_url = self.config['gitlab_base_url'] + self.config['gitlab_endpoint']
        Snapshot.__init__(self, elastic_url, gitlab_url)

    def parse_backup_data(self) -> None:
        """
            Parse the object returned by the api to be outputted to a file 
        """
        for pipeline_id, pipeline_metadata in self.backup_data.items():
            if not os.path.exists(self.config['gitlab_endpoint']):
                os.makedirs(self.config['gitlab_endpoint'])
            self.output_to_file(os.path.join(self.config['gitlab_endpoint'], f"{pipeline_id}.json"),
                                pipeline_metadata)
       
    def output_to_file(self, directory, data) -> None:
        """
            Takes a directory, data in dict format and will output it to a file 
        """
        if isinstance(data, dict):
            with open(directory, 'w+') as file:
                for key, value in data.items():
                    file.write(f"{key}:{value}\n")
                file.close()
        else:
            raise ValueError(f"Provided data is not of type dict, instead got type: {type(data)}")        