# CHANGELOG - fluxcd

<!-- towncrier release notes start -->

## 3.0.0 / 2025-07-10

***Changed***:

* Bump datadog_checks_base to 37.16.0 ([#20711](https://github.com/DataDog/integrations-core/pull/20711))

## 2.2.0 / 2025-01-16 / Agent 7.63.0

***Added***:

* Add `tls_ciphers` param to integration ([#19334](https://github.com/DataDog/integrations-core/pull/19334))

## 2.1.0 / 2024-10-04 / Agent 7.59.0

***Fixed***:

* Bump the version of datadog-checks-base to 37.0.0 ([#18617](https://github.com/DataDog/integrations-core/pull/18617))

## 2.0.0 / 2024-10-01 / Agent 7.58.0

***Changed***:

* Bump minimum version of base check ([#18733](https://github.com/DataDog/integrations-core/pull/18733))

***Added***:

* Bump the python version from 3.11 to 3.12 ([#18212](https://github.com/DataDog/integrations-core/pull/18212))

## 1.2.2 / 2024-07-05 / Agent 7.55.0

***Fixed***:

* Update config model names ([#17802](https://github.com/DataDog/integrations-core/pull/17802))

## 1.2.1 / 2024-05-31

***Fixed***:

* Update the description for the `tls_ca_cert` config option to use `openssl rehash` instead of `c_rehash` ([#16981](https://github.com/DataDog/integrations-core/pull/16981))

## 1.2.0 / 2024-02-16 / Agent 7.52.0

***Added***:

* Update the configuration file to include the new oauth options parameter ([#16835](https://github.com/DataDog/integrations-core/pull/16835))

## 1.1.0 / 2024-01-05 / Agent 7.51.0

***Added***:

* Add more metrics and official Fluxcd v2 support. ([#16117](https://github.com/DataDog/integrations-core/pull/16117))

***Fixed***:

* Bump base check dependency version to ensure Pydantic v2 support. ([#16117](https://github.com/DataDog/integrations-core/pull/16117))
* Correct config models for OpenMetrics check. ([#16117](https://github.com/DataDog/integrations-core/pull/16117))

## 1.0.0 / 2023-11-08

***Changed***:

* Config models update - PR [2088](https://github.com/DataDog/integrations-extras/pull/2088)

## 0.0.1

***Added***:

* Initial Fluxcd Integration.
