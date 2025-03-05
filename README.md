# Keithley SMU Client

A Python-based graphical interface for controlling Keithley SourceMeter 2612B.

## Features

- Three measurement modes:
  - Output characteristics (Id-Vd)
  - Transfer characteristics (Id-Vg)
  - Time-response measurements
- Configurable measurement parameters

## Requirements

- Python
- PyQt5
- pyqtgraph
- numpy
- pyvisa
- pyvisa-py

## Installation

### Via pip (recommended)
```bash
pip install git+https://www.github.com/fabio-terranova/keithley-client.git
```

### From source
```bash
git clone https://github.com/fabio-terranova/keithley-client.git
cd keithley-client
pip install .
```

## Usage

Launch the application using:
```bash
keithley_client
```

### Command Line Options

- `--idvd` : Start in Id-Vd measurement mode
- `--idvg` : Start in Id-Vg measurement mode
- `--time` : Start in time response measurement mode
- `--dummy`: Use dummy mode for testing without hardware
- `--font-size N` : Set GUI font size (default: 8)
- `--version` : Show version information
- `--help` : Display help message

## Configuration

The application can be configured by editing the `config.py` file:
