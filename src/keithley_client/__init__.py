"""
Fabio - 2025

Keithley SMU client
"""

import argparse
import pyqtgraph as pg

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from .gui.MainWindow import MainWindow
from .config import FONT_SIZE

__version__ = "0.1.4"
__author__ = "Fabio T"

win_title = f"Keithley SMU client {__version__} - {__author__}"


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

    `keithley_client [--idvd] [--idvg] [--time] [--font-size] [--dummy] [--version] [--help]`

    ## Options

    The following options can be used to show a specific interface:

    `--idvg`: show the transfer curve interface

    `--idvd`: show the output curve interface

    `--time`: show the time response interface

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
        "--dummy",
        action="store_true",
        help="use a dummy Keithley class to test the application",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=FONT_SIZE,
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
    else:
        mode = "Id-Vd"

    # Create the main window
    main = MainWindow(win_title, mode, args.dummy)
    main.show()

    # Run the application
    app.exec_()
