# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS
from typing import Optional

from datadog_checks.base import AgentCheck, ConfigurationError, is_affirmative
from datadog_checks.base.utils.aws import rds_parse_tags_from_endpoint
from datadog_checks.base.utils.db.utils import get_agent_host_tags

SSL_MODES = {'disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full'}
TABLE_COUNT_LIMIT = 200

DEFAULT_IGNORE_DATABASES = [
    'template0',
    'template1',
    'rdsadmin',
    'azure_maintenance',
    'cloudsqladmin',
    'alloydbadmin',
    'alloydbmetadata',
    'postgres',
]

DEFAULT_IGNORED_SCHEMAS_OWNED_BY = ['rdsadmin', 'rds_superuser']


class PostgresConfig:
    RATE = AgentCheck.rate
    GAUGE = AgentCheck.gauge
    MONOTONIC = AgentCheck.monotonic_count

    def __init__(self, instance, init_config, check):
        self.exclude_hostname = instance.get("exclude_hostname", False)
        self.database_identifier = instance.get('database_identifier', {})
        self.init_config = init_config
        self.host = instance.get('host', '')
        if not self.host:
            raise ConfigurationError('Specify a Postgres host to connect to.')
        self.port = instance.get('port', '5432')
        if self.port != '':
            self.port = int(self.port)
        self.user = instance.get('username', '')
        if not self.user:
            raise ConfigurationError('Please specify a user to connect to Postgres.')
        self.password = instance.get('password', '')
        self.dbname = instance.get('dbname', 'postgres')
        self.reported_hostname = instance.get('reported_hostname', '')
        self.dbstrict = is_affirmative(instance.get('dbstrict', False))
        self.disable_generic_tags = is_affirmative(instance.get('disable_generic_tags', False)) if instance else False

        self.discovery_config = instance.get('database_autodiscovery', {"enabled": False})
        if self.discovery_config['enabled'] and self.dbname != 'postgres':
            raise ConfigurationError(
                "'dbname' parameter should not be set when `database_autodiscovery` is enabled."
                "To monitor more databases, add them to the `database_autodiscovery` includelist."
            )

        self.application_name = instance.get('application_name', 'datadog-agent')
        if not self.application_name.isascii():
            raise ConfigurationError("Application name can include only ASCII characters: %s", self.application_name)

        self.query_timeout = int(instance.get('query_timeout', 5000))
        self.idle_connection_timeout = instance.get('idle_connection_timeout', 60000)
        self.relations = instance.get('relations', [])
        if self.relations and not (self.dbname or self.discovery_config['enabled']):
            raise ConfigurationError(
                '"dbname" parameter must be set OR autodiscovery must be enabled when using the "relations" parameter.'
            )
        self.max_connections = instance.get('max_connections', 30)

        ssl = instance.get('ssl', "allow")
        if ssl in SSL_MODES:
            self.ssl_mode = ssl
        else:
            check.warning(f"Invalid ssl option '{ssl}', should be one of {SSL_MODES}. Defaulting to 'allow'.")
            self.ssl_mode = "allow"

        self.ssl_cert = instance.get('ssl_cert', None)
        self.ssl_root_cert = instance.get('ssl_root_cert', None)
        self.ssl_key = instance.get('ssl_key', None)
        self.ssl_password = instance.get('ssl_password', None)
        self.table_count_limit = instance.get('table_count_limit', TABLE_COUNT_LIMIT)
        self.collect_buffercache_metrics = is_affirmative(instance.get('collect_buffercache_metrics', False))
        self.collect_function_metrics = is_affirmative(instance.get('collect_function_metrics', False))
        # Default value for `count_metrics` is True for backward compatibility
        self.collect_count_metrics = is_affirmative(instance.get('collect_count_metrics', True))
        self.collect_activity_metrics = is_affirmative(instance.get('collect_activity_metrics', False))
        self.collect_checksum_metrics = is_affirmative(instance.get('collect_checksum_metrics', False))
        self.activity_metrics_excluded_aggregations = instance.get('activity_metrics_excluded_aggregations', [])
        self.collect_database_size_metrics = is_affirmative(instance.get('collect_database_size_metrics', True))
        self.collect_wal_metrics = self._should_collect_wal_metrics(instance.get('collect_wal_metrics'))
        self.collect_bloat_metrics = is_affirmative(instance.get('collect_bloat_metrics', False))
        self.data_directory = instance.get('data_directory', None)
        self.ignore_databases = instance.get('ignore_databases', DEFAULT_IGNORE_DATABASES)
        if is_affirmative(instance.get('collect_default_database', True)):
            self.ignore_databases = [d for d in self.ignore_databases if d != 'postgres']
        self.ignore_schemas_owned_by = instance.get('ignore_schemas_owned_by', DEFAULT_IGNORED_SCHEMAS_OWNED_BY)
        self.tag_replication_role = is_affirmative(instance.get('tag_replication_role', True))
        self.custom_metrics = self._get_custom_metrics(instance.get('custom_metrics', []))
        self.max_relations = int(instance.get('max_relations', 300))
        self.min_collection_interval = instance.get('min_collection_interval', 15)
        # database monitoring adds additional telemetry for query metrics & samples
        self.dbm_enabled = is_affirmative(instance.get('dbm', instance.get('deep_database_monitoring', False)))
        self.full_statement_text_cache_max_size = instance.get('full_statement_text_cache_max_size', 10000)
        self.full_statement_text_samples_per_hour_per_query = instance.get(
            'full_statement_text_samples_per_hour_per_query', 1
        )
        # Support a custom view when datadog user has insufficient privilege to see queries
        self.pg_stat_statements_view = instance.get('pg_stat_statements_view', 'pg_stat_statements')
        # statement samples & execution plans
        self.pg_stat_activity_view = instance.get('pg_stat_activity_view', 'pg_stat_activity')
        self.statement_samples_config = instance.get('query_samples', instance.get('statement_samples', {})) or {}
        self.settings_metadata_config = instance.get('collect_settings', {}) or {}
        self.schemas_metadata_config = instance.get('collect_schemas', {"enabled": False})
        self.resources_metadata_config = instance.get('collect_resources', {}) or {}
        self.statement_activity_config = instance.get('query_activity', {}) or {}
        self.statement_metrics_config = instance.get('query_metrics', {}) or {}
        self.query_encodings = instance.get('query_encodings')
        self.managed_identity = instance.get('managed_identity', {})
        self.cloud_metadata = {}
        aws = instance.get('aws', {})
        gcp = instance.get('gcp', {})
        azure = instance.get('azure', {})
        # Remap fully_qualified_domain_name to name
        azure = {k if k != 'fully_qualified_domain_name' else 'name': v for k, v in azure.items()}
        if aws:
            aws['managed_authentication'] = self._aws_managed_authentication(aws, self.password)
            self.cloud_metadata.update({'aws': aws})
        if gcp:
            self.cloud_metadata.update({'gcp': gcp})
        if azure:
            azure['managed_authentication'] = self._azure_managed_authentication(azure, self.managed_identity)
            self.cloud_metadata.update({'azure': azure})
        obfuscator_options_config = instance.get('obfuscator_options', {}) or {}
        self.obfuscator_options = {
            # Valid values for this can be found at
            # https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/semantic_conventions/database.md#connection-level-attributes
            'dbms': 'postgresql',
            'replace_digits': is_affirmative(
                obfuscator_options_config.get(
                    'replace_digits', obfuscator_options_config.get('quantize_sql_tables', False)
                )
            ),
            'dollar_quoted_func': is_affirmative(obfuscator_options_config.get('keep_dollar_quoted_func', True)),
            'keep_sql_alias': is_affirmative(obfuscator_options_config.get('keep_sql_alias', True)),
            'return_json_metadata': is_affirmative(obfuscator_options_config.get('collect_metadata', True)),
            'table_names': is_affirmative(obfuscator_options_config.get('collect_tables', True)),
            'collect_commands': is_affirmative(obfuscator_options_config.get('collect_commands', True)),
            'collect_comments': is_affirmative(obfuscator_options_config.get('collect_comments', True)),
            # Config to enable/disable obfuscation of sql statements with go-sqllexer pkg
            # Valid values for this can be found at https://github.com/DataDog/datadog-agent/blob/main/pkg/obfuscate/obfuscate.go#L108
            'obfuscation_mode': obfuscator_options_config.get('obfuscation_mode', 'obfuscate_and_normalize'),
            'remove_space_between_parentheses': is_affirmative(
                obfuscator_options_config.get('remove_space_between_parentheses', False)
            ),
            'keep_null': is_affirmative(obfuscator_options_config.get('keep_null', False)),
            'keep_boolean': is_affirmative(obfuscator_options_config.get('keep_boolean', False)),
            'keep_positional_parameter': is_affirmative(
                obfuscator_options_config.get('keep_positional_parameter', False)
            ),
            'keep_trailing_semicolon': is_affirmative(obfuscator_options_config.get('keep_trailing_semicolon', False)),
            'keep_identifier_quotation': is_affirmative(
                obfuscator_options_config.get('keep_identifier_quotation', False)
            ),
            'keep_json_path': is_affirmative(obfuscator_options_config.get('keep_json_path', False)),
        }
        collect_raw_query_statement_config: dict = instance.get('collect_raw_query_statement', {}) or {}
        self.collect_raw_query_statement = {
            "enabled": is_affirmative(collect_raw_query_statement_config.get('enabled', False)),
            "cache_max_size": int(collect_raw_query_statement_config.get('cache_max_size', 10000)),
            "samples_per_hour_per_query": int(collect_raw_query_statement_config.get('samples_per_hour_per_query', 1)),
        }
        self.log_unobfuscated_queries = is_affirmative(instance.get('log_unobfuscated_queries', False))
        self.log_unobfuscated_plans = is_affirmative(instance.get('log_unobfuscated_plans', False))
        self.database_instance_collection_interval = instance.get('database_instance_collection_interval', 300)
        self.incremental_query_metrics = is_affirmative(
            self.statement_metrics_config.get('incremental_query_metrics', False)
        )
        self.baseline_metrics_expiry = self.statement_metrics_config.get('baseline_metrics_expiry', 300)
        self.service = instance.get('service') or init_config.get('service') or ''

        self.tags = self._build_tags(
            custom_tags=instance.get('tags', []),
            propagate_agent_tags=self._should_propagate_agent_tags(instance, init_config),
            additional_tags=["raw_query_statement:enabled"] if self.collect_raw_query_statement["enabled"] else [],
        )

    def _build_tags(self, custom_tags, propagate_agent_tags, additional_tags):
        # Clean up tags in case there was a None entry in the instance
        # e.g. if the yaml contains tags: but no actual tags
        if custom_tags is None:
            tags = []
        else:
            tags = list(set(custom_tags))

        # preset tags to host
        if not self.disable_generic_tags:
            tags.append('server:{}'.format(self.host))
        if self.port:
            tags.append('port:{}'.format(self.port))
        else:
            tags.append('port:socket')

        # preset tags to the database name
        tags.extend(["db:%s" % self.dbname])

        rds_tags = rds_parse_tags_from_endpoint(self.host)
        if rds_tags:
            tags.extend(rds_tags)

        if propagate_agent_tags:
            try:
                agent_tags = get_agent_host_tags()
                tags.extend(agent_tags)
            except Exception as e:
                raise ConfigurationError(
                    'propagate_agent_tags enabled but there was an error fetching agent tags {}'.format(e)
                )

        if additional_tags:
            tags.extend(additional_tags)
        return tags

    @staticmethod
    def _get_custom_metrics(custom_metrics):
        # Otherwise pre-process custom metrics and verify definition
        required_parameters = ("descriptors", "metrics", "query", "relation")

        for m in custom_metrics:
            for param in required_parameters:
                if param not in m:
                    raise ConfigurationError('Missing {} parameter in custom metric'.format(param))

            # Old formatting to new formatting. The first params is always the columns names from which to
            # read metrics. The `relation` param instructs the check to replace the next '%s' with the list of
            # relations names.
            if m['relation']:
                m['query'] = m['query'] % ('{metrics_columns}', '{relations_names}')
            else:
                m['query'] = m['query'] % '{metrics_columns}'

            try:
                for ref, (_, mtype) in m['metrics'].items():
                    cap_mtype = mtype.upper()
                    if cap_mtype not in ('RATE', 'GAUGE', 'MONOTONIC'):
                        raise ConfigurationError(
                            'Collector method {} is not known. Known methods are RATE, GAUGE, MONOTONIC'.format(
                                cap_mtype
                            )
                        )

                    m['metrics'][ref][1] = getattr(PostgresConfig, cap_mtype)
            except Exception as e:
                raise Exception('Error processing custom metric `{}`: {}'.format(m, e))
        return custom_metrics

    @staticmethod
    def _aws_managed_authentication(aws, password):
        if 'managed_authentication' not in aws:
            # for backward compatibility
            # if managed_authentication is not set, we assume it is enabled if region is set and password is not set
            managed_authentication = {}
            managed_authentication['enabled'] = 'region' in aws and not password
        else:
            managed_authentication = aws['managed_authentication']
            enabled = is_affirmative(managed_authentication.get('enabled', False))
            if enabled and 'region' not in aws:
                raise ConfigurationError('AWS region must be set when using AWS managed authentication')
            managed_authentication['enabled'] = enabled
        return managed_authentication

    @staticmethod
    def _azure_managed_authentication(azure, managed_identity):
        if 'managed_authentication' not in azure:
            # for backward compatibility
            # if managed_authentication is not set, we assume it is enabled if client_id is set in managed_identity
            managed_authentication = {}
            if managed_identity:
                managed_authentication['enabled'] = 'client_id' in managed_identity
                managed_authentication.update(managed_identity)
            else:
                managed_authentication['enabled'] = False
        else:
            # if managed_authentication is set, we ignore the legacy managed_identity config
            managed_authentication = azure['managed_authentication']
            enabled = is_affirmative(managed_authentication.get('enabled', False))
            if enabled and 'client_id' not in managed_authentication:
                raise ConfigurationError('Azure client_id must be set when using Azure managed authentication')
            managed_authentication['enabled'] = enabled
        return managed_authentication

    @staticmethod
    def _should_collect_wal_metrics(collect_wal_metrics) -> Optional[bool]:
        if collect_wal_metrics is not None:
            # if the user has explicitly set the value, return the boolean
            return is_affirmative(collect_wal_metrics)

        return None

    @staticmethod
    def _should_propagate_agent_tags(instance, init_config) -> bool:
        '''
        return True if the agent tags should be propagated to the check
        '''
        instance_propagate_agent_tags = instance.get('propagate_agent_tags')
        init_config_propagate_agent_tags = init_config.get('propagate_agent_tags')

        if instance_propagate_agent_tags is not None:
            # if the instance has explicitly set the value, return the boolean
            return instance_propagate_agent_tags
        if init_config_propagate_agent_tags is not None:
            # if the init_config has explicitly set the value, return the boolean
            return init_config_propagate_agent_tags
        # if neither the instance nor the init_config has set the value, return False
        return False
