"""testing the snapshot class"""
import os
import pytest
import yaml
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.Models.Snapshots.Snapshot import Snapshot
from app.Models.Snapshots.LogstashSnapshot import LogstashSnapshot

os.chdir("..")


def create_snapshot_instance():
    """creates an instance of Snapshot class for testing. By calling the LogstashSnapshot method,
        we automatically retrive its elastic url and gitlab url since it inherits ELKSnapshotter and Gitlab Snapshotter.
    """

    return LogstashSnapshot()


def test_get_elastic_url():
    """tests the get_elastic_url method"""
    snapshot = create_snapshot_instance()
    assert snapshot.config["elastic_base_url"] == "https://esearch.nbd.int.bell.ca/tv/"


def test_set_elastic_url_with_valid_url():
    """tests the set_elastic_url method with a valid"""
    snapshot = create_snapshot_instance()
    snapshot.elastic_url = "https://www.google.com/"
    assert snapshot.elastic_url == "https://www.google.com/"


def test_set_elastic_url_with_invalid_url():
    """tests the set_elastic_url method with a invalid expecting a ValueError"""
    snapshot = create_snapshot_instance()
    with pytest.raises(ValueError):
        snapshot.elastic_url = "testing123"


def test_get_gitlab_url():
    """tests the get_gitlab_url method"""
    snapshot = create_snapshot_instance()
    assert snapshot.config["gitlab_base_url"] == "https://gitlab.int.bell.ca/"


def test_set_gitlab_url_with_valid_url():
    """tests the set_gitlab_url method with a valid"""
    snapshot = create_snapshot_instance()
    snapshot.gitlab_url = "https://www.google.com/"
    assert snapshot.gitlab_url == "https://www.google.com/"


def test_set_gitlab_url_with_invalid_url():
    """tests the set_gitlab_url method with a invalid expecting a ValueError"""
    snapshot = create_snapshot_instance()
    with pytest.raises(ValueError) as e_info:
        snapshot.gitlab_url = "testing123"


def test_get_backup_data():
    """tests backup_data getter method"""
    snapshot = create_snapshot_instance()
    assert isinstance(snapshot.backup_data, dict)
    assert snapshot.backup_data == {}


def test_set_backup_data_with_valid_data():
    """tests set_backup_data with valid data"""
    snapshot = create_snapshot_instance()
    backup_data = {"a": "testing 123"}
    snapshot.backup_data = backup_data
    assert snapshot.backup_data == backup_data


def test_set_backup_data_with_invalid_data():
    """tests set_backup_data with invalid data expecting a ValueError"""
    snapshot = create_snapshot_instance()
    invalid_backup_data = "testing 123"
    with pytest.raises(ValueError) as e_info:
        snapshot.backup_data = invalid_backup_data


def test_retrieve_dev_logstash_config():
    """tests retrieve_config for dev data"""

    logstash_snapshot = LogstashSnapshot(dev=True)
    expected_params = {}
    print(os.getcwd())
    base_dir = os.getcwd()
    lgst_yml_path = os.path.join(base_dir, 'lib', 'Config', 'Dev', 'Snapshots', 'Logstash.yaml')
    snapshot_yml_path = os.path.join(base_dir, 'lib', 'Config', 'Dev', 'Snapshots', 'Snapshot.yaml')
    with open(lgst_yml_path, 'r') as yaml_file:
        expected_params.update(yaml.safe_load(yaml_file))
    with open(snapshot_yml_path, 'r') as yaml_file:
        expected_params.update(yaml.safe_load(yaml_file))
    expected_params.update({"elk_api_token": os.getenv('elk_api_token')})
    expected_params.update({"gitlab_api_token": os.getenv('gitlab_api_token')})

    params = Snapshot.retrieve_config(logstash_snapshot, True)
    assert isinstance(params, dict) and params == expected_params


def test_retrieve_prod_logstash_config():
    """
        tests retrieve_config for prod data, the expected_params must match the
        Config for the class that is calling the retrieve data method.
    """
    logstash_snapshot = LogstashSnapshot()
    expected_params = {}
    base_dir = os.getcwd()
    lgst_yml_path = os.path.join(base_dir, 'lib', 'Config', 'Prod', 'Snapshots', 'Logstash.yaml')
    snapshot_yml_path = os.path.join(base_dir, 'lib', 'Config', 'Prod', 'Snapshots', 'Snapshot.yaml')
    with open(lgst_yml_path, 'r') as yaml_file:
        expected_params.update(yaml.safe_load(yaml_file))
    with open(snapshot_yml_path, 'r') as yaml_file:
        expected_params.update(yaml.safe_load(yaml_file))
    expected_params.update({"elk_api_token": os.getenv('elk_api_token')})
    expected_params.update({"gitlab_api_token": os.getenv('gitlab_api_token')})
    params = Snapshot.retrieve_config(logstash_snapshot, False)
    assert isinstance(params, dict) and params == expected_params

