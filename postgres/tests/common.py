# (C) Datadog, Inc. 2010-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import os
from sys import maxsize

import pytest

from datadog_checks.base.stubs.aggregator import normalize_tags
from datadog_checks.dev import get_docker_hostname
from datadog_checks.dev.docker import get_container_ip
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.postgres.util import (
    CHECKSUM_METRICS,
    NEWER_14_METRICS,
    QUERY_PG_CONTROL_CHECKPOINT,
    QUERY_PG_REPLICATION_SLOTS,
    QUERY_PG_REPLICATION_SLOTS_STATS,
    QUERY_PG_REPLICATION_STATS_METRICS,
    QUERY_PG_STAT_RECOVERY_PREFETCH,
    QUERY_PG_STAT_WAL_RECEIVER,
    QUERY_PG_UPTIME,
    QUERY_PG_WAIT_EVENT_METRICS,
    SLRU_METRICS,
    SNAPSHOT_TXID_METRICS,
    STAT_IO_METRICS,
    STAT_SUBSCRIPTION_METRICS,
    STAT_SUBSCRIPTION_STATS_METRICS,
    STAT_WAL_METRICS,
    SUBSCRIPTION_STATE_METRICS,
    WAL_FILE_METRICS,
)
from datadog_checks.postgres.version_utils import VersionUtils

HOST = get_docker_hostname()
PORT = '5432'
PORT_REPLICA = '5433'
PORT_REPLICA2 = '5434'
PORT_REPLICA_LOGICAL = '5435'
USER = 'datadog'
USER_ADMIN = 'dd_admin'
PASSWORD = 'datadog'
PASSWORD_ADMIN = 'dd_admin'
DB_NAME = 'datadog_test'
POSTGRES_VERSION = os.environ.get('POSTGRES_VERSION', None)
POSTGRES_IMAGE = "alpine"
POSTGRES_LOCALE = os.environ.get('POSTGRES_LOCALE', "UTF8")

REPLICA_CONTAINER_1_NAME = 'compose-postgres_replica-1'
REPLICA_CONTAINER_2_NAME = 'compose-postgres_replica2-1'
REPLICA_LOGICAL_1_NAME = 'compose-postgres_logical_replica-1'
USING_LATEST = False

if POSTGRES_VERSION is not None:
    USING_LATEST = POSTGRES_VERSION.endswith('latest')
    POSTGRES_IMAGE = POSTGRES_VERSION + "-alpine"

if USING_LATEST is True:
    POSTGRES_VERSION = str(maxsize)
    POSTGRES_IMAGE = "alpine"

SCHEMA_NAME = 'schemaname'

COMMON_METRICS = [
    'postgresql.before_xid_wraparound',
    'postgresql.commits',
    'postgresql.rollbacks',
    'postgresql.disk_read',
    'postgresql.buffer_hit',
    'postgresql.rows_returned',
    'postgresql.rows_fetched',
    'postgresql.rows_inserted',
    'postgresql.rows_updated',
    'postgresql.rows_deleted',
    'postgresql.database_size',
    'postgresql.deadlocks',
    'postgresql.deadlocks.count',
    'postgresql.temp_bytes',
    'postgresql.temp_files',
    'postgresql.blk_read_time',
    'postgresql.blk_write_time',
]

DBM_MIGRATED_METRICS = [
    'postgresql.connections',
]

CONFLICT_METRICS = [
    'postgresql.conflicts.tablespace',
    'postgresql.conflicts.lock',
    'postgresql.conflicts.snapshot',
    'postgresql.conflicts.bufferpin',
    'postgresql.conflicts.deadlock',
]

COMMON_BGW_METRICS = [
    'postgresql.bgwriter.checkpoints_timed',
    'postgresql.bgwriter.checkpoints_requested',
    'postgresql.bgwriter.buffers_checkpoint',
    'postgresql.bgwriter.buffers_clean',
    'postgresql.bgwriter.maxwritten_clean',
    'postgresql.bgwriter.buffers_alloc',
    'postgresql.bgwriter.write_time',
    'postgresql.bgwriter.sync_time',
]

COMMON_BGW_METRICS_PG_ABOVE_94 = ['postgresql.archiver.archived_count', 'postgresql.archiver.failed_count']
COMMON_BGW_METRICS_PG_BELOW_17 = ['postgresql.bgwriter.buffers_backend', 'postgresql.bgwriter.buffers_backend_fsync']
CONNECTION_METRICS = ['postgresql.max_connections', 'postgresql.percent_usage_connections']
CONNECTION_METRICS_DB = ['postgresql.connections']
COMMON_DBS = ['dogs', 'postgres', 'dogs_nofunc', 'dogs_noschema', DB_NAME]

