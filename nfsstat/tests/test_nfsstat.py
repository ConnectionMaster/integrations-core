# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import logging
import os
from copy import deepcopy

import mock

from datadog_checks.base import ensure_unicode
from datadog_checks.nfsstat import NfsStatCheck

from .common import METRICS

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

log = logging.getLogger(__name__)


class TestNfsstat:
    CHECK_NAME = 'nfsstat'
    INSTANCES = {'main': {'tags': ['optional:tag1']}}

    INIT_CONFIG = {'nfsiostat_path': '/opt/datadog-agent/embedded/sbin/nfsiostat'}

    def test_no_devices(self, aggregator):
        instance = self.INSTANCES['main']
        c = NfsStatCheck(self.CHECK_NAME, self.INIT_CONFIG, [instance])
        c.log = mock.MagicMock()

        with mock.patch(
            'datadog_checks.nfsstat.nfsstat.get_subprocess_output',
            return_value=('No NFS mount points were found', '', 0),
        ):
            c.check(instance)
        c.log.warning.assert_called_once_with("No NFS mount points were found.", extra=mock.ANY)

    def test_autofs_enabled(self, aggregator):
        instance = self.INSTANCES['main']
        init_config = deepcopy(self.INIT_CONFIG)
        init_config['autofs_enabled'] = True
        c = NfsStatCheck(self.CHECK_NAME, init_config, [instance])
        c.log = mock.MagicMock()

        with mock.patch(
            'datadog_checks.nfsstat.nfsstat.get_subprocess_output',
            return_value=('No NFS mount points were found', '', 0),
        ):
            c.check(instance)
        c.log.debug.assert_called_once_with("AutoFS enabled: no mount points currently.")

    def test_check(self, aggregator):
        instance = self.INSTANCES['main']
        c = NfsStatCheck(self.CHECK_NAME, self.INIT_CONFIG, [instance])

        with open(os.path.join(FIXTURE_DIR, 'nfsiostat'), 'rb') as f:
            mock_output = ensure_unicode(f.read())

        with mock.patch('datadog_checks.nfsstat.nfsstat.get_subprocess_output', return_value=(mock_output, '', 0)):
            c.check(instance)

        tags = list(instance['tags'])
        tags.extend(['nfs_server:192.168.34.1', 'nfs_export:/exports/nfs/datadog/two', 'nfs_mount:/mnt/datadog/two'])
        tags_unicode = list(instance['tags'])
        tags_unicode.extend(
            [
                'nfs_server:192.168.34.1',
                'nfs_export:/exports/nfs/datadog/thr\u00e9\u00e9',
                'nfs_mount:/mnt/datadog/thr\u00e9\u00e9',
            ]
        )

        for metric in METRICS:
            aggregator.assert_metric(metric, tags=tags)
            aggregator.assert_metric(metric, tags=tags_unicode)

        assert aggregator.metrics_asserted_pct == 100.0
