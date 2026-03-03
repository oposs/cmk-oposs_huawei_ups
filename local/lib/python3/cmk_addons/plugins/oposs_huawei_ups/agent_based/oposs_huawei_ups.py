#!/usr/bin/env python3

from collections import namedtuple

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    all_of,
    check_levels,
    startswith,
)

# Huawei UPS SNMP OID base
OB = ".1.3.6.1.4.1.2011.6.174.1."

# SNMP detection: sysDescr starts with "HUAWEI" AND sysName starts with "UPS"
DETECT_HUAWEI_UPS = all_of(
    startswith(".1.3.6.1.2.1.33.1.1.1.0", "HUAWEI"),
    startswith(".1.3.6.1.2.1.33.1.1.2.0", "UPS"),
)

POWER_SUPPLY_MAP = {
    "0": "UNKNOWN",
    "1": "no power supply",
    "2": "bypass mode",
    "3": "normal mode",
    "4": "battery mode",
    "5": "combined mode",
    "6": "mains ECO mode",
    "7": "battery ECO mode",
}

BATTERY_STATE_MAP = {
    "0": "UNKNOWN state",
    "1": "no battery connected",
    "2": "not charging or discharging",
    "3": "hibernation",
    "4": "float charging",
    "5": "equalized charging",
    "6": "discharging",
}

# ---------------------------------------------------------------------------
# Target definitions — each entry generates one SimpleSNMPSection + CheckPlugin
#
# Two patterns:
#   'result' key → state-mapping check (no params, no levels)
#   otherwise    → check_levels check (with params, configurable thresholds)
#
# For check_levels targets:
#   scale         — multiply raw SNMP int by this factor
#   metric_name   — prefixed metric name for perfdata
#   render_func   — display formatter
#   default_params — SimpleLevels format: {"levels_upper": ("fixed", (w,c))}
#   boundaries    — graph boundaries tuple
#   ruleset_name  — shared WATO ruleset name (optional)
# ---------------------------------------------------------------------------