CHECK_PERFORMANCE_METRICS = [
    'archiver_metrics',
    'bgw_metrics',
    'connections_metrics',
    'count_metrics',
    'instance_metrics',
    'replication_metrics',
    'replication_stats_metrics',
    'slru_metrics',
]

requires_static_version = pytest.mark.skipif(USING_LATEST, reason='Version `latest` is ever-changing, skipping')


def _iterate_metric_name(query):
    metric_prefix = 'postgresql'
    if 'columns' in query:
        if 'metric_prefix' in query:
            metric_prefix = f'{query["metric_prefix"]}'
        for column in query['columns']:
            if column['type'].startswith('tag'):
                continue
            yield f'{metric_prefix}.{column["name"]}'
    else:
        metrics = query['metrics'].values() if 'metrics' in query else query.values()
        for metric in metrics:
            yield f'{metric_prefix}.{metric[0]}'


def _get_expected_replication_tags(check, pg_instance, with_host=True, with_db=False, with_version=True, **kwargs):
    return _get_expected_tags(
        check, pg_instance, with_host=with_host, with_db=with_db, with_version=with_version, role='standby', **kwargs
    )


def _get_expected_tags(
    check,
    pg_instance,
    with_host=True,
    with_db=False,
    with_version=True,
    with_sys_id=True,
    with_cluster_name=True,
    role='master',
    **kwargs,
):
    base_tags = (
        pg_instance['tags']
        + [f'port:{pg_instance["port"]}']
        + [f'database_hostname:{check.database_hostname}', f'database_instance:{check.database_identifier}']
    )
    if role:
        base_tags.append(f'replication_role:{role}')
    if with_db:
        base_tags.append(f'db:{pg_instance["dbname"]}')
    if with_host:
        base_tags.append(f'dd.internal.resource:database_instance:{check.database_identifier}')
    if with_cluster_name and check.cluster_name:
        base_tags.append(f'postgresql_cluster_name:{check.cluster_name}')
    if with_sys_id and check.system_identifier:
        base_tags.append(f'system_identifier:{check.system_identifier}')
    if with_version and check.raw_version:
        base_tags.append(f'postgresql_version:{check.raw_version}')
    for k, v in kwargs.items():
        base_tags.append(f'{k}:{v}')
    return base_tags


def assert_metric_at_least(
    aggregator,
    metric_name,
    lower_bound=None,
    higher_bound=None,
    count=None,
    tags=None,
    min_count=None,
    max_count=None,
):
    found_values = 0
    expected_tags = normalize_tags(tags, sort=True)
    aggregator.assert_metric(metric_name, count=count, tags=expected_tags)
    for metric in aggregator.metrics(metric_name):
        if expected_tags and expected_tags == sorted(metric.tags):
            if lower_bound is not None:
                assert metric.value >= lower_bound, (
                    f'Expected {metric_name} with tags {expected_tags} to have a value >= {lower_bound}, '
                    f'got {metric.value}'
                )
            if higher_bound is not None:
                assert metric.value <= higher_bound, (
                    f'Expected {metric_name} with tags {expected_tags} to have a value <= {higher_bound}, '
                    f'got {metric.value}'
                )
            found_values += 1

    if count:
        assert found_values == count, (
            f'Expected to have {count} with tags {expected_tags} values for metric {metric_name}, got {found_values}'
        )
    if min_count:
        assert found_values >= min_count, (
            f'Expected to have at least {min_count} with tags {expected_tags} values for metric {metric_name},'
            f' got {found_values}'
        )
    if max_count:
        assert found_values <= max_count, (
            f'Expected to have at most {max_count} with tags {expected_tags} values for metric {metric_name},'
            f' got {found_values}'
        )


def check_common_metrics(aggregator, expected_tags, count=1):
    for db in COMMON_DBS:
        db_tags = expected_tags + ['db:{}'.format(db)]
        for name in COMMON_METRICS:
            aggregator.assert_metric(name, count=count, tags=db_tags)
        if POSTGRES_VERSION is None or float(POSTGRES_VERSION) >= 14.0:
            for metric_name in _iterate_metric_name(NEWER_14_METRICS):
                aggregator.assert_metric(metric_name, count=count, tags=db_tags)
    aggregator.assert_metric('postgresql.running', count=count, value=1, tags=expected_tags)


