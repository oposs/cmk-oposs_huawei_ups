"""The checks fed with an snmpwalk of a real UPS2000 3kVA on mains.

tests/data/ups2000_3kva.walk holds the OIDs the plugin fetches plus sysDescr,
sysObjectID and the two UPS-MIB detection OIDs, taken from a production
device and anonymized. The UPS is single-phase: phases B and C send 0, the
input current columns are missing, and battery current and temperature are
2147483647 because no sensor is installed.
"""

import pathlib

import pytest
from cmk.agent_based.v2 import Metric, Result, Service, State
from test_check import _detects, _plugins, _sections, check  # noqa: F401

WALK = pathlib.Path(__file__).resolve().parent / "data/ups2000_3kva.walk"


def _walk():
    values = {}
    for line in WALK.read_text().splitlines():
        oid, _, value = line.partition(" ")
        values[oid] = value
    return values


def _rows(tree, walk):
    """The string table Checkmk builds for one single-column SNMPTree.

    A column that names a scalar instance (Ambient Temperature fetches
    "6.0") returns that instance, as a walk falls back to a GET.
    """
    (oid,) = tree.oids
    column = f"{tree.base}.{oid.column}"
    return [[value] for key, value in walk.items() if key == column or key.startswith(column + ".")]


def _real(check, service):  # noqa: F811
    plugin = _plugins(check)[service]
    (tree,) = _sections(check)[plugin.name].fetch
    section = _sections(check)[plugin.name].parse_function([_rows(tree, _walk())])
    discovered = list(plugin.discovery_function(section))
    params = plugin.check_default_parameters
    if params is None:
        out = list(plugin.check_function(section))
    else:
        out = list(plugin.check_function(params, section))
    return discovered, out


def test_detects_the_real_ups2000(check):  # noqa: F811
    walk = _walk()
    assert walk[".1.3.6.1.2.1.1.1.0"].startswith("Linux GSE200M")
    assert walk[".1.3.6.1.2.1.1.2.0"] == ".1.3.6.1.4.1.8072.3.2.10"
    assert _detects(check.DETECT_HUAWEI_UPS, walk)


# service, state, summary, metric value (None: no metric)
DISCOVERED = [
    ("UPS Alarm Check", State.OK, "No Alarms", None),
    ("Power Supply Method", State.OK, "normal mode", None),
    ("Battery State", State.OK, "float charging", None),
    ("Ambient Temperature", State.OK, "Ambient Temperature: 20 °C", 19.5),
    ("Ambient Humidity", State.OK, "Ambient Humidity: 39 %", 38.6),
    ("Device Temperature", State.OK, "Device Temperature: 14 °C", 13.7),
    ("Phase A Input Voltage", State.OK, "Phase A Input Voltage: 231 V", 231.0),
    ("Input Frequency", State.OK, "Input Frequency: 49.90 Hz", 49.9),
    ("Phase A Output Voltage", State.OK, "Phase A Output Voltage: 230 V", 229.7),
    # UPS-MIB upsOutputCurrent.1 is 13 (0.1 A) as well.
    ("Phase A Output Current", State.OK, "Phase A Output Current: 1 A", 1.3),
    ("Phase B Output Current", State.OK, "Phase B Output Current: 0 A", 0.0),
    ("Phase C Output Current", State.OK, "Phase C Output Current: 0 A", 0.0),
    ("Output Frequency", State.OK, "Output Frequency: 49.90 Hz", 49.9),
    ("Phase A Output Active Power", State.OK, "Phase A Output Active Power: 0.10 kW", 100.0),
    ("Phase B Output Active Power", State.OK, "Phase B Output Active Power: 0.00 kW", 0.0),
    ("Phase C Output Active Power", State.OK, "Phase C Output Active Power: 0.00 kW", 0.0),
    ("Phase A Output Apparent Power", State.OK, "Phase A Output Apparent Power: 0.2 kVA", 200.0),
    ("Phase B Output Apparent Power", State.OK, "Phase B Output Apparent Power: 0.0 kVA", 0.0),
    ("Phase C Output Apparent Power", State.OK, "Phase C Output Apparent Power: 0.0 kVA", 0.0),
    # UPS-MIB upsOutputPercentLoad.1 is 9 %.
    ("Phase A Output Load", State.OK, "Phase A Output Load: 9.0 %", 9.0),
    ("Phase B Output Load", State.OK, "Phase B Output Load: 0.0 %", 0.0),
    ("Phase C Output Load", State.OK, "Phase C Output Load: 0.0 %", 0.0),
    # UPS-MIB upsBatteryVoltage is 820 (0.1 V) as well.
    ("Battery Voltage", State.OK, "Battery Voltage: 82.0 V", 82.0),
    # UPS-MIB upsEstimatedChargeRemaining is 100 %.
    ("Battery Capacity Left", State.OK, "Battery Capacity Left: 100.0 %", 100.0),
    # UPS-MIB upsEstimatedMinutesRemaining is 147 min, 8820 s.
    ("Battery Backup Time", State.OK, "Battery Backup Time: 2.5h", 8822.0),
]


@pytest.mark.parametrize("service, state, summary, value", DISCOVERED, ids=[d[0] for d in DISCOVERED])
def test_real_reading(check, service, state, summary, value):  # noqa: F811
    discovered, out = _real(check, service)
    assert discovered == [Service()]
    results = [r for r in out if isinstance(r, Result)]
    assert results == [Result(state=state, summary=summary)]
    metrics = [m.value for m in out if isinstance(m, Metric)]
    assert metrics == ([] if value is None else [pytest.approx(value)])


@pytest.mark.parametrize("service", [f"Phase {p} Input Current" for p in "ABC"])
def test_missing_column_creates_no_service(check, service):  # noqa: F811
    discovered, out = _real(check, service)
    assert discovered == []
    assert out == []


@pytest.mark.parametrize("service", ["Battery Current", "Battery Temperature"])
def test_no_value_creates_no_service(check, service):  # noqa: F811
    # 2147483647 read as 0.1 units gave 214748364.7 °C, CRIT, and 214748364.7 A.
    discovered, out = _real(check, service)
    assert discovered == []
    assert out == [Result(state=State.UNKNOWN, summary="Device has no value for this measurement (2147483647)")]


SINGLE_PHASE_VOLTAGES = [f"Phase {p} {d} Voltage" for p in "BC" for d in ("Input", "Output")]


@pytest.mark.parametrize("service", SINGLE_PHASE_VOLTAGES)
def test_unused_phase_voltage_is_crit_today(check, service):  # noqa: F811
    _, out = _real(check, service)
    (result,) = [r for r in out if isinstance(r, Result)]
    assert result.state == State.CRIT


@pytest.mark.xfail(strict=True, reason=(
    "OWNER DECISION: a single-phase UPS2000 (UPS-MIB upsInputNumLines.0 and upsOutputNumLines.0 = 1) "
    "sends 0 V for phases B and C, which discovers four voltage services that are CRIT forever"))
@pytest.mark.parametrize("service", SINGLE_PHASE_VOLTAGES)
def test_single_phase_ups_has_no_phase_b_c_voltage_service(check, service):  # noqa: F811
    discovered, _ = _real(check, service)
    assert discovered == []
