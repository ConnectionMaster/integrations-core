# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import psycopg
import pytest
from packaging import version

from datadog_checks.pgbouncer import PgBouncer

from . import common


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check(aggregator, instance, datadog_agent, dd_run_check):
    check = PgBouncer('pgbouncer', {}, [instance])
    dd_run_check(check)

    env_version = common.get_version_from_env()
    assert_metric_coverage(env_version, aggregator)

    # SHOW VERSION; is only available on pgbouncer 1.12+
    if env_version >= version.parse('1.12.0'):
        version_metadata = {
            'version.raw': str(env_version),
            'version.scheme': 'semver',
            'version.major': str(env_version.major),
            'version.minor': str(env_version.minor),
            'version.patch': str(env_version.micro),
        }
        datadog_agent.assert_metadata(check.check_id, version_metadata)
    else:
        # No version metadata expected for older versions
        datadog_agent.assert_metadata(check.check_id, {})


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_with_clients(instance, aggregator, datadog_agent, dd_run_check):
    # add some stats
    connection = psycopg.connect(
        host=common.HOST,
        port=common.PORT,
        user=common.USER,
        password=common.PASS,
        dbname=common.DB,
        connect_timeout=1,
    )
    cur = connection.cursor()
    cur.execute('SELECT * FROM persons;')

    instance.update(
        {
            'collect_per_client_metrics': True,
        }
    )

    # run the check
    check_with_clients = PgBouncer('pgbouncer', {}, [instance])
    check_with_clients.check_id = 'test:123'
    dd_run_check(check_with_clients)

    env_version = common.get_version_from_env()
    assert_metric_coverage(env_version, aggregator, include_clients=True)


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_with_servers(instance, aggregator, datadog_agent, dd_run_check):
    # add some stats
    connection = psycopg.connect(
        host=common.HOST,
        port=common.PORT,
        user=common.USER,
        password=common.PASS,
        dbname=common.DB,
        connect_timeout=1,
    )
    cur = connection.cursor()
    cur.execute('SELECT * FROM persons;')

    instance.update(
        {
            'collect_per_server_metrics': True,
        }
    )

    # run the check
    check_with_servers = PgBouncer('pgbouncer', {}, [instance])
    check_with_servers.check_id = 'test:123'
    dd_run_check(check_with_servers)

    env_version = common.get_version_from_env()
    assert_metric_coverage(env_version, aggregator, include_servers=True)


@pytest.mark.integration
def test_critical_service_check(instance, aggregator, dd_run_check):
    instance['port'] = '123'  # Bad port
    check = PgBouncer('pgbouncer', {}, [instance])
    with pytest.raises(Exception):
        dd_run_check(check)
    aggregator.assert_service_check(PgBouncer.SERVICE_CHECK_NAME, status=PgBouncer.CRITICAL)


@pytest.mark.integration
@pytest.mark.usefixtures("dd_environment")
def test_check_with_url(instance_with_url, aggregator, datadog_agent, dd_run_check):
    # run the check
    check = PgBouncer('pgbouncer', {}, [instance_with_url])
    check.check_id = 'test:123'
    dd_run_check(check)

    env_version = common.get_version_from_env()
    assert_metric_coverage(env_version, aggregator)

    if env_version >= version.parse('1.12.0'):
        version_metadata = {
            'version.raw': str(env_version),
            'version.scheme': 'semver',
            'version.major': str(env_version.major),
            'version.minor': str(env_version.minor),
            'version.patch': str(env_version.micro),
        }
        datadog_agent.assert_metadata(check.check_id, version_metadata)
    else:
        datadog_agent.assert_metadata(check.check_id, {})


@pytest.mark.e2e
def test_check_e2e(dd_agent_check, instance):
    # run the check
    aggregator = dd_agent_check(instance, rate=True)
    version = common.get_version_from_env()
    assert_metric_coverage(version, aggregator)


def assert_metric_coverage(env_version, aggregator, include_clients=False, include_servers=False):
    aggregator.assert_metric('pgbouncer.pools.cl_active')
    aggregator.assert_metric('pgbouncer.pools.cl_waiting')
    aggregator.assert_metric('pgbouncer.pools.sv_active')
    aggregator.assert_metric('pgbouncer.pools.sv_idle')
    aggregator.assert_metric('pgbouncer.pools.sv_used')
    aggregator.assert_metric('pgbouncer.pools.sv_tested')
    aggregator.assert_metric('pgbouncer.pools.sv_login')
    aggregator.assert_metric('pgbouncer.pools.maxwait')
    aggregator.assert_metric('pgbouncer.stats.avg_recv')
    aggregator.assert_metric('pgbouncer.stats.avg_sent')

    if env_version < version.parse('1.8.0'):
        aggregator.assert_metric('pgbouncer.stats.avg_req')
        aggregator.assert_metric('pgbouncer.stats.avg_query')
        aggregator.assert_metric('pgbouncer.stats.requests_per_second')
    else:
        aggregator.assert_metric('pgbouncer.pools.maxwait_us')
        aggregator.assert_metric('pgbouncer.stats.avg_transaction_time')
        aggregator.assert_metric('pgbouncer.stats.avg_query_time')
        aggregator.assert_metric('pgbouncer.stats.avg_transaction_count')
        aggregator.assert_metric('pgbouncer.stats.avg_query_count')
        aggregator.assert_metric('pgbouncer.stats.queries_per_second')
        aggregator.assert_metric('pgbouncer.stats.transactions_per_second')
        aggregator.assert_metric('pgbouncer.stats.total_transaction_time')
        aggregator.assert_metric('pgbouncer.stats.total_wait_time')
        aggregator.assert_metric('pgbouncer.stats.avg_wait_time')

    aggregator.assert_metric('pgbouncer.stats.total_query_time')
    aggregator.assert_metric('pgbouncer.stats.bytes_received_per_second')
    aggregator.assert_metric('pgbouncer.stats.bytes_sent_per_second')

    aggregator.assert_metric('pgbouncer.databases.pool_size', at_least=0)
    aggregator.assert_metric('pgbouncer.databases.max_connections', at_least=0)
    aggregator.assert_metric('pgbouncer.databases.current_connections', at_least=0)

    aggregator.assert_metric('pgbouncer.max_client_conn')

    if include_clients:
        aggregator.assert_metric('pgbouncer.clients.connect_time')
        aggregator.assert_metric('pgbouncer.clients.request_time')
        if env_version >= version.parse('1.8.0'):
            aggregator.assert_metric('pgbouncer.clients.wait')
            aggregator.assert_metric('pgbouncer.clients.wait_us')

    if include_servers:
        aggregator.assert_metric('pgbouncer.servers.connect_time')
        aggregator.assert_metric('pgbouncer.servers.request_time')

    # Service checks
    sc_tags = ['host:{}'.format(common.HOST), 'port:{}'.format(common.PORT), 'db:pgbouncer', 'optional:tag1']
    aggregator.assert_service_check(PgBouncer.SERVICE_CHECK_NAME, status=PgBouncer.OK, tags=sc_tags)
    aggregator.assert_all_metrics_covered()