def check_db_count(aggregator, expected_tags, count=1):
    table_count = 18
    # We create 2 additional partition tables when partition is available + 2 parent tables
    if float(POSTGRES_VERSION) >= 11.0:
        table_count = 25
    aggregator.assert_metric(
        'postgresql.table.count',
        value=table_count,
        count=count,
        tags=expected_tags + ['db:{}'.format(DB_NAME), 'schema:public'],
    )
    aggregator.assert_metric('postgresql.db.count', value=106, count=1)


def check_connection_metrics(aggregator, expected_tags, count=1):
    for name in CONNECTION_METRICS:
        aggregator.assert_metric(name, count=count, tags=expected_tags)
    for db in COMMON_DBS:
        db_tags = expected_tags + ['db:{}'.format(db)]
        for name in CONNECTION_METRICS_DB:
            aggregator.assert_metric(name, count=count, tags=db_tags)


def check_activity_metrics(aggregator, tags, hostname=None, count=1):
    activity_metrics = [
        'postgresql.transactions.open',
        'postgresql.transactions.idle_in_transaction',
        'postgresql.active_queries',
        'postgresql.waiting_queries',
        'postgresql.active_waiting_queries',
        'postgresql.activity.xact_start_age',
    ]
    if POSTGRES_VERSION is None or float(POSTGRES_VERSION) >= 9.6:
        # Query won't have xid assigned so postgresql.activity.backend_xid_age won't be emitted
        activity_metrics.append('postgresql.activity.backend_xmin_age')
    for name in activity_metrics:
        aggregator.assert_metric(name, count=1, tags=tags, hostname=hostname)


