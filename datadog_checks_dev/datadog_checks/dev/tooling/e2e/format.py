# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import re

from datadog_checks.dev._env import E2E_FIXTURE_NAME, deserialize_data

CONFIG_MESSAGE_PATTERN = 'DDEV_E2E_START_MESSAGE (.+) DDEV_E2E_END_MESSAGE'


def parse_config_from_result(env, result):
    output = result.stdout + result.stderr

    if 'NO E2E FIXTURE AVAILABLE' in output:
        return None, None, f'The environment fixture `{E2E_FIXTURE_NAME}` does not exist.'

    if f'{env}: platform mismatch' in output or 'unsupported platform' in output:
        return None, None, f'The environment `{env}` does not support this platform.'

    decoded = parse_encoded_config_data(result.stdout)
    if decoded is None:
        return (
            None,
            None,
            (
                '{}\n{}\nUnable to parse configuration. Try recreating your env to get the '
                'latest version of the dev package.'.format(result.stdout, result.stderr)
            ),
        )

    config = decoded['config']
    metadata = decoded['metadata']

    if config is None:
        return None, None, f'The environment fixture `{E2E_FIXTURE_NAME}` did not yield any configuration.'

    return config, metadata, None


def parse_encoded_config_data(output):
    match = re.search(CONFIG_MESSAGE_PATTERN, output)
    if match:
        return deserialize_data(match.group(1))
