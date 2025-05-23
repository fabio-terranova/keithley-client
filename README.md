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

### SSH key setup

To allow SSH access to the repository, follow these steps:

1. Generate an SSH key pair (if you don't have one):

    ```bash
    ssh-keygen -t ed25519 -C "<email>"
    ```

    Replace `<email>` with your email address.

2. Add the public key to deploy keys in the GitHub repository settings.

### Via pip (recommended)

Generate an SSH key pair (if you don't have one):

```bash
ssh-keygen -t ed25519 -C "<email>"
```

Replace `<email>` with your email address.

Install the package using pip:

```bash
pip install git+ssh://git@github.com/fabio-terranova/keithley-client.git
```

#### Update

To update the package via pip, use the following command:

```bash
pip install --upgrade --no-deps git+ssh://git@github.com/fabio-terranova/keithley-client.git
```

#### Specific version

```bash
pip install git+ssh://git@github.com/fabio-terranova/keithley-client.git@<version>
```

Replace `<version>` with the desired version tag (e.g., `v0.3.4` or `v0.4.1`).

### Via source code

Clone the repository:

```bash
git clone ssh://fabio-terranova@github.com/fabio-terranova/keithley-client.git
```

Navigate to the cloned directory:

```bash
cd keithley-client
```

Install the package:

```bash
pip install --no-deps .
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
- `--pulse` : Start in time (pulse) measurement mode
- `--dummy`: Use dummy mode for testing without hardware
- `--font-size N` : Set GUI font size (default: 8)
- `--version` : Show version information
- `--help` : Display help message

## Configuration

The application uses configuration files to store measurement settings:

- Default settings are defined in the source code
- User settings are saved in the user data directory
- Settings are saved per measurement mode (Id-Vd, Id-Vg, Time, Time pulse)

### Configuration Options

Each measurement mode can be configured with:

- Gate and drain voltage parameters
  - Fixed or sweep mode
  - Start/stop values and number of steps
  - Bidirectional sweeps
  - Pulse parameters (delta voltage and delay)
- Measurement settings
  - Sampling period
  - Number of averaged points per measurement
  - Plot axes configuration
- Data saving options

Settings are automatically saved when changed in the GUI and persist between sessions.
