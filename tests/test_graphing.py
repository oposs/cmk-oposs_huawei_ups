"""Metric names: prefixed, declared, and translated from the legacy plugin.

The legacy oegig huawei_ups plugin wrote generic metric names (temperature,
voltage, ...) into the same per-service RRD directories, because the service
names did not change. The translations map those names onto the prefixed
metrics, keyed on the check commands the services run today.
"""

import importlib.util
import pathlib
import sys

import pytest
from cmk.agent_based.v2 import CheckPlugin, Metric, SimpleSNMPSection
from cmk.graphing.v1 import graphs, metrics, perfometers, translations

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "local/lib/python3/cmk_addons/plugins/oposs_huawei_ups"

# The metric the legacy plugin wrote, per prefixed metric of this plugin.
LEGACY = {
    "oposs_huawei_temperature": "temperature",
    "oposs_huawei_humidity": "humidity",
    "oposs_huawei_voltage": "voltage",
    "oposs_huawei_current": "current",
    "oposs_huawei_frequency": "frequency",
    "oposs_huawei_active_power": "power",
    "oposs_huawei_apparent_power": "power",
    "oposs_huawei_load_pct": "percentage",
    "oposs_huawei_battery_pct": "percentage",
    "oposs_huawei_backup_time": "duration",
}


def _load(path):
    name = "test_graphing_" + path.stem + "_" + path.parent.name
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def check():
    return _load(PLUGIN / "agent_based/oposs_huawei_ups.py")


@pytest.fixture(scope="module")
def graphing_objects():
    objects = []
    for path in sorted((PLUGIN / "graphing").glob("*.py")):
        objects.extend(vars(_load(path)).values())
    return objects


@pytest.fixture(scope="module")
def declared(graphing_objects):
    return {o.name for o in graphing_objects if isinstance(o, metrics.Metric)}


@pytest.fixture(scope="module")
def emitted(check):
    """Check plugin name -> the metric names it yields for a reading."""
    sections = {v.name: v for v in vars(check).values() if isinstance(v, SimpleSNMPSection)}
    out = {}
    for plugin in vars(check).values():
        if not isinstance(plugin, CheckPlugin):
            continue
        section = sections[plugin.name].parse_function([[["100"]]])
        if plugin.check_default_parameters is None:
            results = plugin.check_function(section)
        else:
            results = plugin.check_function(plugin.check_default_parameters, section)
        out[plugin.name] = [m.name for m in results if isinstance(m, Metric)]
    return out


@pytest.fixture(scope="module")
def translation_list(graphing_objects):
    return [o for o in graphing_objects if isinstance(o, translations.Translation)]


def test_every_emitted_metric_is_prefixed_and_declared(emitted, declared):
    names = {n for metrics_ in emitted.values() for n in metrics_}
    assert names
    assert [n for n in names if not n.startswith("oposs_huawei_")] == []
    assert sorted(names - declared) == []


def test_every_declared_metric_is_emitted(emitted, declared):
    names = {n for metrics_ in emitted.values() for n in metrics_}
    assert sorted(declared - names) == []


def test_levels_checks_emit_one_metric_state_checks_none(emitted):
    for name, metrics_ in emitted.items():
        expected = 0 if name in (
            "oposs_huawei_ups_ups_alarm_check",
            "oposs_huawei_ups_power_supply_method",
            "oposs_huawei_ups_battery_state",
        ) else 1
        assert len(metrics_) == expected, name


def test_every_declared_name_is_prefixed(graphing_objects):
    kinds = (metrics.Metric, graphs.Graph, perfometers.Perfometer, translations.Translation)
    names = [o.name for o in graphing_objects if isinstance(o, kinds)]
    assert [n for n in names if not n.startswith("oposs_huawei_")] == []


def test_graphs_and_perfometers_use_declared_metrics(graphing_objects, declared):
    used = set()
    for o in graphing_objects:
        if isinstance(o, graphs.Graph):
            used.update(o.simple_lines)
            used.update(o.compound_lines)
        elif isinstance(o, perfometers.Perfometer):
            used.update(o.segments)
    assert used
    assert sorted(used - declared) == []


def test_translations_are_keyed_on_live_check_commands(translation_list, emitted):
    # Checkmk looks a translation up by the service's current check command,
    # so a key naming the legacy check would never fire.
    for translation in translation_list:
        assert translation.check_commands == [translations.PassiveCheck(translation.name)]
        assert translation.name in emitted, translation.name


def test_translations_rename_legacy_names_to_the_emitted_metric(translation_list, emitted, declared):
    for translation in translation_list:
        ((old, rule),) = translation.translations.items()
        (new,) = emitted[translation.name]
        # Same units in both plugins, so a rename without scaling.
        assert rule == translations.RenameTo(new), translation.name
        assert new in declared
        assert old == LEGACY[new], translation.name


def test_every_metric_check_has_a_translation_except_output_frequency(translation_list, emitted):
    # The legacy Output Frequency read input current C, so its history is
    # left out on purpose rather than merged into the frequency graph.
    translated = {t.name for t in translation_list}
    with_metrics = {name for name, m in emitted.items() if m}
    assert sorted(with_metrics - translated) == ["oposs_huawei_ups_output_frequency"]
    assert sorted(translated - with_metrics) == []
