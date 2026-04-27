# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### New

### Changed
- Removed the metric translation for the legacy `output_frequency` check.
  That v1 check read the wrong SNMP OID (`hwUpsInputCurrentC` instead of
  the actual output frequency); merging the bogus historical values into
  the now-correct Output Frequency graph would visually corrupt it. The
  legacy `frequency.rrd` for that service stays on disk but is no longer
  queried.

### Fixed
- Metric translations for legacy `huawei_ups_*` history are now keyed on
  the *new* check commands (`oposs_huawei_ups_*`) so they actually fire.
  Previously they were keyed on the now-uninstalled legacy commands and
  Checkmk's translation lookup (an exact match on the live service's
  current check command) silently missed them — leaving the legacy RRD
  data orphaned in the per-service directories. After upgrading and
  reloading (`cmk -R` / `omd restart apache`), graphs of the new
  `oposs_huawei_*` services on hosts that previously ran the legacy
  oegig plugin will show one continuous line spanning the pre- and
  post-upgrade history.

## 0.2.0 - 2026-04-27
### Changed
- Render zero-anchored single-metric graphs as filled areas instead of thin
  lines for better readability (voltage and frequency graphs remain lines
  because their y-axis baseline is non-zero)

## 0.1.1 - 2026-03-24
### Fixed
- Fix ruleset topic: use `Topic.ENVIRONMENTAL` instead of incorrect `Topic.ENVIRONMENT`

## 0.1.0 - 2026-03-04
### New
- Initial migration from oegig-plugins to Checkmk 2.3.x v2 API
- Data-driven architecture: targets list + closure generates ~34 check plugins
- Graphing definitions for all metric types (temperature, voltage, current,
  frequency, power, load, battery capacity, backup time, humidity)
- Custom WATO rulesets for configurable thresholds
- Metric names prefixed with `oposs_huawei_` for namespace isolation
- MKP packaging via oposs/mkp-builder GitHub Action

### Fixed
- Output Frequency check now fetches from output table (4.100.1.7)
  instead of input table (3.100.1.7) where it was reading input current C


