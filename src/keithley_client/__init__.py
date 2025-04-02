"""
Fabio - 2025

Keithley SMU client
"""

import argparse
import os

import PyQt5
import pyqtgraph as pg
import json
from platformdirs import user_data_dir
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from .config import CONFIGS
from .gui.MainWindow import MainWindow

__version__ = "0.3.0"
__author__ = "Fabio T"
__all__ = ["PyQt5"]

win_title = f"Keithley SMU client {__version__} - {__author__}"

# Create the data directory
user_dir = user_data_dir(appname="keithley_client", appauthor=False)

if not os.path.exists(user_dir):
    os.makedirs(user_dir)

with open(os.path.join(user_dir, "default.json"), "w") as f:
    json.dump(CONFIGS, f, indent=4)


def config_pyqtgraph():
    """
    PyQtGraph configuration
    """
    pg.setConfigOption("antialias", True)
    pg.setConfigOption("background", "w")
    pg.setConfigOption("foreground", "k")
    pg.setConfigOption("leftButtonPan", False)


def cli():
    """
    # Command line interface

    ## Usage

    `keithley_client [--idvd] [--idvg] [--time] [--font-size N] [--dummy] [--version] [--help]`

    ## Options

    The following options can be used to show a specific interface:

    `--idvg`: show the transfer curve interface

    `--idvd`: show the output curve interface

    `--time`: show the time response interface

    `--pulse`: show the pulse response interface

    `--dummy`: use a dummy Keithley class to test the application

    `--font-size`: set the font size of the application

    `--version`: show the version of the program
    """

    parser = argparse.ArgumentParser(description="Keithley SMU client")
    parser.add_argument(
        "--idvg", action="store_true", help="show the transfer curve interface"
    )
    parser.add_argument(
        "--idvd", action="store_true", help="show the output curve interface"
    )
    parser.add_argument(
        "--time", action="store_true", help="show the time response interface"
    )
    parser.add_argument(
        "--pulse", action="store_true", help="show the pulse response interface"
    )
    parser.add_argument(
        "--dummy",
        action="store_true",
        help="use a dummy Keithley class to test the application",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=8,
        help="set the font size of the application",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args()

    config_pyqtgraph()

    # Create the application
    app = QApplication([])
    app.setFont(QFont("Arial", args.font_size))
    if args.idvg:
        mode = "Id-Vg"
    elif args.idvd:
        mode = "Id-Vd"
    elif args.time:
        mode = "Time"
    elif args.pulse:
        mode = "Time (pulse)"
    else:
        mode = "Id-Vd"

    # Create the main window
    main = MainWindow(win_title, mode, args.dummy)
    main.show()

    # Run the application
    app.exec_()