def check_stat_replication_physical_slot(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 10:
        return
    replication_tags = expected_tags + [
        'wal_app_name:walreceiver',
        f'wal_client_addr:{get_container_ip(REPLICA_CONTAINER_1_NAME)}',
        'wal_state:streaming',
        'wal_sync_state:async',
        'slot_name:replication_slot',
        'slot_type:physical',
    ]
    for metric_name in _iterate_metric_name(QUERY_PG_REPLICATION_STATS_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=replication_tags)


def check_stat_replication_no_slot(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 10:
        return
    wal_app_name = 'replica2'
    if float(POSTGRES_VERSION) < 12:
        wal_app_name = 'walreceiver'
    replication_tags = expected_tags + [
        f'wal_app_name:{wal_app_name}',
        f'wal_client_addr:{get_container_ip(REPLICA_CONTAINER_2_NAME)}',
        'wal_state:streaming',
        'wal_sync_state:async',
    ]
    for metric_name in _iterate_metric_name(QUERY_PG_REPLICATION_STATS_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=replication_tags)


def check_wal_receiver_metrics(aggregator, expected_tags, count=1, connected=1):
    if float(POSTGRES_VERSION) < 10.0:
        return
    if not connected:
        aggregator.assert_metric(
            'postgresql.wal_receiver.connected', count=count, value=1, tags=expected_tags + ['status:disconnected']
        )
        return
    for metric_name in _iterate_metric_name(QUERY_PG_STAT_WAL_RECEIVER):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_physical_replication_slots(aggregator, expected_tags):
    replication_slot_tags = expected_tags + [
        'slot_name:replication_slot',
        'slot_persistence:permanent',
        'slot_state:active',
        'slot_type:physical',
    ]
    check_replication_slots(aggregator, expected_tags=replication_slot_tags)


def check_logical_replication_slots(aggregator, expected_tags):
    logical_replication_slot_tags = expected_tags + [
        'slot_name:logical_slot',
        'slot_state:inactive',
        'slot_type:logical',
    ]
    check_replication_slots(aggregator, expected_tags=logical_replication_slot_tags + ['slot_persistence:permanent'])
    # Only logical replication slots will have rows in pg_stats_replication_slots
    check_replication_slots_stats(aggregator, expected_tags=logical_replication_slot_tags)


def check_replication_slots(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 10.0:
        return
    for metric_name in _iterate_metric_name(QUERY_PG_REPLICATION_SLOTS):
        if 'slot_type:physical' in expected_tags and metric_name in [
            'postgresql.replication_slot.confirmed_flush_delay_bytes',
            'postgresql.replication_slot.catalog_xmin_age',
        ]:
            continue
        if 'slot_type:logical' in expected_tags and metric_name in [
            'postgresql.replication_slot.restart_delay_bytes',
            'postgresql.replication_slot.xmin_age',
        ]:
            continue
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_replication_slots_stats(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 14.0:
        return
    for metric_name in _iterate_metric_name(QUERY_PG_REPLICATION_SLOTS_STATS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_wait_event_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 10.0:
        return
    for metric_name in _iterate_metric_name(QUERY_PG_WAIT_EVENT_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_replication_delay(aggregator, metrics_cache, expected_tags, count=1):
    replication_metrics = metrics_cache.get_replication_metrics(VersionUtils.parse_version(POSTGRES_VERSION), False)
    for metric_name in _iterate_metric_name(replication_metrics):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_uptime_metrics(aggregator, expected_tags, count=1):
    for metric_name in _iterate_metric_name(QUERY_PG_UPTIME):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_control_metrics(aggregator, expected_tags, count=1):
    for metric_name in _iterate_metric_name(QUERY_PG_CONTROL_CHECKPOINT):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_conflict_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 9.1:
        return
    for db in COMMON_DBS:
        db_tags = expected_tags + ['db:{}'.format(db)]
        for name in CONFLICT_METRICS:
            aggregator.assert_metric(name, count=count, tags=db_tags)


def check_bgw_metrics(aggregator, expected_tags, count=1):
    for name in COMMON_BGW_METRICS:
        aggregator.assert_metric(name, count=count, tags=expected_tags)

    if float(POSTGRES_VERSION) < 17:
        for name in COMMON_BGW_METRICS_PG_BELOW_17:
            aggregator.assert_metric(name, count=count, tags=expected_tags)

    if float(POSTGRES_VERSION) >= 9.4:
        for name in COMMON_BGW_METRICS_PG_ABOVE_94:
            aggregator.assert_metric(name, count=count, tags=expected_tags)


def check_slru_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 13.0:
        return

    slru_caches = [
        'subtransaction',
        'serializable',
        'multixact_member',
        'transaction',
        'other',
        'notify',
        'commit_timestamp',
        'multixact_offset',
    ]
    if float(POSTGRES_VERSION) < 17.0:
        slru_caches = [
            'Subtrans',
            'Serial',
            'MultiXactMember',
            'Xact',
            'other',
            'Notify',
            'CommitTs',
            'MultiXactOffset',
        ]
    for metric_name in _iterate_metric_name(SLRU_METRICS):
        for slru_cache in slru_caches:
            aggregator.assert_metric(
                metric_name,
                count=count,
                tags=expected_tags + ['slru_name:{}'.format(slru_cache)],
            )


def check_snapshot_txid_metrics(aggregator, expected_tags, count=1):
    for metric_name in _iterate_metric_name(SNAPSHOT_TXID_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_file_wal_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 10:
        return

    for metric_name in _iterate_metric_name(WAL_FILE_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_stat_wal_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 14.0:
        return

    for metric_name in _iterate_metric_name(STAT_WAL_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_performance_metrics(aggregator, expected_tags, count=1, is_aurora=False):
    expected_metrics = set(CHECK_PERFORMANCE_METRICS)
    if is_aurora:
        expected_metrics = expected_metrics - {'replication_metrics'}
    if float(POSTGRES_VERSION) < 13.0:
        expected_metrics = expected_metrics - {'slru_metrics'}
    if float(POSTGRES_VERSION) < 10.0:
        expected_metrics = expected_metrics - {'replication_stats_metrics'}
    for name in expected_metrics:
        aggregator.assert_metric(
            'dd.postgres.operation.time', count=count, tags=expected_tags + ['operation:{}'.format(name)]
        )


def check_subscription_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 10:
        return
    for metric_name in _iterate_metric_name(STAT_SUBSCRIPTION_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_subscription_state_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 14:
        return
    for metric_name in _iterate_metric_name(SUBSCRIPTION_STATE_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_recovery_prefetch_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 15.0:
        return

    for metric_name in _iterate_metric_name(QUERY_PG_STAT_RECOVERY_PREFETCH):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_subscription_stats_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 15:
        return
    for metric_name in _iterate_metric_name(STAT_SUBSCRIPTION_STATS_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags)


def check_checksum_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 12:
        return
    for metric_name in _iterate_metric_name(CHECKSUM_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_tags + ['db:{}'.format(DB_NAME)])


def check_stat_io_metrics(aggregator, expected_tags, count=1):
    if float(POSTGRES_VERSION) < 16:
        return
    expected_stat_io_tags = expected_tags + [
        'backend_type:walsender',
        'context:normal',
        'object:relation',
    ]
    for metric_name in _iterate_metric_name(STAT_IO_METRICS):
        aggregator.assert_metric(metric_name, count=count, tags=expected_stat_io_tags)


def check_metrics_metadata(aggregator):
    exclude = ['dd.postgres.operation.time']
    aggregator.assert_metrics_using_metadata(get_metadata_metrics(), exclude=exclude)
