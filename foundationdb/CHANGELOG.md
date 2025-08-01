# CHANGELOG - FoundationDB

<!-- towncrier release notes start -->

## 3.3.1 / 2025-07-10

***Fixed***:

* Respect `tls_ca_file` and `tls_password` config options ([#19865](https://github.com/DataDog/integrations-core/pull/19865))

## 3.3.0 / 2025-05-15 / Agent 7.67.0

***Added***:

* Tag FoundationDB process metrics with process class, assigned roles ([#19682](https://github.com/DataDog/integrations-core/pull/19682))
* Introduce a `foundationdb.processes_per_role` gauge tagged by process role/class ([#19706](https://github.com/DataDog/integrations-core/pull/19706))
* Update dependencies ([#20215](https://github.com/DataDog/integrations-core/pull/20215))

## 3.2.1 / 2025-04-17 / Agent 7.66.0

***Fixed***:

* Honor `tags` instance configuration in FoundationDB integration ([#19771](https://github.com/DataDog/integrations-core/pull/19771))

## 3.2.0 / 2025-03-19 / Agent 7.65.0

***Added***:

* Add more FoundationDB metrics ([#19681](https://github.com/DataDog/integrations-core/pull/19681))

***Fixed***:

* Use `__NAMESPACE__` in the FoundationDB integration ([#19770](https://github.com/DataDog/integrations-core/pull/19770))

## 3.1.0 / 2025-02-20 / Agent 7.64.0

***Added***:

* Update dependencies ([#19576](https://github.com/DataDog/integrations-core/pull/19576))

## 3.0.0 / 2024-10-04 / Agent 7.59.0

***Removed***:

* Remove support for Python 2. ([#18580](https://github.com/DataDog/integrations-core/pull/18580))

***Fixed***:

* Bump the version of datadog-checks-base to 37.0.0 ([#18617](https://github.com/DataDog/integrations-core/pull/18617))

## 2.0.0 / 2024-10-01 / Agent 7.58.0

***Changed***:

* Bump minimum version of base check ([#18733](https://github.com/DataDog/integrations-core/pull/18733))

***Added***:

* Bump the python version from 3.11 to 3.12 ([#18212](https://github.com/DataDog/integrations-core/pull/18212))

## 1.4.0 / 2024-01-05 / Agent 7.51.0

***Added***:

* Bump the Python version from py3.9 to py3.11 ([#15997](https://github.com/DataDog/integrations-core/pull/15997))

## 1.3.1 / 2023-08-18 / Agent 7.48.0

***Fixed***:

* Update datadog-checks-base dependency version to 32.6.0 ([#15604](https://github.com/DataDog/integrations-core/pull/15604))

## 1.3.0 / 2023-08-10

***Added***:

* Update generated config models ([#15212](https://github.com/DataDog/integrations-core/pull/15212))

***Fixed***:

* Fix types for generated config models ([#15334](https://github.com/DataDog/integrations-core/pull/15334))

## 1.2.1 / 2023-07-10 / Agent 7.47.0

***Fixed***:

* Bump Python version from py3.8 to py3.9 ([#14701](https://github.com/DataDog/integrations-core/pull/14701))

## 1.2.0 / 2022-09-16 / Agent 7.40.0

***Added***:

* Refactor tooling for getting the current env name ([#12939](https://github.com/DataDog/integrations-core/pull/12939))

## 1.1.2 / 2022-08-05 / Agent 7.39.0

***Fixed***:

* Dependency updates ([#12653](https://github.com/DataDog/integrations-core/pull/12653))

## 1.1.1 / 2022-05-15 / Agent 7.37.0

***Fixed***:

* Upgrade dependencies ([#11958](https://github.com/DataDog/integrations-core/pull/11958))

## 1.1.0 / 2022-04-05

***Added***:

* Upgrade dependencies ([#11726](https://github.com/DataDog/integrations-core/pull/11726))
* Add metric_patterns options to filter all metric submission by a list of regexes ([#11695](https://github.com/DataDog/integrations-core/pull/11695))

## 1.0.0 / 2022-03-15

***Added***:

* Move foundationdb to core ([#11636](https://github.com/DataDog/integrations-core/pull/11636))
