#!/usr/bin/env python3
# Copyright (C) 2025 OETIKER+PARTNER AG - License: GNU General Public License v2

"""Metric translations for the legacy oegig huawei_ups plugin -> oposs_huawei_ups.

The old plugin emitted generic metric names (``temperature``, ``voltage``,
``current``, ``frequency``, ``percentage``, ``power``, ``humidity``,
``duration``).  The new plugin emits prefixed metrics (``oposs_huawei_*``).
Service names are unchanged across both plugins, so on an upgraded site the
legacy RRD files (e.g. ``temperature.rrd``) sit in the same per-service
directory as the new ones (e.g. ``oposs_huawei_temperature.rrd``).

Each Translation tells the Checkmk graphing engine: when rendering a graph
for the *current* service (whose check command is now
``check_mk-oposs_huawei_ups_*``), treat any RRD column carrying the old
generic name as if it were the new prefixed metric.  This stitches the
old and new history together into one continuous line.

IMPORTANT: ``check_commands`` MUST reference the *new* check name, not the
legacy one.  Checkmk's translation lookup
(``cmk/gui/graphing/_translated_metrics.py``,
``lookup_metric_translations_for_check_command``) does an exact dict lookup
on the live service's current check command; an entry keyed on the
now-uninstalled legacy command would never fire.

There is intentionally NO entry for ``oposs_huawei_ups_output_frequency``.
The legacy v1 check read the wrong SNMP OID (``.3.100.1.7`` =
``hwUpsInputCurrentC`` instead of the output frequency at ``.4.100.1.7``),
so historical RRD values are bogus current-C readings (~3-4) rather than
~50 Hz.  Stitching them into the now-correct Output Frequency graph would
visually corrupt it; the legacy RRD is left orphaned on disk on purpose.
The Input Frequency translation IS kept because that OID was correct in
both versions.
"""

from cmk.graphing.v1 import translations

# --- Temperature checks ---

translation_oposs_huawei_ups_ambient_temperature = translations.Translation(
    name="oposs_huawei_ups_ambient_temperature",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_ambient_temperature")],
    translations={"temperature": translations.RenameTo("oposs_huawei_temperature")},
)

translation_oposs_huawei_ups_device_temperature = translations.Translation(
    name="oposs_huawei_ups_device_temperature",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_device_temperature")],
    translations={"temperature": translations.RenameTo("oposs_huawei_temperature")},
)

translation_oposs_huawei_ups_battery_temperature = translations.Translation(
    name="oposs_huawei_ups_battery_temperature",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_battery_temperature")],
    translations={"temperature": translations.RenameTo("oposs_huawei_temperature")},
)

# --- Humidity ---

translation_oposs_huawei_ups_ambient_humidity = translations.Translation(
    name="oposs_huawei_ups_ambient_humidity",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_ambient_humidity")],
    translations={"humidity": translations.RenameTo("oposs_huawei_humidity")},
)

# --- Input Voltage (per-phase) ---

translation_oposs_huawei_ups_phase_a_input_voltage = translations.Translation(
    name="oposs_huawei_ups_phase_a_input_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_input_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_oposs_huawei_ups_phase_b_input_voltage = translations.Translation(
    name="oposs_huawei_ups_phase_b_input_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_input_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_oposs_huawei_ups_phase_c_input_voltage = translations.Translation(
    name="oposs_huawei_ups_phase_c_input_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_input_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

# --- Output Voltage (per-phase) ---

translation_oposs_huawei_ups_phase_a_output_voltage = translations.Translation(
    name="oposs_huawei_ups_phase_a_output_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_output_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_oposs_huawei_ups_phase_b_output_voltage = translations.Translation(
    name="oposs_huawei_ups_phase_b_output_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_output_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

translation_oposs_huawei_ups_phase_c_output_voltage = translations.Translation(
    name="oposs_huawei_ups_phase_c_output_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_output_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

# --- Battery Voltage ---

translation_oposs_huawei_ups_battery_voltage = translations.Translation(
    name="oposs_huawei_ups_battery_voltage",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_battery_voltage")],
    translations={"voltage": translations.RenameTo("oposs_huawei_voltage")},
)

# --- Input Current (per-phase) ---

translation_oposs_huawei_ups_phase_a_input_current = translations.Translation(
    name="oposs_huawei_ups_phase_a_input_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_input_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_oposs_huawei_ups_phase_b_input_current = translations.Translation(
    name="oposs_huawei_ups_phase_b_input_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_input_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_oposs_huawei_ups_phase_c_input_current = translations.Translation(
    name="oposs_huawei_ups_phase_c_input_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_input_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

# --- Output Current (per-phase) ---

translation_oposs_huawei_ups_phase_a_output_current = translations.Translation(
    name="oposs_huawei_ups_phase_a_output_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_output_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_oposs_huawei_ups_phase_b_output_current = translations.Translation(
    name="oposs_huawei_ups_phase_b_output_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_output_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

translation_oposs_huawei_ups_phase_c_output_current = translations.Translation(
    name="oposs_huawei_ups_phase_c_output_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_output_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

# --- Battery Current ---

translation_oposs_huawei_ups_battery_current = translations.Translation(
    name="oposs_huawei_ups_battery_current",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_battery_current")],
    translations={"current": translations.RenameTo("oposs_huawei_current")},
)

# --- Frequency ---
# Note: deliberately NO entry for output_frequency (see module docstring).

translation_oposs_huawei_ups_input_frequency = translations.Translation(
    name="oposs_huawei_ups_input_frequency",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_input_frequency")],
    translations={"frequency": translations.RenameTo("oposs_huawei_frequency")},
)

# --- Output Active Power (per-phase) ---

translation_oposs_huawei_ups_phase_a_output_active_power = translations.Translation(
    name="oposs_huawei_ups_phase_a_output_active_power",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_output_active_power")],
    translations={"power": translations.RenameTo("oposs_huawei_active_power")},
)

translation_oposs_huawei_ups_phase_b_output_active_power = translations.Translation(
    name="oposs_huawei_ups_phase_b_output_active_power",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_output_active_power")],
    translations={"power": translations.RenameTo("oposs_huawei_active_power")},
)

translation_oposs_huawei_ups_phase_c_output_active_power = translations.Translation(
    name="oposs_huawei_ups_phase_c_output_active_power",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_output_active_power")],
    translations={"power": translations.RenameTo("oposs_huawei_active_power")},
)

# --- Output Apparent Power (per-phase) ---

translation_oposs_huawei_ups_phase_a_output_apparent_power = translations.Translation(
    name="oposs_huawei_ups_phase_a_output_apparent_power",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_output_apparent_power")],
    translations={"power": translations.RenameTo("oposs_huawei_apparent_power")},
)

translation_oposs_huawei_ups_phase_b_output_apparent_power = translations.Translation(
    name="oposs_huawei_ups_phase_b_output_apparent_power",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_output_apparent_power")],
    translations={"power": translations.RenameTo("oposs_huawei_apparent_power")},
)

translation_oposs_huawei_ups_phase_c_output_apparent_power = translations.Translation(
    name="oposs_huawei_ups_phase_c_output_apparent_power",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_output_apparent_power")],
    translations={"power": translations.RenameTo("oposs_huawei_apparent_power")},
)

# --- Output Load (per-phase) ---

translation_oposs_huawei_ups_phase_a_output_load = translations.Translation(
    name="oposs_huawei_ups_phase_a_output_load",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_a_output_load")],
    translations={"percentage": translations.RenameTo("oposs_huawei_load_pct")},
)

translation_oposs_huawei_ups_phase_b_output_load = translations.Translation(
    name="oposs_huawei_ups_phase_b_output_load",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_b_output_load")],
    translations={"percentage": translations.RenameTo("oposs_huawei_load_pct")},
)

translation_oposs_huawei_ups_phase_c_output_load = translations.Translation(
    name="oposs_huawei_ups_phase_c_output_load",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_phase_c_output_load")],
    translations={"percentage": translations.RenameTo("oposs_huawei_load_pct")},
)

# --- Battery Capacity ---

translation_oposs_huawei_ups_battery_capacity_left = translations.Translation(
    name="oposs_huawei_ups_battery_capacity_left",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_battery_capacity_left")],
    translations={"percentage": translations.RenameTo("oposs_huawei_battery_pct")},
)

# --- Battery Backup Time ---

translation_oposs_huawei_ups_battery_backup_time = translations.Translation(
    name="oposs_huawei_ups_battery_backup_time",
    check_commands=[translations.PassiveCheck("oposs_huawei_ups_battery_backup_time")],
    translations={"duration": translations.RenameTo("oposs_huawei_backup_time")},
)
