#!/usr/bin/env python3
# Copyright (C) 2025 OETIKER+PARTNER AG - License: GNU General Public License v2

"""Metric translations for the Huawei UPS plugin rename.

The v1 check names follow the pattern ``huawei_ups_<service_name>``,
using generic metric names (temperature, voltage, current, etc.).
The v2 plugin uses ``oposs_huawei_ups_<service_name>`` with prefixed
metric names.  Each old check needs its own Translation entry because
the same generic metric name maps to different prefixed names depending
on the check context.
"""

from cmk.graphing.v1 import translations

# --- Temperature checks ---

translation_huawei_ups_ambient_temperature = translations.Translation(
    name="huawei_ups_ambient_temperature",
    check_commands=[translations.PassiveCheck("huawei_ups_ambient_temperature")],
    translations={"temperature": translations.RenameTo("oposs_huawei_temperature")},
)

translation_huawei_ups_device_temperature = translations.Translation(
    name="huawei_ups_device_temperature",
    check_commands=[translations.PassiveCheck("huawei_ups_device_temperature")],
    translations={"temperature": translations.RenameTo("oposs_huawei_temperature")},
)

translation_huawei_ups_battery_temperature = translations.Translation(
    name="huawei_ups_battery_temperature",
    check_commands=[translations.PassiveCheck("huawei_ups_battery_temperature")],
    translations={"temperature": translations.RenameTo("oposs_huawei_temperature")},
)

# --- Humidity ---

translation_huawei_ups_ambient_humidity = translations.Translation(
    name="huawei_ups_ambient_humidity",
    check_commands=[translations.PassiveCheck("huawei_ups_ambient_humidity")],
    translations={"humidity": translations.RenameTo("oposs_huawei_humidity")},
)

# --- Input Voltage (per-phase) ---

translation_huawei_ups_phase_a_input_voltage = translations.Translation(
    name="huawei_ups_phase_a_input_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_input_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_huawei_ups_phase_b_input_voltage = translations.Translation(
    name="huawei_ups_phase_b_input_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_input_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_huawei_ups_phase_c_input_voltage = translations.Translation(
    name="huawei_ups_phase_c_input_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_input_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

# --- Output Voltage (per-phase) ---

translation_huawei_ups_phase_a_output_voltage = translations.Translation(
    name="huawei_ups_phase_a_output_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_output_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_huawei_ups_phase_b_output_voltage = translations.Translation(
    name="huawei_ups_phase_b_output_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_output_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_huawei_ups_phase_c_output_voltage = translations.Translation(
    name="huawei_ups_phase_c_output_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_output_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

# --- Battery Voltage ---

translation_huawei_ups_battery_voltage = translations.Translation(
    name="huawei_ups_battery_voltage",
    check_commands=[translations.PassiveCheck("huawei_ups_battery_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

# --- Input Current (per-phase) ---

translation_huawei_ups_phase_a_input_current = translations.Translation(
    name="huawei_ups_phase_a_input_current",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_input_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_huawei_ups_phase_b_input_current = translations.Translation(
    name="huawei_ups_phase_b_input_current",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_input_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_huawei_ups_phase_c_input_current = translations.Translation(
    name="huawei_ups_phase_c_input_current",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_input_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

# --- Output Current (per-phase) ---

translation_huawei_ups_phase_a_output_current = translations.Translation(
    name="huawei_ups_phase_a_output_current",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_output_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_huawei_ups_phase_b_output_current = translations.Translation(
    name="huawei_ups_phase_b_output_current",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_output_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_huawei_ups_phase_c_output_current = translations.Translation(
    name="huawei_ups_phase_c_output_current",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_output_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

# --- Battery Current ---

translation_huawei_ups_battery_current = translations.Translation(
    name="huawei_ups_battery_current",
    check_commands=[translations.PassiveCheck("huawei_ups_battery_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

# --- Frequency ---

translation_huawei_ups_input_frequency = translations.Translation(
    name="huawei_ups_input_frequency",
    check_commands=[translations.PassiveCheck("huawei_ups_input_frequency")],
    translations={"frequency": translations.RenameTo("oposs_huawei_frequency")},
)

translation_huawei_ups_output_frequency = translations.Translation(
    name="huawei_ups_output_frequency",
    check_commands=[translations.PassiveCheck("huawei_ups_output_frequency")],
    translations={"frequency": translations.RenameTo("oposs_huawei_frequency")},
)

# --- Output Active Power (per-phase) ---

translation_huawei_ups_phase_a_output_active_power = translations.Translation(
    name="huawei_ups_phase_a_output_active_power",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_output_active_power")],
    translations={"power": translations.RenameTo("oposs_huawei_active_power")},
)

translation_huawei_ups_phase_b_output_active_power = translations.Translation(
    name="huawei_ups_phase_b_output_active_power",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_output_active_power")],
    translations={"power": translations.RenameTo("oposs_huawei_active_power")},
)

translation_huawei_ups_phase_c_output_active_power = translations.Translation(
    name="huawei_ups_phase_c_output_active_power",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_output_active_power")],
    translations={"power": translations.RenameTo("oposs_huawei_active_power")},
)

# --- Output Apparent Power (per-phase) ---

translation_huawei_ups_phase_a_output_apparent_power = translations.Translation(
    name="huawei_ups_phase_a_output_apparent_power",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_output_apparent_power")],
    translations={"power": translations.RenameTo("oposs_huawei_apparent_power")},
)

translation_huawei_ups_phase_b_output_apparent_power = translations.Translation(
    name="huawei_ups_phase_b_output_apparent_power",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_output_apparent_power")],
    translations={"power": translations.RenameTo("oposs_huawei_apparent_power")},
)

translation_huawei_ups_phase_c_output_apparent_power = translations.Translation(
    name="huawei_ups_phase_c_output_apparent_power",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_output_apparent_power")],
    translations={"power": translations.RenameTo("oposs_huawei_apparent_power")},
)

# --- Output Load (per-phase) ---

translation_huawei_ups_phase_a_output_load = translations.Translation(
    name="huawei_ups_phase_a_output_load",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_a_output_load")],
    translations={"percentage": translations.RenameTo("oposs_huawei_load_pct")},
)

translation_huawei_ups_phase_b_output_load = translations.Translation(
    name="huawei_ups_phase_b_output_load",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_b_output_load")],
    translations={"percentage": translations.RenameTo("oposs_huawei_load_pct")},
)

translation_huawei_ups_phase_c_output_load = translations.Translation(
    name="huawei_ups_phase_c_output_load",
    check_commands=[translations.PassiveCheck("huawei_ups_phase_c_output_load")],
    translations={"percentage": translations.RenameTo("oposs_huawei_load_pct")},
)

# --- Battery Capacity ---

translation_huawei_ups_battery_capacity_left = translations.Translation(
    name="huawei_ups_battery_capacity_left",
    check_commands=[translations.PassiveCheck("huawei_ups_battery_capacity_left")],
    translations={"percentage": translations.RenameTo("oposs_huawei_battery_pct")},
)

# --- Battery Backup Time ---

translation_huawei_ups_battery_backup_time = translations.Translation(
    name="huawei_ups_battery_backup_time",
    check_commands=[translations.PassiveCheck("huawei_ups_battery_backup_time")],
    translations={"duration": translations.RenameTo("oposs_huawei_backup_time")},
)
