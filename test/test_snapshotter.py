from app.Models.Snapshots.LogstashSnapshot import LogstashSnapshot


def test_getting_elk_snapshot():
    """ tests getting a snapshot from the elk env"""
    lgst_snapshot = LogstashSnapshot()
    assert lgst_snapshot.take_snapshot(body=None) is None