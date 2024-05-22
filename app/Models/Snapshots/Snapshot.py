""""
    Parent Class for the various elastic snapshot types.

    Classes:
        Snapshot
    Functions:
        elastic_url() -> string
        gitlab_url() -> string
        backup_data() -> list
        backup_data(list)
"""
import os
import validators
import yaml
from ..Snapshotter.GitlabSnapshotter import GitlabSnapshotter
from ..Snapshotter.ELKSnapshotter import ELKSnapshotter
import logging
from dotenv import load_dotenv

class Snapshot(GitlabSnapshotter, ELKSnapshotter):
    """"Parent class for all snapshot types"""
    load_dotenv()
    def __init__(self, elastic_url, gitlab_url):
        self.elastic_url = elastic_url
        self.gitlab_url = gitlab_url
        self.backup_data = {}
        GitlabSnapshotter.__init__(self)
        ELKSnapshotter.__init__(self)

    @property
    def elastic_url(self):
        """
        This is the elastic endpoint that will be called to retrieve the
        backup data.
        """
        return self._elastic_url

    @elastic_url.setter
    def elastic_url(self, url):
        if validators.url(url):
            self._elastic_url = url
        else:
            raise ValueError(f"Invalid url provided. url: {url}")

    @property
    def gitlab_url(self):
        """This is the gitlab project/submodule endpoint that the backup data will be pushed to"""
        return self._gitlab_url

    @gitlab_url.setter
    def gitlab_url(self, url):
        if validators.url(url):
            self._gitlab_url = url
        else:
            raise ValueError(f"Invalid url provided. url: {url}")

    @property
    def backup_data(self):
        """
            This is the backup data that is retrieved and subsequently pushed to gitlab. 
            The backup data is stored in a list.
        """
        return self._backup_data

    @backup_data.setter
    def backup_data(self, backup_data):
        if isinstance(backup_data, dict):
            self._backup_data = backup_data
        else:
            raise ValueError(
                f"expecting backupData to be of type List, instead got: {type(backup_data)}"
            )

    @property
    def config(self):
        """
        returns the config hash
        """
        return self._config

    @config.setter
    def config(self, config):
        """
            sets the config hash 
        """
        if isinstance(config, dict):
            self._config = config
        else:
            raise ValueError(
                f"expecting config data to be of type dict, instead got: {type(config)}"
            )

    def retrieve_config(self, dev_env) -> hash:
        """
            This method will be responsible for traversing and retrieving information
            stored within the Config directory specific to the calling sub class,
            Parent class(snapshot), prod/dev flag and will return a hash of all params
            in the yaml file.
        """
        path = "Config"
        env_path = "Dev" if dev_env is True else "Prod"
        snapshot_type = type(self).__name__.replace("Snapshot",".yaml")

        config_data = {}
        config_paths = [os.path.join("lib", path, env_path, "Snapshots", snapshot_type),
                       os.path.join("lib", path, env_path, "Snapshots", "Snapshot.yaml")]
        
        for config_path in config_paths:
            with open(config_path, 'r') as config_file:
                config_data.update(yaml.safe_load(config_file))

        config_data.update({"elk_api_token": os.getenv('elk_api_token')})
        config_data.update({"gitlab_api_token": os.getenv('gitlab_api_token')})

        # Log the config data that has been retrived
        logging.debug(config_data)
        return config_data

    def take_snapshot(self, body) -> None:
        """
            Takes the snapshot and stores it in the backup field
        """
        backup_data = ELKSnapshotter.take_snapshot(self, self.elastic_url, body)
        self.backup_data = backup_data

    def push_snapshot(self) -> None:
        """
            Pushes the snapshot data to gitlab submodule
        """
        GitlabSnapshotter.push_snapshot(self, self.gitlab_url, self.config['gitlab_endpoint'])   