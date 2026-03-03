# Huawei UPS Checkmk Plugin

Checkmk SNMP plugin for monitoring Huawei UPS2000 systems.

## Features

Monitors Huawei UPS devices via SNMP with ~34 services:

| Category | Services | Thresholds |
|----------|----------|------------|
| Alarms | UPS Alarm Check | State-based |
| Status | Power Supply Method, Battery State | State-based |
| Environment | Ambient Temperature, Ambient Humidity | Configurable |
| Device | Device Temperature | Configurable |
| Input | Phase A/B/C Voltage, Frequency, Phase A/B/C Current | Configurable (voltage, frequency) |
| Output | Phase A/B/C Voltage, Frequency, Phase A/B/C Current | Configurable (voltage, frequency) |
| Output Power | Phase A/B/C Active Power, Phase A/B/C Apparent Power | Info only |
| Output Load | Phase A/B/C Load | Configurable |
| Battery | Voltage, Current, Capacity, Backup Time, Temperature | Configurable (capacity, time, temperature) |

All configurable thresholds can be adjusted through Checkmk's WATO GUI.

## SNMP Detection

The plugin detects Huawei UPS devices where:
- OID `.1.3.6.1.2.1.33.1.1.1.0` starts with `HUAWEI`
- OID `.1.3.6.1.2.1.33.1.1.2.0` starts with `UPS`

## Installation

### MKP Package (recommended)

Download the latest `.mkp` file from the
[Releases](https://github.com/oposs/cmk-oposs_huawei_ups/releases) page and
install it:

```bash
mkp install oposs_huawei_ups-<version>.mkp
```

### Manual Installation

Copy the plugin files into your Checkmk site:

```
local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/
├── agent_based/
│   └── oposs_huawei_ups.py
├── graphing/
│   └── huawei_ups.py
└── rulesets/
    └── huawei_ups.py
```

## Troubleshooting

Test SNMP connectivity:

```bash
snmpget -v2c -c <community> <host> .1.3.6.1.2.1.33.1.1.1.0
```

Expected output contains `HUAWEI`.

## License

MIT - OETIKER+PARTNER AG
