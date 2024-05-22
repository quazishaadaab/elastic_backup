"""
    Orchestrates taking or pushing a Snapshot depending on the child class
    
    Classes:
        Snapshotter
    Functions:
        get_api_token()
        set_api_token(token)
"""


class Snapshotter():
    """
        Takes the snapshot for the various Snapshot types and stores the results in
        the Snapshot instance
    """
    def __init__(self, api_token) -> None:
        #TODO: bell_cert
        self._api_token = api_token

    @property
    def api_token(self) -> str:
        """api token for authentication"""
        return self._api_token

    @api_token.setter
    def api_token(self, api_token) -> None:
        self._api_token = api_token