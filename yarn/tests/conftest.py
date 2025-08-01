# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
from copy import deepcopy
from urllib.parse import urljoin

import pytest
from mock import patch
from requests.exceptions import SSLError

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckEndpoints
from datadog_checks.dev.http import MockResponse
from datadog_checks.yarn import YarnCheck
from datadog_checks.yarn.yarn import YARN_APPS_PATH, YARN_CLUSTER_METRICS_PATH, YARN_NODES_PATH, YARN_SCHEDULER_PATH

from .common import (
    FIXTURE_DIR,
    HERE,
    INSTANCE_INTEGRATION,
    TEST_PASSWORD,
    TEST_USERNAME,
    YARN_APPS_URL,
    YARN_CLUSTER_METRICS_URL,
    YARN_NODES_URL,
    YARN_SCHEDULER_URL,
)


@pytest.fixture(scope="session")
def dd_environment():
    conditions = [
        CheckEndpoints(urljoin(INSTANCE_INTEGRATION['resourcemanager_uri'], endpoint), attempts=240)
        for endpoint in (YARN_APPS_PATH, YARN_CLUSTER_METRICS_PATH, YARN_NODES_PATH, YARN_SCHEDULER_PATH)
    ]

    with docker_run(
        compose_file=os.path.join(HERE, "compose", "docker-compose.yaml"),
        mount_logs=True,
        conditions=conditions,
        sleep=30,
    ):
        yield INSTANCE_INTEGRATION


@pytest.fixture
def check():
    return lambda instance: YarnCheck('yarn', {}, [instance])


@pytest.fixture
def instance():
    return deepcopy(INSTANCE_INTEGRATION)


@pytest.fixture
def mocked_request():
    with patch("requests.Session.get", new=requests_get_mock):
        yield


@pytest.fixture
def mocked_auth_request():
    def requests_auth_get(session, *args, **kwargs):
        # Make sure we're passing in authentication
        assert 'auth' in kwargs, 'Missing "auth" argument in requests.Session.get(...) call'

        # Make sure we've got the correct username and password
        assert kwargs['auth'] == (
            TEST_USERNAME,
            TEST_PASSWORD,
        ), "Incorrect username or password in requests.Session.get"

        # Return mocked request.get(...)
        return requests_get_mock(session, *args, **kwargs)

    with patch("requests.Session.get", new=requests_auth_get):
        yield


@pytest.fixture
def mocked_bad_cert_request():
    """
    Mock request.Session.get to an endpoint with a badly configured ssl cert
    """

    def requests_bad_cert_get(session, *args, **kwargs):
        # Make sure we're passing in the 'verify' argument
        assert 'verify' in kwargs, 'Missing "verify" argument in requests.Session.get(...) call'

        if kwargs['verify']:
            raise SSLError("certificate verification failed for {}".format(args[0]))

        # Return the actual response
        return requests_get_mock(session, *args, **kwargs)

    with patch("requests.Session.get", new=requests_bad_cert_get):
        yield


def requests_get_mock(session, *args, **kwargs):
    if args[0] == YARN_CLUSTER_METRICS_URL:
        return MockResponse(file_path=os.path.join(FIXTURE_DIR, 'cluster_metrics'))
    elif args[0] == YARN_APPS_URL:
        return MockResponse(file_path=os.path.join(FIXTURE_DIR, 'apps_metrics'))
    elif args[0] == YARN_NODES_URL:
        return MockResponse(file_path=os.path.join(FIXTURE_DIR, 'nodes_metrics'))
    elif args[0] == YARN_SCHEDULER_URL:
        return MockResponse(file_path=os.path.join(FIXTURE_DIR, 'scheduler_metrics'))
