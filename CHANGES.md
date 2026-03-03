# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### New

- Initial migration from oegig-plugins to Checkmk 2.3.x v2 API
- Data-driven architecture: targets list + closure generates ~34 check plugins
- Graphing definitions for all metric types (temperature, voltage, current,
  frequency, power, load, battery capacity, backup time, humidity)
- Custom WATO rulesets for configurable thresholds
- Metric names prefixed with `oposs_huawei_` for namespace isolation
- MKP packaging via oposs/mkp-builder GitHub Action

### Changed

### Fixed

- Output Frequency check now fetches from output table (4.100.1.7)
  instead of input table (3.100.1.7) where it was reading input current C
