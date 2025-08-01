# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.argo_workflows import ArgoWorkflowsCheck
from datadog_checks.base.stubs import aggregator as agg
from datadog_checks.dev.utils import assert_service_checks, get_metadata_metrics


@pytest.fixture
def instance():
    return {'openmetrics_endpoint': 'http://localhost:9090/metrics'}


GAUGES = {
    (n, agg.GAUGE)
    for n in {
        'current_workflows',
        'pods',
        'queue_depth',
        'workers_busy',
        'workflow_condition',
        'go.goroutines',
        'go.info',
        'go.memstats.alloc_bytes',
        'go.memstats.buck_hash.sys_bytes',
        'go.memstats.gc.sys_bytes',
        'go.memstats.heap.alloc_bytes',
        'go.memstats.heap.idle_bytes',
        'go.memstats.heap.inuse_bytes',
        'go.memstats.heap.objects',
        'go.memstats.heap.released_bytes',
        'go.memstats.heap.sys_bytes',
        'go.memstats.mcache.inuse_bytes',
        'go.memstats.mcache.sys_bytes',
        'go.memstats.mspan.inuse_bytes',
        'go.memstats.mspan.sys_bytes',
        'go.memstats.next.gc_bytes',
        'go.memstats.other.sys_bytes',
        'go.memstats.stack.inuse_bytes',
        'go.memstats.stack.sys_bytes',
        'go.memstats.sys_bytes',
        'go.threads',
    }
}
COUNTS = {
    (n, agg.MONOTONIC_COUNT)
    for n in {
        'error.count',
        'k8s_request.count',
        'log_messages.count',
        'queue_adds.count',
        'workflows_processed.count',
        'go.memstats.alloc_bytes.count',
        'go.memstats.frees.count',
        'go.memstats.lookups.count',
        'go.memstats.mallocs.count',
    }
}
# Sorting eases debugging of missing metrics.
EXPECTED_METRICS = sorted(GAUGES | COUNTS)

V3_6_METRICS = {
    ('cronworkflows.concurrencypolicy_triggered.count', agg.MONOTONIC_COUNT),
    ('cronworkflows.triggered.count', agg.MONOTONIC_COUNT),
    ('deprecated.feature', agg.GAUGE),
    ('current_workflows', agg.GAUGE),
    ('is_leader', agg.GAUGE),
    ('log_messages.count', agg.MONOTONIC_COUNT),
    ('pod.pending.count', agg.MONOTONIC_COUNT),
    ('pods', agg.GAUGE),
    ('pods_total.count', agg.MONOTONIC_COUNT),
    ('queue_depth', agg.GAUGE),
    ('queue.longest_running', agg.GAUGE),
    ('queue.retries.count', agg.MONOTONIC_COUNT),
    ('queue.unfinished_work', agg.GAUGE),
    ('total.count', agg.MONOTONIC_COUNT),
    ('version', agg.GAUGE),
    ('workflowtemplate.runtime', agg.GAUGE),
    ('workflowtemplate.triggered.count', agg.MONOTONIC_COUNT),
}


@pytest.mark.parametrize(
    "fixture_file, description",
    [
        ('tests/fixtures/metrics.txt', 'Test with old metric names'),
        ('tests/fixtures/metricsv3-6+.txt', 'Test with new metric names (Argo v3.6+)'),
    ],
)
def test_check_with_fixtures(dd_run_check, aggregator, instance, mock_http_response, fixture_file, description):
    mock_http_response(file_path=fixture_file)
    check = ArgoWorkflowsCheck('argo_workflows', {}, [instance])
    dd_run_check(check)

    for m_name, m_type in EXPECTED_METRICS:
        aggregator.assert_metric(f'argo_workflows.{m_name}', metric_type=m_type)

    if fixture_file == 'tests/fixtures/metricsv3-6+.txt':
        for m_name, m_type in V3_6_METRICS:
            aggregator.assert_metric(f'argo_workflows.{m_name}', metric_type=m_type)

        histograms = (
            'k8s_request.duration',
            'queue.duration',
            'operation_duration_seconds',
            'queue_latency',
        )

        for m_name in histograms:
            aggregator.assert_metric(f'argo_workflows.{m_name}.sum', metric_type=agg.MONOTONIC_COUNT)
            aggregator.assert_metric(f'argo_workflows.{m_name}.count', metric_type=agg.MONOTONIC_COUNT)
            aggregator.assert_metric(f'argo_workflows.{m_name}.bucket', metric_type=agg.MONOTONIC_COUNT)

    histograms = (
        'operation_duration_seconds',
        'queue_latency',
    )
    for m_name in histograms:
        aggregator.assert_metric(f'argo_workflows.{m_name}.sum', metric_type=agg.MONOTONIC_COUNT)
        aggregator.assert_metric(f'argo_workflows.{m_name}.count', metric_type=agg.MONOTONIC_COUNT)
        aggregator.assert_metric(f'argo_workflows.{m_name}.bucket', metric_type=agg.MONOTONIC_COUNT)

    for suff in ('count', 'quantile', 'sum'):
        aggregator.assert_metric(f'argo_workflows.go.gc.duration.seconds.{suff}')

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())
    aggregator.assert_service_check('argo_workflows.openmetrics.health', ArgoWorkflowsCheck.OK)
    assert_service_checks(aggregator)


def test_emits_critical_service_check_when_service_is_down(dd_run_check, aggregator, instance, mock_http_response):
    mock_http_response(status_code=404)
    check = ArgoWorkflowsCheck('argo_workflows', {}, [instance])
    with pytest.raises(Exception, match='requests.exceptions.HTTPError'):
        dd_run_check(check)
    aggregator.assert_service_check('argo_workflows.openmetrics.health', ArgoWorkflowsCheck.CRITICAL)
