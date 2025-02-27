# Keithley SMU Client

A Python-based graphical interface for controlling Keithley SourceMeter 2612B. This application provides a user-friendly way to perform common semiconductor measurements including Id-Vd, Id-Vg, and time-based measurements.

## Features

- Three measurement modes:
  - Output characteristics (Id-Vd)
  - Transfer characteristics (Id-Vg)
  - Time-based measurements
- Real-time plotting
- Data export functionality
- Configurable measurement parameters
- GPIB communication support

## Requirements

- Python 3.7+
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
- `--time` : Start in time measurement mode
- `--dummy`: Use dummy mode for testing without hardware
- `--font-size N` : Set GUI font size (default: 8)
- `--version` : Show version information
- `--help` : Display help message

## Configuration

The application can be configured by editing the `config.py` file:

### Default configurations available:
- Id-Vd measurements
- Id-Vg measurements
- Time-based measurements

Each configuration includes:
- Voltage sweep ranges
- Step sizes

## License

MIT License - See LICENSE file for details
