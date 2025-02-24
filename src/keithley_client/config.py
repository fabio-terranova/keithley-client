"""
Configuration file for the Keithley client.
"""

KEITHLEY_ADDRESS = "GPIB0::26::INSTR"

CONFIGS = {
    "Id-Vd": {
        "Vg": {
            "mode": "Sweep",
            "fixed": {"value": -6},
            "sweep": {"start": 2, "stop": -6, "steps": 5},
            "bidirectional": False,
        },
        "Vd": {
            "mode": "Sweep",
            "fixed": {"value": 0},
            "sweep": {"start": 0, "stop": -6, "steps": 51},
            "bidirectional": False,
        },
        "Y1": {
            "enabled": True,
            "axis": "Id",
            "unit": "A",
        },
        "Y2": {
            "enabled": True,
            "axis": "Ig",
            "unit": "A",
        },
        "X": {
            "axis": "Vd",
            "unit": "V",
        },
        "saving": ["Vg", "Vd", "Id", "Ig"],
    },
    "Id-Vg": {
        "Vg": {
            "mode": "Sweep",
            "fixed": {"value": -6},
            "sweep": {"start": 2, "stop": -6, "steps": 51},
            "bidirectional": True,
        },
        "Vd": {
            "mode": "Fixed",
            "fixed": {"value": -7},
            "sweep": {"start": 0, "stop": -6, "steps": 51},
            "bidirectional": False,
        },
        "Y1": {
            "enabled": True,
            "axis": "Id",
            "unit": "A",
        },
        "Y2": {
            "enabled": True,
            "axis": "Ig",
            "unit": "A",
        },
        "X": {
            "axis": "Vg",
            "unit": "V",
        },
        "saving": ["Vg", "Vd", "Id", "Ig"],
    },
    "Time": {
        "Vg": {
            "mode": "Fixed",
            "fixed": {"value": -6},
            "sweep": {"start": 2, "stop": -6, "steps": 51},
            "bidirectional": False,
        },
        "Vd": {
            "mode": "Fixed",
            "fixed": {"value": -7},
            "sweep": {"start": 0, "stop": -6, "steps": 51},
            "bidirectional": False,
        },
        "Y1": {
            "enabled": True,
            "axis": "Id",
            "unit": "A",
        },
        "Y2": {
            "enabled": True,
            "axis": "Ig",
            "unit": "A",
        },
        "X": {
            "axis": "Time",
            "unit": "s",
        },
        "saving": ["Time", "Vg", "Vd", "Id", "Ig"],
    },
}
