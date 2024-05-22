"""
    Orchestrates pushing a Snapshot to gitlab
    
    Classes:
        GitlabSnapshotter
    Functions:
        get_gitlab_api_token()
        set_gitlab_api_token(token)
        push_snapshot(Snapshot)
"""

import os
import logging
from .Snapshotter import Snapshotter
from dotenv import load_dotenv


class GitlabSnapshotter(Snapshotter):
    """
        All functionality related to pushing a snapshot to gitlab
    """
    def __init__(self) -> None:
        # Load environment variables defined in the CI file.
        load_dotenv()
        gitlab_api_token = os.getenv('gitlab_api_token')
        Snapshotter.__init__(self, gitlab_api_token)

    @Snapshotter.api_token.getter
    def gitlab_api_token(self):
        """api token for authenticating with gitlab"""
        return self.api_token

    @gitlab_api_token.setter
    def gitlab_api_token(self, token):
        self.api_token = token

    def push_snapshot(self, url, submodule_directory):
        """
            Pushes the snapshot to its respective gitlab endpoint
            https://stackoverflow.com/questions/56921192/how-to-place-a-created-file-in-an-existed-gitlab-repository-through-python
        """

        # This will log which directory we are in so the github commands work properly in the correct folder
        logging.debug(submodule_directory)
        os.chdir(submodule_directory)

        os.popen(f'{"git init"}').read()
        os.popen(f"git config --global user.email {os.getenv('git_email')} ").read()
        os.popen(f"git config --global user.name {os.getenv('git_username')} ").read()
        os.popen(f"git pull {self.config['gitlab_push_url']}").read()
        os.popen(f"git checkout -b {self.config['gitlab_branch']}").read()
        os.popen(f'{"git add -A"}').read()
        os.popen(f'git commit -m "{"daily back up"}"').read()
        os.popen(f"git push https://oauth2:{self.config['gitlab_api_token']}@{self.config['gitlab_push_url']} {self.config['gitlab_branch']} -f").read()
        os.chdir("..")