targets = [
    # --- State-mapping checks ---
    {
        "name": "UPS Alarm Check",
        "query": SNMPTree(base=".1.3.6.1.2.1.33.1.6", oids=["1"]),
        "keys": ["upsAlarmPresent"],
        "result": lambda obj, cfg: Result(
            state=State.OK if obj.upsAlarmPresent == "0" else State.CRIT,
            summary="%s Alarms present - check online status!"
            % obj.upsAlarmPresent
            if obj.upsAlarmPresent != "0"
            else "No Alarms",
        ),
    },
    {
        "name": "Power Supply Method",
        "query": SNMPTree(base=OB + "2.101", oids=["1.1"]),
        "keys": ["method"],
        "result": lambda obj, cfg: Result(
            state=State.UNKNOWN
            if obj.method == "0"
            else State.CRIT
            if obj.method == "1"
            else State.OK,
            summary=POWER_SUPPLY_MAP.get(obj.method, "unknown(%s)" % obj.method),
        ),
    },
    {
        "name": "Battery State",
        "query": SNMPTree(base=OB + "2.101", oids=["1.3"]),
        "keys": ["state"],
        "result": lambda obj, cfg: Result(
            state=State.UNKNOWN
            if obj.state == "0"
            else State.CRIT
            if obj.state == "1"
            else State.OK,
            summary=BATTERY_STATE_MAP.get(obj.state, "unknown(%s)" % obj.state),
        ),
    },
    # --- Environment ---
    {
        "name": "Ambient Temperature",
        "query": SNMPTree(base=OB + "1.1", oids=["6.0"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_temperature",
        "render_func": lambda v: "%.0f \u00b0C" % v,
        "default_params": {"levels_upper": ("fixed", (40.0, 50.0))},
        "boundaries": (0.0, 120.0),
        "ruleset_name": "oposs_huawei_ups_ambient_temperature",
    },
    {
        "name": "Ambient Humidity",
        "query": SNMPTree(base=OB + "1.1", oids=["7.0"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_humidity",
        "render_func": lambda v: "%.0f %%" % v,
        "default_params": {"levels_upper": ("fixed", (83.0, 86.0))},
        "boundaries": (0.0, 100.0),
        "ruleset_name": "oposs_huawei_ups_ambient_humidity",
    },
    # --- Device ---
    {
        "name": "Device Temperature",
        "query": SNMPTree(base=OB + "2.101", oids=["1.4"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_temperature",
        "render_func": lambda v: "%.0f \u00b0C" % v,
        "default_params": {"levels_upper": ("fixed", (60.0, 70.0))},
        "boundaries": (0.0, 100.0),
        "ruleset_name": "oposs_huawei_ups_device_temperature",
    },
    # --- Input Voltage (per-phase) ---
    *(
        {
            "name": "Phase %s Input Voltage" % name,
            "query": SNMPTree(base=OB + "3.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 0.1,
            "metric_name": "oposs_huawei_voltage",
            "render_func": lambda v: "%.0f V" % v,
            "default_params": {"levels_lower": ("fixed", (210.0, 180.0))},
            "boundaries": (0.0, 250.0),
            "ruleset_name": "oposs_huawei_ups_input_voltage",
        }
        for name, oid in [("A", "1"), ("B", "2"), ("C", "3")]
    ),
    # --- Input Frequency ---
    {
        "name": "Input Frequency",
        "query": SNMPTree(base=OB + "3.100", oids=["1.4"]),
        "keys": ["value"],
        "scale": 0.01,
        "metric_name": "oposs_huawei_frequency",
        "render_func": lambda v: "%.2f Hz" % v,
        "default_params": {
            "levels_lower": ("fixed", (49.0, 48.0)),
            "levels_upper": ("fixed", (51.0, 52.0)),
        },
        "boundaries": (0.0, 100.0),
        "ruleset_name": "oposs_huawei_ups_input_frequency",
    },
    # --- Input Current (per-phase, info only) ---
    *(
        {
            "name": "Phase %s Input Current" % name,
            "query": SNMPTree(base=OB + "3.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 0.1,
            "metric_name": "oposs_huawei_current",
            "render_func": lambda v: "%.0f A" % v,
            "default_params": {},
            "boundaries": (0.0, 1000.0),
        }
        for name, oid in [("A", "5"), ("B", "6"), ("C", "7")]
    ),
    # --- Output Voltage (per-phase) ---
    *(
        {
            "name": "Phase %s Output Voltage" % name,
            "query": SNMPTree(base=OB + "4.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 0.1,
            "metric_name": "oposs_huawei_voltage",
            "render_func": lambda v: "%.0f V" % v,
            "default_params": {"levels_lower": ("fixed", (210.0, 180.0))},
            "boundaries": (0.0, 250.0),
            "ruleset_name": "oposs_huawei_ups_output_voltage",
        }
        for name, oid in [("A", "1"), ("B", "2"), ("C", "3")]
    ),
    # --- Output Current (per-phase, info only) ---
    *(
        {
            "name": "Phase %s Output Current" % name,
            "query": SNMPTree(base=OB + "4.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 0.1,
            "metric_name": "oposs_huawei_current",
            "render_func": lambda v: "%.0f A" % v,
            "default_params": {},
            "boundaries": (0.0, 1000.0),
        }
        for name, oid in [("A", "4"), ("B", "5"), ("C", "6")]
    ),
    # --- Output Frequency (NOTE: fixed OID — was erroneously reading from input table) ---
    {
        "name": "Output Frequency",
        "query": SNMPTree(base=OB + "4.100", oids=["1.7"]),
        "keys": ["value"],
        "scale": 0.01,
        "metric_name": "oposs_huawei_frequency",
        "render_func": lambda v: "%.2f Hz" % v,
        "default_params": {
            "levels_lower": ("fixed", (49.0, 48.0)),
            "levels_upper": ("fixed", (51.0, 52.0)),
        },
        "boundaries": (0.0, 100.0),
        "ruleset_name": "oposs_huawei_ups_output_frequency",
    },
    # --- Output Active Power (per-phase, info only) ---
    *(
        {
            "name": "Phase %s Output Active Power" % name,
            "query": SNMPTree(base=OB + "4.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 100.0,
            "metric_name": "oposs_huawei_active_power",
            "render_func": lambda v: "%.2f kW" % (v / 1000.0),
            "default_params": {},
            "boundaries": (-1200.0, 1200.0),
        }
        for name, oid in [("A", "8"), ("B", "9"), ("C", "10")]
    ),
    # --- Output Apparent Power (per-phase, info only) ---
    *(
        {
            "name": "Phase %s Output Apparent Power" % name,
            "query": SNMPTree(base=OB + "4.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 100.0,
            "metric_name": "oposs_huawei_apparent_power",
            "render_func": lambda v: "%.1f kVA" % (v / 1000.0),
            "default_params": {},
            "boundaries": (-1200.0, 1200.0),
        }
        for name, oid in [("A", "11"), ("B", "12"), ("C", "13")]
    ),
    # --- Output Load (per-phase) ---
    *(
        {
            "name": "Phase %s Output Load" % name,
            "query": SNMPTree(base=OB + "4.100", oids=["1.%s" % oid]),
            "keys": ["value"],
            "scale": 0.1,
            "metric_name": "oposs_huawei_load_pct",
            "render_func": lambda v: "%.1f %%" % v,
            "default_params": {"levels_upper": ("fixed", (80.0, 90.0))},
            "boundaries": (0.0, 500.0),
            "ruleset_name": "oposs_huawei_ups_output_load",
        }
        for name, oid in [("A", "14"), ("B", "15"), ("C", "16")]
    ),
    # --- Battery ---
    {
        "name": "Battery Voltage",
        "query": SNMPTree(base=OB + "6.100", oids=["1.1"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_voltage",
        "render_func": lambda v: "%.1f V" % v,
        "default_params": {},
        "boundaries": (0.0, 2000.0),
    },
    {
        "name": "Battery Current",
        "query": SNMPTree(base=OB + "6.100", oids=["1.2"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_current",
        "render_func": lambda v: "%.1f A" % v,
        "default_params": {},
        "boundaries": (-300.0, 300.0),
    },
    {
        "name": "Battery Capacity Left",
        "query": SNMPTree(base=OB + "6.100", oids=["1.3"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_battery_pct",
        "render_func": lambda v: "%.1f %%" % v,
        "default_params": {"levels_lower": ("fixed", (15.0, 10.0))},
        "boundaries": (0.0, 100.0),
        "ruleset_name": "oposs_huawei_ups_battery_capacity",
    },
    {
        "name": "Battery Backup Time",
        "query": SNMPTree(base=OB + "6.100", oids=["1.4"]),
        "keys": ["value"],
        "scale": 1.0,
        "metric_name": "oposs_huawei_backup_time",
        "render_func": lambda v: "%.1fh" % (v / 3600.0),
        "default_params": {"levels_lower": ("fixed", (1200.0, 600.0))},
        "boundaries": (0.0, 172800.0),
        "ruleset_name": "oposs_huawei_ups_battery_backup_time",
    },
    {
        "name": "Battery Temperature",
        "query": SNMPTree(base=OB + "6.100", oids=["1.6"]),
        "keys": ["value"],
        "scale": 0.1,
        "metric_name": "oposs_huawei_temperature",
        "render_func": lambda v: "%.0f \u00b0C" % v,
        "default_params": {"levels_upper": ("fixed", (60.0, 70.0))},
        "boundaries": (0.0, 80.0),
        "ruleset_name": "oposs_huawei_ups_battery_temperature",
    },
]


# ---------------------------------------------------------------------------
# Dynamic plugin generation
# ---------------------------------------------------------------------------


def _make_plugins(cfg):
    """Generate SimpleSNMPSection + CheckPlugin module-level variables."""
    check_key = "oposs_huawei_ups_%s" % cfg["name"].lower().replace(" ", "_")
    obj_class = namedtuple(check_key, cfg["keys"])

    def parse_fn(string_table):
        for row in string_table:
            return obj_class(*row)
        return None

    def discovery_fn(section):
        if section:
            yield Service()

    if "result" in cfg:
        # State-mapping check — no params
        def check_fn(section):
            if not section:
                return
            yield cfg["result"](section, cfg)

        cp_kwargs = {}
    else:
        # check_levels check — with params
        def check_fn(params, section):
            if not section:
                return
            value = cfg.get("scale", 1.0) * float(section.value)
            yield from check_levels(
                value=value,
                levels_upper=params.get("levels_upper"),
                levels_lower=params.get("levels_lower"),
                boundaries=cfg.get("boundaries"),
                metric_name=cfg["metric_name"],
                render_func=cfg["render_func"],
                label=cfg["name"],
            )

        cp_kwargs = {
            "check_default_parameters": cfg["default_params"],
        }
        if "ruleset_name" in cfg:
            cp_kwargs["check_ruleset_name"] = cfg["ruleset_name"]

    globals()["snmp_section_%s" % check_key] = SimpleSNMPSection(
        name=check_key,
        detect=DETECT_HUAWEI_UPS,
        parse_function=parse_fn,
        fetch=cfg["query"],
    )

    globals()["check_plugin_%s" % check_key] = CheckPlugin(
        name=check_key,
        sections=[check_key],
        service_name=cfg["name"],
        discovery_function=discovery_fn,
        check_function=check_fn,
        **cp_kwargs,
    )


for _cfg in targets:
    _make_plugins(_cfg)
