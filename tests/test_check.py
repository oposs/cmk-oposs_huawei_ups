"""The 34 Huawei UPS2000 checks, fed with SNMP rows as Checkmk fetches them.

Every target in the check module becomes one SNMP section that fetches a
single column, so the string table of a one-module UPS2000 is one row with
one raw integer, e.g. [["2301"]] for 230.1 V. The device reports voltages,
currents, temperatures, humidity and load in 0.1 units, frequencies in
0.01 Hz, power in 0.1 kW / 0.1 kVA and the backup time in seconds.
"""

import importlib.util
import pathlib
import re
import sys

import pytest
from cmk.agent_based.v2 import (
    CheckPlugin,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    State,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECK = ROOT / "local/lib/python3/cmk_addons/plugins/oposs_huawei_ups/agent_based/oposs_huawei_ups.py"
OB = ".1.3.6.1.4.1.2011.6.174.1."


@pytest.fixture(scope="module")
def check():
    name = "test_oposs_huawei_ups_check"
    spec = importlib.util.spec_from_file_location(name, CHECK)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    yield module
    sys.modules.pop(name, None)


def _plugins(check):
    return {v.service_name: v for v in vars(check).values() if isinstance(v, CheckPlugin)}


def _sections(check):
    return {v.name: v for v in vars(check).values() if isinstance(v, SimpleSNMPSection)}


def _run(check, service, rows, params=None):
    """Parse, discover and check one service the way Checkmk does."""
    plugin = _plugins(check)[service]
    (section_name,) = plugin.sections
    # Checkmk hands the parse function one table per SNMPTree in fetch.
    section = _sections(check)[section_name].parse_function([rows])
    discovered = list(plugin.discovery_function(section))
    if params is None:
        params = plugin.check_default_parameters
    if params is None:
        out = list(plugin.check_function(section))
    else:
        out = list(plugin.check_function(params, section))
    return discovered, out


def _result(out):
    (result,) = [r for r in out if isinstance(r, Result)]
    return result


def _metric(out):
    (metric,) = [m for m in out if isinstance(m, Metric)]
    return metric


# --- registration -----------------------------------------------------------

SERVICES = [
    "UPS Alarm Check", "Power Supply Method", "Battery State",
    "Ambient Temperature", "Ambient Humidity", "Device Temperature",
    *(f"Phase {p} Input Voltage" for p in "ABC"),
    "Input Frequency",
    *(f"Phase {p} Input Current" for p in "ABC"),
    *(f"Phase {p} Output Voltage" for p in "ABC"),
    *(f"Phase {p} Output Current" for p in "ABC"),
    "Output Frequency",
    *(f"Phase {p} Output Active Power" for p in "ABC"),
    *(f"Phase {p} Output Apparent Power" for p in "ABC"),
    *(f"Phase {p} Output Load" for p in "ABC"),
    "Battery Voltage", "Battery Current", "Battery Capacity Left",
    "Battery Backup Time", "Battery Temperature",
]

# Where each service reads its value (HUAWEI-UPS-MIB, one column each).
OIDS = {
    "UPS Alarm Check": ".1.3.6.1.2.1.33.1.6.1",
    "Power Supply Method": OB + "2.101.1.1",
    "Battery State": OB + "2.101.1.3",
    "Ambient Temperature": OB + "1.1.6.0",
    "Ambient Humidity": OB + "1.1.7.0",
    "Device Temperature": OB + "2.101.1.4",
    **{f"Phase {p} Input Voltage": OB + f"3.100.1.{i}" for p, i in zip("ABC", (1, 2, 3))},
    "Input Frequency": OB + "3.100.1.4",
    **{f"Phase {p} Input Current": OB + f"3.100.1.{i}" for p, i in zip("ABC", (5, 6, 7))},
    **{f"Phase {p} Output Voltage": OB + f"4.100.1.{i}" for p, i in zip("ABC", (1, 2, 3))},
    **{f"Phase {p} Output Current": OB + f"4.100.1.{i}" for p, i in zip("ABC", (4, 5, 6))},
    "Output Frequency": OB + "4.100.1.7",
    **{f"Phase {p} Output Active Power": OB + f"4.100.1.{i}" for p, i in zip("ABC", (8, 9, 10))},
    **{f"Phase {p} Output Apparent Power": OB + f"4.100.1.{i}" for p, i in zip("ABC", (11, 12, 13))},
    **{f"Phase {p} Output Load": OB + f"4.100.1.{i}" for p, i in zip("ABC", (14, 15, 16))},
    "Battery Voltage": OB + "6.100.1.1",
    "Battery Current": OB + "6.100.1.2",
    "Battery Capacity Left": OB + "6.100.1.3",
    "Battery Backup Time": OB + "6.100.1.4",
    "Battery Temperature": OB + "6.100.1.6",
}


def test_every_service_is_registered_once(check):
    plugins = _plugins(check)
    assert sorted(plugins) == sorted(SERVICES)
    assert len({p.name for p in plugins.values()}) == len(SERVICES)


def test_check_names_follow_the_service_names(check):
    # The translations and the RRD directories depend on these names.
    for service, plugin in _plugins(check).items():
        assert plugin.name == "oposs_huawei_ups_" + service.lower().replace(" ", "_")
        assert plugin.sections == [plugin.name]


@pytest.mark.parametrize("service", SERVICES)
def test_service_reads_its_oid(check, service):
    plugin = _plugins(check)[service]
    (tree,) = _sections(check)[plugin.name].fetch
    (oid,) = tree.oids
    assert f"{tree.base}.{oid.column}" == OIDS[service]


def test_output_frequency_does_not_read_input_current_c(check):
    # The legacy check read hwUpsInputCurrentC (3.100.1.7) for this service.
    sections = _sections(check)
    (out_freq,) = sections["oposs_huawei_ups_output_frequency"].fetch
    (in_current_c,) = sections["oposs_huawei_ups_phase_c_input_current"].fetch
    assert (out_freq.base, out_freq.oids) != (in_current_c.base, in_current_c.oids)


def test_no_two_services_read_the_same_oid(check):
    fetched = [f"{t.base}.{t.oids[0].column}" for s in _sections(check).values() for t in s.fetch]
    assert len(fetched) == len(set(fetched)) == len(SERVICES)


# --- SNMP detection ---------------------------------------------------------

def _detects(spec, values):
    """Evaluate a detect specification as Checkmk does: OR of ANDs of regexes."""
    return any(
        all(bool(re.fullmatch(regex, values.get(oid, ""), re.DOTALL)) is flag
            for oid, regex, flag in conjunction)
        for conjunction in spec
    )


UPS2000 = {
    ".1.3.6.1.2.1.33.1.1.1.0": "HUAWEI",    # upsIdentManufacturer
    ".1.3.6.1.2.1.33.1.1.2.0": "UPS2000",   # upsIdentModel
}


def test_detects_a_huawei_ups2000(check):
    assert _detects(check.DETECT_HUAWEI_UPS, UPS2000)


@pytest.mark.parametrize("values", [
    {**UPS2000, ".1.3.6.1.2.1.33.1.1.1.0": "APC"},
    {**UPS2000, ".1.3.6.1.2.1.33.1.1.2.0": "SmartLi"},
    {},
], ids=["other-vendor", "other-model", "no-ups-mib"])
def test_ignores_other_devices(check, values):
    assert not _detects(check.DETECT_HUAWEI_UPS, values)


def test_every_section_uses_the_same_detection(check):
    for section in _sections(check).values():
        assert section.detect == check.DETECT_HUAWEI_UPS


# --- parse and discovery ----------------------------------------------------

@pytest.mark.parametrize("service", SERVICES)
def test_no_rows_means_no_service_and_no_result(check, service):
    discovered, out = _run(check, service, [])
    assert discovered == []
    assert out == []


@pytest.mark.parametrize("service", SERVICES)
def test_a_row_creates_one_itemless_service(check, service):
    discovered, _ = _run(check, service, [["3"]])
    assert discovered == [Service()]


def test_parse_takes_the_first_table_row(check):
    section = _sections(check)["oposs_huawei_ups_battery_voltage"]
    assert section.parse_function([[["2160"], ["9999"]]]).value == "2160"


# --- state checks -----------------------------------------------------------

def test_no_alarm_is_ok(check):
    _, out = _run(check, "UPS Alarm Check", [["0"]])
    assert out == [Result(state=State.OK, summary="No Alarms")]


def test_present_alarms_are_crit(check):
    _, out = _run(check, "UPS Alarm Check", [["2"]])
    assert out == [Result(state=State.CRIT, summary="2 Alarms present - check online status!")]


@pytest.mark.parametrize("raw, state, summary", [
    ("0", State.UNKNOWN, "UNKNOWN"),
    ("1", State.CRIT, "no power supply"),
    ("2", State.OK, "bypass mode"),
    ("3", State.OK, "normal mode"),
    ("4", State.OK, "battery mode"),
    ("5", State.OK, "combined mode"),
    ("6", State.OK, "mains ECO mode"),
    ("7", State.OK, "battery ECO mode"),
    ("9", State.OK, "unknown(9)"),
])
def test_power_supply_method(check, raw, state, summary):
    _, out = _run(check, "Power Supply Method", [[raw]])
    assert out == [Result(state=state, summary=summary)]


@pytest.mark.parametrize("raw, state, summary", [
    ("0", State.UNKNOWN, "UNKNOWN state"),
    ("1", State.CRIT, "no battery connected"),
    ("2", State.OK, "not charging or discharging"),
    ("3", State.OK, "hibernation"),
    ("4", State.OK, "float charging"),
    ("5", State.OK, "equalized charging"),
    ("6", State.OK, "discharging"),
    ("8", State.OK, "unknown(8)"),
])
def test_battery_state(check, raw, state, summary):
    _, out = _run(check, "Battery State", [[raw]])
    assert out == [Result(state=state, summary=summary)]


# --- levels checks ----------------------------------------------------------

# service, metric, raw value, value after scaling, summary
NORMAL = [
    ("Ambient Temperature", "oposs_huawei_temperature", "231", 23.1, "Ambient Temperature: 23 °C"),
    ("Ambient Humidity", "oposs_huawei_humidity", "452", 45.2, "Ambient Humidity: 45 %"),
    ("Device Temperature", "oposs_huawei_temperature", "352", 35.2, "Device Temperature: 35 °C"),
    ("Phase A Input Voltage", "oposs_huawei_voltage", "2301", 230.1, "Phase A Input Voltage: 230 V"),
    ("Input Frequency", "oposs_huawei_frequency", "5001", 50.01, "Input Frequency: 50.01 Hz"),
    ("Phase B Input Current", "oposs_huawei_current", "123", 12.3, "Phase B Input Current: 12 A"),
    ("Phase C Output Voltage", "oposs_huawei_voltage", "2299", 229.9, "Phase C Output Voltage: 230 V"),
    ("Phase A Output Current", "oposs_huawei_current", "87", 8.7, "Phase A Output Current: 9 A"),
    ("Output Frequency", "oposs_huawei_frequency", "4998", 49.98, "Output Frequency: 49.98 Hz"),
    ("Phase B Output Active Power", "oposs_huawei_active_power", "18", 1800.0,
     "Phase B Output Active Power: 1.80 kW"),
    ("Phase C Output Apparent Power", "oposs_huawei_apparent_power", "21", 2100.0,
     "Phase C Output Apparent Power: 2.1 kVA"),
    ("Phase A Output Load", "oposs_huawei_load_pct", "235", 23.5, "Phase A Output Load: 23.5 %"),
    ("Battery Voltage", "oposs_huawei_voltage", "2160", 216.0, "Battery Voltage: 216.0 V"),
    ("Battery Current", "oposs_huawei_current", "-45", -4.5, "Battery Current: -4.5 A"),
    ("Battery Capacity Left", "oposs_huawei_battery_pct", "1000", 100.0, "Battery Capacity Left: 100.0 %"),
    ("Battery Backup Time", "oposs_huawei_backup_time", "5400", 5400.0, "Battery Backup Time: 1.5h"),
    ("Battery Temperature", "oposs_huawei_temperature", "255", 25.5, "Battery Temperature: 26 °C"),
]


@pytest.mark.parametrize("service, metric, raw, value, summary", NORMAL, ids=[n[0] for n in NORMAL])
def test_normal_reading_is_ok_with_metric(check, service, metric, raw, value, summary):
    _, out = _run(check, service, [[raw]])
    result = _result(out)
    assert result.state == State.OK
    assert result.summary == summary
    emitted = _metric(out)
    assert emitted.name == metric
    assert emitted.value == pytest.approx(value)


# service, raw WARN value, raw CRIT value, levels as the summary shows them
LEVELS = [
    ("Ambient Temperature", "425", "512", "at 40 \u00b0C/50 \u00b0C"),
    ("Ambient Humidity", "840", "870", "at 83 %/86 %"),
    ("Device Temperature", "650", "720", "at 60 \u00b0C/70 \u00b0C"),
    ("Phase A Input Voltage", "2000", "1700", "below 210 V/180 V"),
    ("Phase B Input Voltage", "2000", "1700", "below 210 V/180 V"),
    ("Phase C Input Voltage", "2000", "1700", "below 210 V/180 V"),
    ("Input Frequency", "4880", "4750", "below 49.00 Hz/48.00 Hz"),
    ("Input Frequency", "5120", "5250", "at 51.00 Hz/52.00 Hz"),
    ("Phase A Output Voltage", "2000", "1700", "below 210 V/180 V"),
    ("Output Frequency", "4880", "4750", "below 49.00 Hz/48.00 Hz"),
    ("Output Frequency", "5120", "5250", "at 51.00 Hz/52.00 Hz"),
    ("Phase C Output Load", "850", "950", "at 80.0 %/90.0 %"),
    ("Battery Capacity Left", "120", "80", "below 15.0 %/10.0 %"),
    ("Battery Backup Time", "900", "300", "below 0.3h/0.2h"),
    ("Battery Temperature", "650", "750", "at 60 \u00b0C/70 \u00b0C"),
]


@pytest.mark.parametrize("service, warn, crit, levels", LEVELS, ids=[f"{n[0]}-{n[1]}" for n in LEVELS])
def test_default_levels_warn_and_crit(check, service, warn, crit, levels):
    for raw, state in ((warn, State.WARN), (crit, State.CRIT)):
        _, out = _run(check, service, [[raw]])
        result = _result(out)
        assert result.state == state, raw
        assert result.summary.endswith(f"(warn/crit {levels})"), result.summary


def test_upper_levels_go_into_the_metric(check):
    _, out = _run(check, "Ambient Temperature", [["231"]])
    assert _metric(out) == Metric("oposs_huawei_temperature", 23.1, levels=(40.0, 50.0), boundaries=(0.0, 120.0))


@pytest.mark.parametrize("service", [
    *(f"Phase {p} Input Current" for p in "ABC"),
    *(f"Phase {p} Output Current" for p in "ABC"),
    *(f"Phase {p} Output Active Power" for p in "ABC"),
    *(f"Phase {p} Output Apparent Power" for p in "ABC"),
    "Battery Voltage", "Battery Current",
])
def test_info_only_services_stay_ok(check, service):
    _, out = _run(check, service, [["99999"]])
    assert _result(out).state == State.OK


def test_rule_levels_replace_the_defaults(check):
    params = {"levels_upper": ("fixed", (20.0, 30.0))}
    _, out = _run(check, "Ambient Temperature", [["231"]], params)
    assert _result(out).state == State.WARN


def test_levels_switched_off_in_a_rule(check):
    params = {"levels_upper": ("no_levels", None)}
    _, out = _run(check, "Ambient Temperature", [["999"]], params)
    assert _result(out).state == State.OK


@pytest.mark.xfail(strict=True, reason="BUG: a non-numeric SNMP value crashes the check instead of giving a result")
@pytest.mark.parametrize("raw", ["", "N/A"])
def test_garbage_value_does_not_crash(check, raw):
    _, out = _run(check, "Battery Temperature", [[raw]])
    assert _result(out).state == State.UNKNOWN
