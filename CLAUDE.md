# cmk-oposs_huawei_ups

Checkmk SNMP plugin for Huawei UPS2000 systems.
Migrated from oegig-plugins to Checkmk 2.3.x v2 API.

## Components

- `local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/agent_based/oposs_huawei_ups.py` — SNMP sections + ~34 check plugins
- `local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/graphing/huawei_ups.py` — metric, graph, perfometer definitions
- `local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/rulesets/huawei_ups.py` — WATO ruleset definitions
- `.mkp-builder.ini` — MKP packaging config
- `.github/workflows/` — CI and the release flow, callers of the oposs/repo-infra workflows (`ci.yml`, `changelog.yml`, `release-pr.yml`, `release-build.yml`, `release-publish.yml`)
- `tests/` — pytest suite against the real Checkmk 2.3.0 API (`pytest -q`)

## Architecture

- Data-driven design: `targets` list defines all checks declaratively
- `_make_plugins()` closure generates module-level variables via `globals()`
- Each target gets its own `SimpleSNMPSection` + `CheckPlugin`
- Two check patterns: state-mapping (Result) and check_levels (with params)
- SNMP detection (UPS-MIB): upsIdentManufacturer (`.1.3.6.1.2.1.33.1.1.1.0`) starts with "HUAWEI" AND upsIdentModel (`.1.3.6.1.2.1.33.1.1.2.0`) starts with "UPS"
- Phase B and C plugins take a second section, `oposs_huawei_ups_numlines` (UPS-MIB upsInputNumLines/upsOutputNumLines), and are discovered only when their direction has 3 lines or no count; their functions get generated `section_<name>` signatures
- A levels value of 2147483647 means "no value": not discovered, UNKNOWN in the check
- `tests/data/ups2000_3kva.walk` is an anonymized walk of a real single-phase UPS2000 3kVA, used by `tests/test_real_walk.py`
- Metric prefix: `oposs_huawei_`
- Custom WATO rulesets for checks with configurable thresholds
