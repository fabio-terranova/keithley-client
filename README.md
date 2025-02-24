# Keithely SMU client

A Python-based graphical interface for controlling Keithley SMU 2600 Series

## Requirements

- Python 3.7+
- PyQt5
- pyqtgraph
- numpy
- pyvisa

## Installation

1. Install via pip
```bash
pip install git+https://www.github.com/fabio-terranova/keithley-client
```

## Usage

Launch the application with:

```bash
keithley_client
```

Command line options:
- `--idvd`: Start in Id-Vd measurement mode
- `--idvg`: Start in Id-Vg measurement mode
- `--time`: Start in time measurement mode
- `--font-size N`: Set GUI font size (default: 8)
- `--version`: Show version information

## Configuration

Edit `config.py` to modify:
- Default GPIB address
- Default measurement configurations
- Plot settings
- Font size

## License

MIT License - See LICENSE file for details
