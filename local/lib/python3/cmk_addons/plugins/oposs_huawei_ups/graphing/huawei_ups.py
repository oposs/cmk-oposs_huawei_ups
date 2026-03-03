#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    Metric,
    Unit,
)
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.perfometers import Perfometer, FocusRange, Closed

# Units
unit_celsius = Unit(DecimalNotation("\u00b0C"))
unit_percent = Unit(DecimalNotation("%"))
unit_volts = Unit(DecimalNotation("V"))
unit_amperes = Unit(DecimalNotation("A"))
unit_hertz = Unit(DecimalNotation("Hz"))
unit_watts = Unit(DecimalNotation("W"))
unit_va = Unit(DecimalNotation("VA"))
unit_seconds = Unit(DecimalNotation("s"))

# Metrics
metric_oposs_huawei_temperature = Metric(
    name="oposs_huawei_temperature",
    title=Title("Temperature"),
    unit=unit_celsius,
    color=Color.ORANGE,
)

metric_oposs_huawei_humidity = Metric(
    name="oposs_huawei_humidity",
    title=Title("Humidity"),
    unit=unit_percent,
    color=Color.CYAN,
)

metric_oposs_huawei_voltage = Metric(
    name="oposs_huawei_voltage",
    title=Title("Voltage"),
    unit=unit_volts,
    color=Color.BLUE,
)

metric_oposs_huawei_current = Metric(
    name="oposs_huawei_current",
    title=Title("Current"),
    unit=unit_amperes,
    color=Color.GREEN,
)

metric_oposs_huawei_frequency = Metric(
    name="oposs_huawei_frequency",
    title=Title("Frequency"),
    unit=unit_hertz,
    color=Color.PURPLE,
)

metric_oposs_huawei_active_power = Metric(
    name="oposs_huawei_active_power",
    title=Title("Active Power"),
    unit=unit_watts,
    color=Color.YELLOW,
)

metric_oposs_huawei_apparent_power = Metric(
    name="oposs_huawei_apparent_power",
    title=Title("Apparent Power"),
    unit=unit_va,
    color=Color.DARK_YELLOW,
)

metric_oposs_huawei_load_pct = Metric(
    name="oposs_huawei_load_pct",
    title=Title("Load"),
    unit=unit_percent,
    color=Color.RED,
)

metric_oposs_huawei_battery_pct = Metric(
    name="oposs_huawei_battery_pct",
    title=Title("Battery Capacity"),
    unit=unit_percent,
    color=Color.GREEN,
)

metric_oposs_huawei_backup_time = Metric(
    name="oposs_huawei_backup_time",
    title=Title("Backup Time"),
    unit=unit_seconds,
    color=Color.BLUE,
)

# Graphs
graph_oposs_huawei_temperature = Graph(
    name="oposs_huawei_temperature",
    title=Title("Huawei UPS Temperature"),
    simple_lines=["oposs_huawei_temperature"],
    minimal_range=MinimalRange(lower=0, upper=80),
)

graph_oposs_huawei_humidity = Graph(
    name="oposs_huawei_humidity",
    title=Title("Huawei UPS Humidity"),
    simple_lines=["oposs_huawei_humidity"],
    minimal_range=MinimalRange(lower=0, upper=100),
)

graph_oposs_huawei_voltage = Graph(
    name="oposs_huawei_voltage",
    title=Title("Huawei UPS Voltage"),
    simple_lines=["oposs_huawei_voltage"],
)

graph_oposs_huawei_current = Graph(
    name="oposs_huawei_current",
    title=Title("Huawei UPS Current"),
    simple_lines=["oposs_huawei_current"],
)

graph_oposs_huawei_frequency = Graph(
    name="oposs_huawei_frequency",
    title=Title("Huawei UPS Frequency"),
    simple_lines=["oposs_huawei_frequency"],
    minimal_range=MinimalRange(lower=45, upper=55),
)

graph_oposs_huawei_active_power = Graph(
    name="oposs_huawei_active_power",
    title=Title("Huawei UPS Active Power"),
    simple_lines=["oposs_huawei_active_power"],
)

graph_oposs_huawei_apparent_power = Graph(
    name="oposs_huawei_apparent_power",
    title=Title("Huawei UPS Apparent Power"),
    simple_lines=["oposs_huawei_apparent_power"],
)

graph_oposs_huawei_load_pct = Graph(
    name="oposs_huawei_load_pct",
    title=Title("Huawei UPS Load"),
    simple_lines=["oposs_huawei_load_pct"],
    minimal_range=MinimalRange(lower=0, upper=100),
)

graph_oposs_huawei_battery_pct = Graph(
    name="oposs_huawei_battery_pct",
    title=Title("Huawei UPS Battery Capacity"),
    simple_lines=["oposs_huawei_battery_pct"],
    minimal_range=MinimalRange(lower=0, upper=100),
)

graph_oposs_huawei_backup_time = Graph(
    name="oposs_huawei_backup_time",
    title=Title("Huawei UPS Backup Time"),
    simple_lines=["oposs_huawei_backup_time"],
)

# Perfometers
perfometer_oposs_huawei_load_pct = Perfometer(
    name="oposs_huawei_load_pct",
    focus_range=FocusRange(lower=Closed(0), upper=Closed(100)),
    segments=["oposs_huawei_load_pct"],
)

perfometer_oposs_huawei_battery_pct = Perfometer(
    name="oposs_huawei_battery_pct",
    focus_range=FocusRange(lower=Closed(0), upper=Closed(100)),
    segments=["oposs_huawei_battery_pct"],
)

perfometer_oposs_huawei_humidity = Perfometer(
    name="oposs_huawei_humidity",
    focus_range=FocusRange(lower=Closed(0), upper=Closed(100)),
    segments=["oposs_huawei_humidity"],
)
