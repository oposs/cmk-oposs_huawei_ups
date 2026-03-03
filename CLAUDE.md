# cmk-oposs_huawei_ups

Checkmk SNMP plugin for Huawei UPS2000 systems.
Migrated from oegig-plugins to Checkmk 2.3.x v2 API.

## Components

- `local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/agent_based/oposs_huawei_ups.py` — SNMP sections + ~34 check plugins
- `local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/graphing/huawei_ups.py` — metric, graph, perfometer definitions
- `local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/rulesets/huawei_ups.py` — WATO ruleset definitions
- `.mkp-builder.ini` — MKP packaging config
- `.github/workflows/release.yml` — automated release workflow

## Architecture

- Data-driven design: `targets` list defines all checks declaratively
- `_make_plugins()` closure generates module-level variables via `globals()`
- Each target gets its own `SimpleSNMPSection` + `CheckPlugin`
- Two check patterns: state-mapping (Result) and check_levels (with params)
- SNMP detection: sysDescr starts with "HUAWEI" AND sysName starts with "UPS"
- Metric prefix: `oposs_huawei_`
- Custom WATO rulesets for checks with configurable thresholds
