# CHANGELOG - CockroachDB

<!-- towncrier release notes start -->

## 6.0.0 / 2025-07-10

***Changed***:

* Bump datadog_checks_base to 37.16.0 ([#20711](https://github.com/DataDog/integrations-core/pull/20711))

## 5.1.0 / 2025-01-16 / Agent 7.63.0

***Added***:

* Add `tls_ciphers` param to integration ([#19334](https://github.com/DataDog/integrations-core/pull/19334))

## 5.0.0 / 2024-10-04 / Agent 7.59.0

***Removed***:

* Remove support for Python 2. ([#18580](https://github.com/DataDog/integrations-core/pull/18580))

***Fixed***:

* Bump the version of datadog-checks-base to 37.0.0 ([#18617](https://github.com/DataDog/integrations-core/pull/18617))

## 4.0.0 / 2024-10-01 / Agent 7.58.0

***Changed***:

* Bump minimum version of base check ([#18733](https://github.com/DataDog/integrations-core/pull/18733))

***Added***:

* Bump the python version from 3.11 to 3.12 ([#18212](https://github.com/DataDog/integrations-core/pull/18212))

## 3.3.2 / 2024-07-05 / Agent 7.55.0

***Fixed***:

* Update config model names ([#17802](https://github.com/DataDog/integrations-core/pull/17802))

## 3.3.1 / 2024-05-31

***Fixed***:

* Update the description for the `tls_ca_cert` config option to use `openssl rehash` instead of `c_rehash` ([#16981](https://github.com/DataDog/integrations-core/pull/16981))

## 3.3.0 / 2024-03-22 / Agent 7.53.0

***Added***:

* Collect changefeed metrics ([#17079](https://github.com/DataDog/integrations-core/pull/17079))
* Add admission metrics ([#17141](https://github.com/DataDog/integrations-core/pull/17141))
* Add distsender metrics ([#17155](https://github.com/DataDog/integrations-core/pull/17155))
* Add jobs metrics ([#17163](https://github.com/DataDog/integrations-core/pull/17163))
* Add kv metrics ([#17164](https://github.com/DataDog/integrations-core/pull/17164))
* Add physical replication and queue metrics ([#17166](https://github.com/DataDog/integrations-core/pull/17166))
* Collect more metrics ([#17183](https://github.com/DataDog/integrations-core/pull/17183))
* Collect new metrics ([#17192](https://github.com/DataDog/integrations-core/pull/17192))

Special thanks to [sudomateo](https://github.com/sudomateo) for their contributions to this release.

## 3.2.0 / 2024-02-16 / Agent 7.52.0

***Added***:

* Update the configuration file to include the new oauth options parameter ([#16835](https://github.com/DataDog/integrations-core/pull/16835))

## 3.1.0 / 2024-01-05 / Agent 7.51.0

***Added***:

* Bump the Python version from py3.9 to py3.11 ([#15997](https://github.com/DataDog/integrations-core/pull/15997))

## 3.0.0 / 2023-08-10 / Agent 7.48.0

***Changed***:

* Bump the minimum base check version ([#15427](https://github.com/DataDog/integrations-core/pull/15427))

***Added***:

* Update generated config models ([#15212](https://github.com/DataDog/integrations-core/pull/15212))

***Fixed***:

* Fix types for generated config models ([#15334](https://github.com/DataDog/integrations-core/pull/15334))

## 2.7.1 / 2023-07-10 / Agent 7.47.0

***Fixed***:

* Bump Python version from py3.8 to py3.9 ([#14701](https://github.com/DataDog/integrations-core/pull/14701))

## 2.7.0 / 2023-05-26 / Agent 7.46.0

***Added***:

* Add an ignore_connection_errors option to the openmetrics check ([#14504](https://github.com/DataDog/integrations-core/pull/14504))
* Add new metrics from CockroachDB 23 ([#14492](https://github.com/DataDog/integrations-core/pull/14492))
* Add new metrics to CockroachDB integration ([#14484](https://github.com/DataDog/integrations-core/pull/14484))

***Fixed***:

* Update minimum datadog base package version ([#14463](https://github.com/DataDog/integrations-core/pull/14463))
* Deprecate `use_latest_spec` option ([#14446](https://github.com/DataDog/integrations-core/pull/14446))

## 2.6.0 / 2023-03-03 / Agent 7.44.0

***Added***:

* Collect schedules_BACKUP_last_completed_time metric ([#13825](https://github.com/DataDog/integrations-core/pull/13825))

## 2.5.0 / 2022-12-09 / Agent 7.42.0

***Added***:

* Collect additional metrics ([#13339](https://github.com/DataDog/integrations-core/pull/13339))

## 2.4.1 / 2022-10-28 / Agent 7.41.0

***Fixed***:

* Remove metrics limit from legacy version of the integration ([#13038](https://github.com/DataDog/integrations-core/pull/13038))

## 2.4.0 / 2022-09-16 / Agent 7.40.0

***Added***:

* Update HTTP config spec templates ([#12890](https://github.com/DataDog/integrations-core/pull/12890))
* Document Openmetrics V2 version of backup metrics ([#12730](https://github.com/DataDog/integrations-core/pull/12730))

## 2.3.0 / 2022-08-05 / Agent 7.39.0

***Added***:

* [CockroachDB] Add additional metrics for CockroachDB integration ([#12382](https://github.com/DataDog/integrations-core/pull/12382)) Thanks [tomellis91](https://github.com/tomellis91).

## 2.2.1 / 2022-05-18 / Agent 7.37.0

***Fixed***:

* Fix extra metrics description example ([#12043](https://github.com/DataDog/integrations-core/pull/12043))

## 2.2.0 / 2022-05-15

***Added***:

* Support dynamic bearer tokens (Bound Service Account Token Volume) ([#11915](https://github.com/DataDog/integrations-core/pull/11915))

## 2.1.0 / 2022-04-05 / Agent 7.36.0

***Added***:

* Add metric_patterns options to filter all metric submission by a list of regexes ([#11695](https://github.com/DataDog/integrations-core/pull/11695))

***Fixed***:

* Remove outdated warning in the description for the `tls_ignore_warning` option ([#11591](https://github.com/DataDog/integrations-core/pull/11591))

## 2.0.0 / 2022-02-19 / Agent 7.35.0

***Changed***:

* Add tls_protocols_allowed option documentation ([#11251](https://github.com/DataDog/integrations-core/pull/11251))

***Added***:

* Add `pyproject.toml` file ([#11329](https://github.com/DataDog/integrations-core/pull/11329))

***Fixed***:

* Fix namespace packaging on Python 2 ([#11532](https://github.com/DataDog/integrations-core/pull/11532))

## 1.9.2 / 2022-01-21 / Agent 7.34.0

***Fixed***:

* Fix license header dates in autogenerated files ([#11187](https://github.com/DataDog/integrations-core/pull/11187))

## 1.9.1 / 2022-01-18

***Fixed***:

* Fix the type of `bearer_token_auth` ([#11144](https://github.com/DataDog/integrations-core/pull/11144))

## 1.9.0 / 2022-01-08

***Added***:

* Allow the use of the new OpenMetrics implementation ([#11026](https://github.com/DataDog/integrations-core/pull/11026))

***Fixed***:

* Bump base package ([#11070](https://github.com/DataDog/integrations-core/pull/11070))
* Add comment to autogenerated model files ([#10945](https://github.com/DataDog/integrations-core/pull/10945))

## 1.8.0 / 2021-11-13 / Agent 7.33.0

***Added***:

* Document new include_labels option ([#10617](https://github.com/DataDog/integrations-core/pull/10617))
* Document new use_process_start_time option ([#10601](https://github.com/DataDog/integrations-core/pull/10601))
* Add runtime configuration validation ([#8897](https://github.com/DataDog/integrations-core/pull/8897))

## 1.7.0 / 2021-10-04 / Agent 7.32.0

***Added***:

* Add HTTP option to control the size of streaming responses ([#10183](https://github.com/DataDog/integrations-core/pull/10183))
* Add allow_redirect option ([#10160](https://github.com/DataDog/integrations-core/pull/10160))

***Fixed***:

* Fix the description of the `allow_redirects` HTTP option ([#10195](https://github.com/DataDog/integrations-core/pull/10195))

## 1.6.0 / 2021-05-28 / Agent 7.29.0

***Added***:

* Support "ignore_tags" configuration ([#9392](https://github.com/DataDog/integrations-core/pull/9392))

## 1.5.1 / 2021-01-25 / Agent 7.26.0

***Fixed***:

* Update prometheus_metrics_prefix documentation ([#8236](https://github.com/DataDog/integrations-core/pull/8236))

## 1.5.0 / 2020-10-31 / Agent 7.24.0

***Added***:

* Sync openmetrics config specs with new option ignore_metrics_by_labels ([#7823](https://github.com/DataDog/integrations-core/pull/7823))
* Add ability to dynamically get authentication information ([#7660](https://github.com/DataDog/integrations-core/pull/7660))

## 1.4.0 / 2020-09-21 / Agent 7.23.0

***Added***:

* Add RequestsWrapper option to support UTF-8 for basic auth ([#7441](https://github.com/DataDog/integrations-core/pull/7441))
* Add config specs ([#7439](https://github.com/DataDog/integrations-core/pull/7439))

## 1.3.0 / 2020-05-17 / Agent 7.20.0

***Added***:

* Allow optional dependency installation for all checks ([#6589](https://github.com/DataDog/integrations-core/pull/6589))

## 1.2.0 / 2020-04-04 / Agent 7.19.0

***Added***:

* Collect metadata for CockroachDB ([#5924](https://github.com/DataDog/integrations-core/pull/5924))

***Fixed***:

* Update deprecated imports ([#6088](https://github.com/DataDog/integrations-core/pull/6088))

## 1.1.0 / 2019-05-14 / Agent 6.12.0

***Added***:

* Adhere to code style ([#3490](https://github.com/DataDog/integrations-core/pull/3490))

## 1.0.0 / 2018-10-13 / Agent 6.6.0

***Added***:

* Add CockroachDB integration ([#2150][1])

[1]: https://github.com/DataDog/integrations-core/pull/2150
