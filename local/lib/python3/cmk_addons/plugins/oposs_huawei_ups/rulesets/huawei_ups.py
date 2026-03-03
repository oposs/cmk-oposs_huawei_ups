#!/usr/bin/env python3

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)


def _upper_levels(title, unit, default):
    return Dictionary(
        elements={
            "levels_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("%s" % title),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol=unit),
                    prefill_fixed_levels=DefaultValue(default),
                ),
                required=True,
            ),
        },
    )


def _lower_levels(title, unit, default):
    return Dictionary(
        elements={
            "levels_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("%s" % title),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Float(unit_symbol=unit),
                    prefill_fixed_levels=DefaultValue(default),
                ),
                required=True,
            ),
        },
    )


def _upper_lower_levels(title_upper, title_lower, unit, default_upper, default_lower):
    return Dictionary(
        elements={
            "levels_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("%s" % title_upper),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol=unit),
                    prefill_fixed_levels=DefaultValue(default_upper),
                ),
                required=True,
            ),
            "levels_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("%s" % title_lower),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Float(unit_symbol=unit),
                    prefill_fixed_levels=DefaultValue(default_lower),
                ),
                required=True,
            ),
        },
    )


# --- Temperature rulesets ---

rule_spec_oposs_huawei_ups_ambient_temperature = CheckParameters(
    name="oposs_huawei_ups_ambient_temperature",
    title=Title("Huawei UPS Ambient Temperature"),
    topic=Topic.ENVIRONMENT,
    parameter_form=lambda: _upper_levels("Upper levels", "\u00b0C", (40.0, 50.0)),
    condition=HostCondition(),
)

rule_spec_oposs_huawei_ups_device_temperature = CheckParameters(
    name="oposs_huawei_ups_device_temperature",
    title=Title("Huawei UPS Device Temperature"),
    topic=Topic.ENVIRONMENT,
    parameter_form=lambda: _upper_levels("Upper levels", "\u00b0C", (60.0, 70.0)),
    condition=HostCondition(),
)

rule_spec_oposs_huawei_ups_battery_temperature = CheckParameters(
    name="oposs_huawei_ups_battery_temperature",
    title=Title("Huawei UPS Battery Temperature"),
    topic=Topic.ENVIRONMENT,
    parameter_form=lambda: _upper_levels("Upper levels", "\u00b0C", (60.0, 70.0)),
    condition=HostCondition(),
)

# --- Humidity ---

rule_spec_oposs_huawei_ups_ambient_humidity = CheckParameters(
    name="oposs_huawei_ups_ambient_humidity",
    title=Title("Huawei UPS Ambient Humidity"),
    topic=Topic.ENVIRONMENT,
    parameter_form=lambda: _upper_levels("Upper levels", "%", (83.0, 86.0)),
    condition=HostCondition(),
)

# --- Voltage rulesets ---

rule_spec_oposs_huawei_ups_input_voltage = CheckParameters(
    name="oposs_huawei_ups_input_voltage",
    title=Title("Huawei UPS Input Voltage"),
    topic=Topic.POWER,
    parameter_form=lambda: _lower_levels("Lower levels", "V", (210.0, 180.0)),
    condition=HostCondition(),
)

rule_spec_oposs_huawei_ups_output_voltage = CheckParameters(
    name="oposs_huawei_ups_output_voltage",
    title=Title("Huawei UPS Output Voltage"),
    topic=Topic.POWER,
    parameter_form=lambda: _lower_levels("Lower levels", "V", (210.0, 180.0)),
    condition=HostCondition(),
)

# --- Frequency rulesets ---

rule_spec_oposs_huawei_ups_input_frequency = CheckParameters(
    name="oposs_huawei_ups_input_frequency",
    title=Title("Huawei UPS Input Frequency"),
    topic=Topic.POWER,
    parameter_form=lambda: _upper_lower_levels(
        "Upper levels", "Lower levels", "Hz", (51.0, 52.0), (49.0, 48.0),
    ),
    condition=HostCondition(),
)

rule_spec_oposs_huawei_ups_output_frequency = CheckParameters(
    name="oposs_huawei_ups_output_frequency",
    title=Title("Huawei UPS Output Frequency"),
    topic=Topic.POWER,
    parameter_form=lambda: _upper_lower_levels(
        "Upper levels", "Lower levels", "Hz", (51.0, 52.0), (49.0, 48.0),
    ),
    condition=HostCondition(),
)

# --- Load ---

rule_spec_oposs_huawei_ups_output_load = CheckParameters(
    name="oposs_huawei_ups_output_load",
    title=Title("Huawei UPS Output Load"),
    topic=Topic.POWER,
    parameter_form=lambda: _upper_levels("Upper levels", "%", (80.0, 90.0)),
    condition=HostCondition(),
)

# --- Battery ---

rule_spec_oposs_huawei_ups_battery_capacity = CheckParameters(
    name="oposs_huawei_ups_battery_capacity",
    title=Title("Huawei UPS Battery Capacity"),
    topic=Topic.POWER,
    parameter_form=lambda: _lower_levels("Lower levels", "%", (15.0, 10.0)),
    condition=HostCondition(),
)

rule_spec_oposs_huawei_ups_battery_backup_time = CheckParameters(
    name="oposs_huawei_ups_battery_backup_time",
    title=Title("Huawei UPS Battery Backup Time"),
    topic=Topic.POWER,
    parameter_form=lambda: _lower_levels("Lower levels", "s", (1200.0, 600.0)),
    condition=HostCondition(),
)
