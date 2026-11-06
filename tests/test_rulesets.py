"""The rule forms build, and every check with levels has a matching rule."""

import importlib.util
import pathlib
import sys

import pytest
from cmk.agent_based.v2 import CheckPlugin
from cmk.rulesets.v1.form_specs import LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "local/lib/python3/cmk_addons/plugins/oposs_huawei_ups"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def rules():
    module = _load(PLUGIN / "rulesets/huawei_ups.py", "test_oposs_huawei_ups_rulesets")
    return {v.name: v for v in vars(module).values() if isinstance(v, CheckParameters)}


@pytest.fixture(scope="module")
def plugins():
    module = _load(PLUGIN / "agent_based/oposs_huawei_ups.py", "test_oposs_huawei_ups_check_rs")
    return [v for v in vars(module).values() if isinstance(v, CheckPlugin)]


def test_there_are_eleven_rules(rules):
    assert len(rules) == 11


def test_every_ruleset_name_has_a_rule(plugins, rules):
    used = {p.check_ruleset_name for p in plugins if p.check_ruleset_name}
    assert sorted(used - set(rules)) == []


def test_every_rule_is_used(plugins, rules):
    used = {p.check_ruleset_name for p in plugins}
    assert sorted(set(rules) - used) == []


def test_rules_match_itemless_services(rules):
    # The services carry no item, so an item condition would never match.
    for rule in rules.values():
        assert isinstance(rule.condition, HostCondition), rule.name
        assert rule.topic in (Topic.ENVIRONMENTAL, Topic.POWER), rule.name


def test_check_defaults_match_the_form(plugins, rules):
    """A form field per default, with the default as prefill and the right direction."""
    checked = 0
    for plugin in plugins:
        if not plugin.check_ruleset_name:
            continue
        form = rules[plugin.check_ruleset_name].parameter_form()
        defaults = plugin.check_default_parameters
        assert set(form.elements) == set(defaults), plugin.name
        for key, (kind, levels) in defaults.items():
            spec = form.elements[key].parameter_form
            assert isinstance(spec, SimpleLevels)
            assert kind == "fixed"
            assert spec.prefill_fixed_levels.value == levels, (plugin.name, key)
            expected = LevelDirection.UPPER if key == "levels_upper" else LevelDirection.LOWER
            assert spec.level_direction == expected, (plugin.name, key)
        checked += 1
    assert checked == 17


def test_checks_without_a_rule_have_no_levels(plugins):
    for plugin in plugins:
        if plugin.check_ruleset_name is None and plugin.check_default_parameters is not None:
            assert plugin.check_default_parameters == {}, plugin.name
