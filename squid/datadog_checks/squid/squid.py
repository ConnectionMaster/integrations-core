# (C) Datadog, Inc. 2010-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import re

import requests

from datadog_checks.base import AgentCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'squid'

METRIC_PREFIX = "squid.cachemgr"
SERVICE_CHECK = "squid.can_connect"
SQUID_COUNTERS = [
    "client_http.requests",
    "client_http.hits",
    "client_http.errors",
    "client_http.kbytes_in",
    "client_http.kbytes_out",
    "client_http.hit_kbytes_out",
    "server.all.requests",
    "server.all.errors",
    "server.all.kbytes_in",
    "server.all.kbytes_out",
    "server.http.requests",
    "server.http.errors",
    "server.http.kbytes_in",
    "server.http.kbytes_out",
    "server.ftp.requests",
    "server.ftp.errors",
    "server.ftp.kbytes_in",
    "server.ftp.kbytes_out",
    "server.other.requests",
    "server.other.errors",
    "server.other.kbytes_in",
    "server.other.kbytes_out",
    "icp.pkts_sent",
    "icp.pkts_recv",
    "icp.queries_sent",
    "icp.replies_sent",
    "icp.queries_recv",
    "icp.replies_recv",
    "icp.query_timeouts",
    "icp.replies_queued",
    "icp.kbytes_sent",
    "icp.kbytes_recv",
    "icp.q_kbytes_sent",
    "icp.r_kbytes_sent",
    "icp.q_kbytes_recv",
    "icp.r_kbytes_recv",
    "icp.times_used",
    "cd.times_used",
    "cd.msgs_sent",
    "cd.msgs_recv",
    "cd.memory",
    "cd.local_memory",
    "cd.kbytes_sent",
    "cd.kbytes_recv",
    "unlink.requests",
    "page_faults",
    "select_loops",
    "cpu_time",
    "swap.outs",
    "swap.ins",
    "swap.files_cleaned",
    "aborted_requests",
]

# Regular SEMVER pattern but the "patch" part is optional.
SQUID_VERSION_PATTERN = re.compile(
    r"""
    (?P<major>0|[1-9]\d*)
    \.
    (?P<minor>0|[1-9]\d*)
    (?:\.(?P<patch>0|[1-9]\d*))?
    (?:-(?P<release>
        (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
        (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
    ))?
    (?:\+(?P<build>
        [0-9a-zA-Z-]+
        (?:\.[0-9a-zA-Z-]+)*
    ))?
    """,
    re.VERBOSE,
)


class SquidCheck(AgentCheck):
    HTTP_CONFIG_REMAPPER = {'cachemgr_username': {'name': 'username'}, 'cachemgr_password': {'name': 'password'}}

    def check(self, instance):
        name, host, port, custom_tags = self.parse_instance(instance)
        tags = ["name:%s" % name]
        # Get the squid counters values
        counters = self.get_counters(host, port, tags + custom_tags)

        # Send these values as rate
        for counter, value in counters.items():
            self.rate(counter, value, tags=tags + custom_tags)

    def get_counters(self, host, port, tags):
        if not (host.startswith('http://') or host.startswith('https://')):
            host = 'http://%s' % host
        url = "%s:%s/squid-internal-mgr/counters" % (host, port)
        try:
            res = self.http.get(url)
            res.raise_for_status()
            self.service_check(SERVICE_CHECK, AgentCheck.OK, tags=tags)
            headers = res.headers
            self.submit_version(headers)

        except requests.exceptions.RequestException as e:
            self.service_check(SERVICE_CHECK, AgentCheck.CRITICAL, tags=tags)
            self.log.error('There was an error connecting to squid at %s: %s', url, e)
            raise

        # Each line is a counter in the form 'counter_name = value'
        raw_counters = res.text.strip().split("\n")
        counters = {}
        for line in raw_counters:
            counter, value = self.parse_counter(line)
            if counter in SQUID_COUNTERS:
                counters["%s.%s" % (METRIC_PREFIX, counter)] = float(value)
        return counters

    def parse_instance(self, instance):
        name = instance.get("name")
        if not name:
            raise Exception("Each instance in squid.yaml must have a name")
        host = instance.get("host", "localhost")
        port = instance.get("port", 3128)
        custom_tags = instance.get("tags", [])
        return name, host, port, custom_tags

    def parse_counter(self, line):
        # Squid returns a plain text page with one counter per line:
        # ...
        # client_http.errors = 0
        # client_http.kbytes_in = 0
        # client_http.kbytes_out = 2
        # ...
        try:
            counter, value = line.strip().split("=")
            counter = counter.strip()
            value = value.strip()
        except ValueError as e:
            self.log.error('Error parsing counter with line %s: %s', line, e)
            return None, None

        return counter, value

    @AgentCheck.metadata_entrypoint
    def submit_version(self, headers):
        version_header = headers.get("Server", "")
        if "/" not in version_header:
            self.log.debug("Squid version %s not valid version", version_header)
            return

        squid_version = version_header.split('/')[1]
        self.set_metadata(
            'version', squid_version, scheme='regex', final_scheme='semver', pattern=SQUID_VERSION_PATTERN
        )
        self.log.debug("Squid version %s metadata submitted")
