# CHANGELOG - TLS

<!-- towncrier release notes start -->

## 5.0.0 / 2025-07-10

***Changed***:

* Bump datadog_checks_base to 37.16.0 ([#20711](https://github.com/DataDog/integrations-core/pull/20711))

***Added***:

* Update dependencies ([#20561](https://github.com/DataDog/integrations-core/pull/20561))

***Fixed***:

* Allow HTTPS requests to use `tls_ciphers` parameter ([#20179](https://github.com/DataDog/integrations-core/pull/20179))

## 4.6.0 / 2025-06-12 / Agent 7.68.0

***Added***:

* Update dependencies ([#20399](https://github.com/DataDog/integrations-core/pull/20399))

## 4.5.0 / 2025-05-15 / Agent 7.67.0

***Added***:

* Update dependencies ([#20215](https://github.com/DataDog/integrations-core/pull/20215))

***Fixed***:

* Replace deprecated `cert.not_valid_after` and `datetime.utcnow()` with `cert.not_valid_after_utc` and `datetime.now(timezone.utc)` respectively. ([#20100](https://github.com/DataDog/integrations-core/pull/20100))

## 4.4.0 / 2025-04-17 / Agent 7.66.0

***Added***:

* Update dependencies ([#19962](https://github.com/DataDog/integrations-core/pull/19962))

## 4.3.0 / 2025-03-19 / Agent 7.65.0

***Added***:

* Update dependencies ([#19687](https://github.com/DataDog/integrations-core/pull/19687))

***Fixed***:

* Bump base check dependency to use new assert method functionality. ([#19763](https://github.com/DataDog/integrations-core/pull/19763))

## 4.2.0 / 2025-01-25 / Agent 7.63.0

***Added***:

* Update dependencies ([#19430](https://github.com/DataDog/integrations-core/pull/19430))

## 4.1.0 / 2025-01-16

***Added***:

* Add `tls_ciphers` param to integration ([#19334](https://github.com/DataDog/integrations-core/pull/19334))

## 4.0.0 / 2024-10-04 / Agent 7.59.0

***Removed***:

* Remove support for Python 2. ([#18580](https://github.com/DataDog/integrations-core/pull/18580))

***Fixed***:

* Bump the version of datadog-checks-base to 37.0.0 ([#18617](https://github.com/DataDog/integrations-core/pull/18617))

## 3.0.0 / 2024-10-01 / Agent 7.58.0

***Changed***:

* Bump minimum version of base check ([#18733](https://github.com/DataDog/integrations-core/pull/18733))

***Security***:

* Bump version of cryptography to 43.0.1 to address vulnerability ([#18656](https://github.com/DataDog/integrations-core/pull/18656))

***Added***:

* Bump the python version from 3.11 to 3.12 ([#18212](https://github.com/DataDog/integrations-core/pull/18212))

## 2.20.0 / 2024-09-05

***Added***:

* Update dependencies ([#18478](https://github.com/DataDog/integrations-core/pull/18478))

## 2.19.0 / 2024-08-09 / Agent 7.57.0

***Added***:

* Update dependencies ([#18187](https://github.com/DataDog/integrations-core/pull/18187))

## 2.18.0 / 2024-07-05 / Agent 7.56.0

***Added***:

* Update dependencies ([#17817](https://github.com/DataDog/integrations-core/pull/17817))

## 2.17.0 / 2024-05-31 / Agent 7.55.0

***Added***:

* Update dependencies ([#17519](https://github.com/DataDog/integrations-core/pull/17519))

## 2.16.1 / 2024-03-22 / Agent 7.53.0

***Fixed***:

* Attempt getting protocol version before certificate ([#17046](https://github.com/DataDog/integrations-core/pull/17046))

## 2.16.0 / 2024-03-07 / Agent 7.52.0

***Security***:

* Bump cryptography to 42.0.5 ([#17054](https://github.com/DataDog/integrations-core/pull/17054))

## 2.15.0 / 2024-02-16

***Added***:

* Bump `service-identity` version to 23.1.0 ([#16558](https://github.com/DataDog/integrations-core/pull/16558))
* Update dependencies ([#16788](https://github.com/DataDog/integrations-core/pull/16788))

## 2.14.0 / 2024-01-05 / Agent 7.51.0

***Added***:

* Bump the Python version from py3.9 to py3.11 ([#15997](https://github.com/DataDog/integrations-core/pull/15997))
* Update dependencies ([#16448](https://github.com/DataDog/integrations-core/pull/16448))

## 2.13.2 / 2023-12-04 / Agent 7.50.0

***Fixed***:

* Bump the cryptography version to 41.0.6 ([#16322](https://github.com/DataDog/integrations-core/pull/16322))

## 2.13.1 / 2023-10-26 / Agent 7.49.0

***Fixed***:

* Bump the `cryptography` version to 41.0.5 ([#16083](https://github.com/DataDog/integrations-core/pull/16083))

## 2.13.0 / 2023-09-29

***Added***:

* Update Cryptography dependency ([#15922](https://github.com/DataDog/integrations-core/pull/15922))

## 2.12.1 / 2023-08-18 / Agent 7.48.0

***Fixed***:

* Bump cryptography to 41.0.3 ([#15517](https://github.com/DataDog/integrations-core/pull/15517))
* Update datadog-checks-base dependency version to 32.6.0 ([#15604](https://github.com/DataDog/integrations-core/pull/15604))

## 2.12.0 / 2023-08-10

***Added***:

* Update generated config models ([#15212](https://github.com/DataDog/integrations-core/pull/15212))

***Fixed***:

* Fix types for generated config models ([#15334](https://github.com/DataDog/integrations-core/pull/15334))

## 2.11.0 / 2023-07-10 / Agent 7.47.0

***Added***:

* Bump dependencies for Agent 7.47 ([#15145](https://github.com/DataDog/integrations-core/pull/15145))

***Fixed***:

* Bump Python version from py3.8 to py3.9 ([#14701](https://github.com/DataDog/integrations-core/pull/14701))

## 2.10.0 / 2023-04-14 / Agent 7.45.0

***Added***:

* Implement StartTLS protocol for MySQL ([#14352](https://github.com/DataDog/integrations-core/pull/14352)) Thanks [dpavlov-smartling](https://github.com/dpavlov-smartling).

## 2.9.1 / 2022-12-09 / Agent 7.42.0

***Fixed***:

* Update `cryptography` dependency ([#13367](https://github.com/DataDog/integrations-core/pull/13367))
* Remove `default_backend` parameter from cryptography calls ([#13333](https://github.com/DataDog/integrations-core/pull/13333))

## 2.9.0 / 2022-08-05 / Agent 7.39.0

***Added***:

* Implement StartTLS protocol for postgres ([#12596](https://github.com/DataDog/integrations-core/pull/12596)) Thanks [krogon](https://github.com/krogon).

## 2.8.0 / 2022-04-05 / Agent 7.36.0

***Added***:

* Upgrade dependencies ([#11726](https://github.com/DataDog/integrations-core/pull/11726))
* Add metric_patterns options to filter all metric submission by a list of regexes ([#11695](https://github.com/DataDog/integrations-core/pull/11695))

***Fixed***:

* Support newer versions of `click` ([#11746](https://github.com/DataDog/integrations-core/pull/11746))

## 2.7.0 / 2022-02-19 / Agent 7.35.0

***Added***:

* Add `pyproject.toml` file ([#11447](https://github.com/DataDog/integrations-core/pull/11447))

***Fixed***:

* Fix namespace packaging on Python 2 ([#11532](https://github.com/DataDog/integrations-core/pull/11532))

## 2.6.2 / 2022-02-04

***Fixed***:

* Check intermediate certificate protocol version ([#11207](https://github.com/DataDog/integrations-core/pull/11207))

## 2.6.1 / 2022-01-08 / Agent 7.34.0

***Fixed***:

* Add comment to autogenerated model files ([#10945](https://github.com/DataDog/integrations-core/pull/10945))

## 2.6.0 / 2021-10-04 / Agent 7.32.0

***Added***:

* Update dependencies ([#10258](https://github.com/DataDog/integrations-core/pull/10258))
* Update dependencies ([#10228](https://github.com/DataDog/integrations-core/pull/10228))
* Disable generic tags ([#10027](https://github.com/DataDog/integrations-core/pull/10027))

***Fixed***:

* Add server as generic tag ([#10100](https://github.com/DataDog/integrations-core/pull/10100))

## 2.5.0 / 2021-05-27 / Agent 7.28.1

***Added***:

* Add runtime configuration validation ([#8996](https://github.com/DataDog/integrations-core/pull/8996))

***Fixed***:

* Do not use check inheritance ([#9433](https://github.com/DataDog/integrations-core/pull/9433))

## 2.4.0 / 2021-04-19 / Agent 7.28.0

***Added***:

* Add an option to send certificate duration ([#9067](https://github.com/DataDog/integrations-core/pull/9067)) Thanks [lindleywhite](https://github.com/lindleywhite).
* Upgrade cryptography to 3.4.6 on Python 3 ([#8764](https://github.com/DataDog/integrations-core/pull/8764))

***Fixed***:

* Refactor TLS check ([#8792](https://github.com/DataDog/integrations-core/pull/8792))
* Add more debug lines ([#8787](https://github.com/DataDog/integrations-core/pull/8787))

## 2.3.0 / 2021-03-07 / Agent 7.27.0

***Security***:

* Upgrade cryptography python package ([#8611](https://github.com/DataDog/integrations-core/pull/8611))

***Fixed***:

* Include validate_cert in backwards compatibility remapper ([#8543](https://github.com/DataDog/integrations-core/pull/8543))

## 2.2.0 / 2021-02-03

***Added***:

* Implement AIA chasing ([#8521](https://github.com/DataDog/integrations-core/pull/8521))

***Fixed***:

* Remove outdated description of `local_cert_path` option ([#8500](https://github.com/DataDog/integrations-core/pull/8500))
* Bump minimum package ([#8443](https://github.com/DataDog/integrations-core/pull/8443))

## 2.1.0 / 2021-01-28

***Security***:

* Upgrade cryptography python package ([#8476](https://github.com/DataDog/integrations-core/pull/8476))

## 2.0.0 / 2021-01-25

***Changed***:

* Update TLS check to use TLS context wrapper ([#8230](https://github.com/DataDog/integrations-core/pull/8230))

## 1.8.0 / 2020-10-31 / Agent 7.24.0

***Security***:

* Upgrade `cryptography` dependency ([#7869](https://github.com/DataDog/integrations-core/pull/7869))

## 1.7.0 / 2020-10-14

***Added***:

* Adding debug logging to tls check ([#7664](https://github.com/DataDog/integrations-core/pull/7664))

## 1.6.0 / 2020-09-21 / Agent 7.23.0

***Added***:

* Add config spec ([#7529](https://github.com/DataDog/integrations-core/pull/7529))

## 1.5.0 / 2020-05-17 / Agent 7.20.0

***Added***:

* Allow optional dependency installation for all checks ([#6589](https://github.com/DataDog/integrations-core/pull/6589))

## 1.4.1 / 2020-02-12 / Agent 7.18.0

***Fixed***:

* Don't rely on file extension for local cert loading ([#5694](https://github.com/DataDog/integrations-core/pull/5694))

## 1.4.0 / 2020-01-13 / Agent 7.17.0

***Added***:

* Use lazy logging format ([#5398](https://github.com/DataDog/integrations-core/pull/5398))

## 1.3.0 / 2019-12-02 / Agent 7.16.0

***Added***:

* Upgrade cryptography to 2.8 ([#5047](https://github.com/DataDog/integrations-core/pull/5047))

## 1.2.0 / 2019-07-04 / Agent 6.13.0

***Added***:

* Update cryptography version ([#4000](https://github.com/DataDog/integrations-core/pull/4000))

## 1.1.0 / 2019-06-24

***Added***:

* Allow certificate validation to be completely disabled ([#3966](https://github.com/DataDog/integrations-core/pull/3966))

## 1.0.0 / 2019-04-22 / Agent 6.12.0

***Added***:

* Add TLS integration ([#3256](https://github.com/DataDog/integrations-core/pull/3256))
