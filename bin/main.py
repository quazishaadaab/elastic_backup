import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.Models.Snapshots.LogstashSnapshot import LogstashSnapshot
from app.Models.Snapshots.WatcherSnapshot import WatcherSnapshot
from app.Models.Snapshots.ILMSnapshot import ILMSnapshot
from app.Models.Snapshots.IndexTemplateSnapshot import IndexTemplateSnapshot
from app.Models.Snapshots.LegacyTemplateSnapshot import LegacyIndexTemplateSnapshot


os.chdir("..")

logstash_snapshot_prod = LogstashSnapshot()
logstash_snapshot_prod.take_snapshot(body=None)
logstash_snapshot_prod.parse_backup_data()
logstash_snapshot_prod.push_snapshot()

watcher_snapshot_prod = WatcherSnapshot()
watcher_snapshot_prod.take_snapshot(body=None)
watcher_snapshot_prod.parse_backup_data()
watcher_snapshot_prod.push_snapshot()

ilm_snapshot_prod = ILMSnapshot()
ilm_snapshot_prod.take_snapshot(body=None)
ilm_snapshot_prod.parse_backup_data()
ilm_snapshot_prod.push_snapshot()

index_template_snapshot_prod = IndexTemplateSnapshot()
index_template_snapshot_prod.take_snapshot(body=None)
index_template_snapshot_prod.parse_backup_data()
index_template_snapshot_prod.push_snapshot()

legacy_index_template_snapshot_prod = LegacyIndexTemplateSnapshot()
legacy_index_template_snapshot_prod.take_snapshot(body=None)
legacy_index_template_snapshot_prod.parse_backup_data()
legacy_index_template_snapshot_prod.push_snapshot()

logstash_snapshot_dev = LogstashSnapshot(dev=True)
logstash_snapshot_dev.take_snapshot(body=None)
logstash_snapshot_dev.parse_backup_data()
logstash_snapshot_dev.push_snapshot()

watcher_snapshot_dev = WatcherSnapshot(dev=True)
watcher_snapshot_dev.take_snapshot(body=None)
watcher_snapshot_dev.parse_backup_data()
watcher_snapshot_dev.push_snapshot()

ilm_snapshot_dev = ILMSnapshot(dev=True)
ilm_snapshot_dev.take_snapshot(body=None)
ilm_snapshot_dev.parse_backup_data()
ilm_snapshot_dev.push_snapshot()

index_template_snapshot_dev = IndexTemplateSnapshot(dev=True)
index_template_snapshot_dev.take_snapshot(body=None)
index_template_snapshot_dev.parse_backup_data()
index_template_snapshot_dev.push_snapshot()

legacy_index_template_snapshot_dev = LegacyIndexTemplateSnapshot(dev=True)
legacy_index_template_snapshot_dev.take_snapshot(body=None)
legacy_index_template_snapshot_dev.parse_backup_data()
legacy_index_template_snapshot_dev.push_snapshot()
