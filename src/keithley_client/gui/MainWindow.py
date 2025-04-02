import json
import os

import numpy as np
from platformdirs import user_data_dir
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QWidget,
)
from pyqtgraph import GraphicsLayoutWidget

from ..config import CONFIGS, KEITHLEY_ADDRESS
from ..controller.recorder import Recorder
from ..utils import float_to_eng_string

user_dir = user_data_dir(appname="keithley_client", appauthor=False)


class MainWindow(QMainWindow):
    """
    Main window
    """

    def __init__(self, win_title, mode, dummy=False):
        super().__init__()

        self.win_title = win_title
        self.mode = mode
        try:
            with open(os.path.join(user_dir, "user.json"), "r") as f:
                self.configs = json.load(f)
                print(
                    f"Loading configuration from {os.path.join(user_dir, 'user.json')}"
                )
        except FileNotFoundError:
            print("No user configuration found, loading default configuration")
            try:
                with open(os.path.join(user_dir, "default.json"), "r") as f:
                    self.configs = json.load(f)
                    print(
                        f"Loading configuration from {os.path.join(user_dir, 'default.json')}"
                    )
            except FileNotFoundError:
                print("No default configuration found, loading hardcoded configuration")
                self.configs = CONFIGS

        self.recorder = Recorder(KEITHLEY_ADDRESS, dummy=dummy)
        self.recorder.data_ready.connect(self.update_plots)
        self.recorder.data_ended.connect(self.stop)

        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface
        """
        self.setWindowTitle(self.win_title)

        # Mode group
        self.mode_group = QGroupBox("Measurement mode")
        self.mode_layout = QGridLayout()
        self.mode_group.setLayout(self.mode_layout)
        self.restore_config_button = QPushButton("Restore configurations")

        self.config_combo = QComboBox()
        self.config_combo.addItem("Id-Vd")
        self.config_combo.addItem("Id-Vg")
        self.config_combo.addItem("Time")
        self.config_combo.setCurrentText(self.mode)

        self.mode_layout.addWidget(self.config_combo)
        self.mode_layout.addWidget(self.restore_config_button)

        # Voltage source configuration
        self.voltage_group = QGroupBox("Voltage configuration")
        self.voltage_layout = QGridLayout()
        self.voltage_group.setLayout(self.voltage_layout)

        self.Vg_group = QGroupBox("Vg")
        self.Vg_layout = QGridLayout()
        self.Vg_group.setLayout(self.Vg_layout)

        self.Vg_mode_label = QLabel("Mode")
        self.Vg_mode_combo = QComboBox()
        self.Vg_mode_combo.addItem("Sweep")
        self.Vg_mode_combo.addItem("Fixed")

        self.Vg_bidirectional_checkbox = QCheckBox("Bidirectional")
        self.Vg_value_label = QLabel("Value (V)")
        self.Vg_spin = QDoubleSpinBox()

        self.Vg_start_label = QLabel("Start value (V)")
        self.Vg_start_spin = QDoubleSpinBox()
        self.Vg_stop_label = QLabel("Stop value (V)")
        self.Vg_stop_spin = QDoubleSpinBox()
        self.Vg_step_label = QLabel("Steps")
        self.Vg_step_spin = QSpinBox()

        self.Vg_step_value = QLabel()

        self.Vg_layout.addWidget(self.Vg_mode_label, 0, 0)
        self.Vg_layout.addWidget(self.Vg_mode_combo, 0, 1)
        self.Vg_layout.addWidget(self.Vg_bidirectional_checkbox, 1, 0, 1, 2)
        self.Vg_layout.addWidget(self.Vg_value_label, 2, 0)
        self.Vg_layout.addWidget(self.Vg_spin, 2, 1)
        self.Vg_layout.addWidget(self.Vg_start_label, 3, 0)
        self.Vg_layout.addWidget(self.Vg_start_spin, 3, 1)
        self.Vg_layout.addWidget(self.Vg_stop_label, 4, 0)
        self.Vg_layout.addWidget(self.Vg_stop_spin, 4, 1)
        self.Vg_layout.addWidget(self.Vg_step_label, 5, 0)
        self.Vg_layout.addWidget(self.Vg_step_spin, 5, 1)
        self.Vg_layout.addWidget(self.Vg_step_value, 6, 0, 1, 2)

        self.Vd_group = QGroupBox("Vd")
        self.Vd_layout = QGridLayout()
        self.Vd_group.setLayout(self.Vd_layout)

        self.Vd_mode_label = QLabel("Mode")
        self.Vd_mode_combo = QComboBox()
        self.Vd_mode_combo.addItem("Sweep")
        self.Vd_mode_combo.addItem("Fixed")

        self.Vd_bidirectional_checkbox = QCheckBox("Bidirectional")

        self.Vd_value_label = QLabel("Value (V)")
        self.Vd_spin = QDoubleSpinBox()

        self.Vd_start_label = QLabel("Start value (V)")
        self.Vd_start_spin = QDoubleSpinBox()

        self.Vd_stop_label = QLabel("Stop value (V)")
        self.Vd_stop_spin = QDoubleSpinBox()

        self.Vd_step_label = QLabel("Steps")
        self.Vd_step_spin = QSpinBox()

        self.Vd_step_value = QLabel()

        for widget in [
            self.Vg_spin,
            self.Vg_start_spin,
            self.Vg_stop_spin,
            self.Vd_spin,
            self.Vd_start_spin,
            self.Vd_stop_spin,
        ]:
            widget.setDecimals(2)
            widget.setRange(-20, 20)
            widget.setSingleStep(1)

        for widget in [self.Vg_step_spin, self.Vd_step_spin]:
            widget.setMinimum(2)
            widget.setMaximum(1000)

        self.Vd_layout.addWidget(self.Vd_mode_label, 0, 0)
        self.Vd_layout.addWidget(self.Vd_mode_combo, 0, 1)
        self.Vd_layout.addWidget(self.Vd_bidirectional_checkbox, 1, 0, 1, 2)
        self.Vd_layout.addWidget(self.Vd_value_label, 2, 0)
        self.Vd_layout.addWidget(self.Vd_spin, 2, 1)
        self.Vd_layout.addWidget(self.Vd_start_label, 3, 0)
        self.Vd_layout.addWidget(self.Vd_start_spin, 3, 1)
        self.Vd_layout.addWidget(self.Vd_stop_label, 4, 0)
        self.Vd_layout.addWidget(self.Vd_stop_spin, 4, 1)
        self.Vd_layout.addWidget(self.Vd_step_label, 5, 0)
        self.Vd_layout.addWidget(self.Vd_step_spin, 5, 1)
        self.Vd_layout.addWidget(self.Vd_step_value, 6, 0, 1, 2)

        self.voltage_layout.addWidget(self.Vg_group, 0, 1)
        self.voltage_layout.addWidget(self.Vd_group, 0, 0)

        # Measurement configuration
        self.measurement_group = QGroupBox("Measurement configuration")
        self.measurement_layout = QGridLayout()
        self.measurement_group.setLayout(self.measurement_layout)

        self.Y1_axis_checkbox = QCheckBox("Y1 axis")
        self.Y1_axis_checkbox.setChecked(True)
        self.Y1_axis_checkbox.setEnabled(False)
        self.Y1_combo = QComboBox()
        self.Y1_combo.addItem("Id")
        self.Y1_combo.addItem("Ig")

        self.Y2_axis_checkbox = QCheckBox("Y2 axis")
        self.Y2_axis_checkbox.setChecked(True)
        self.Y2_combo = QComboBox()
        self.Y2_combo.addItem("Ig")
        self.Y2_combo.addItem("Id")

        self.X_label = QLabel("X axis")
        self.X_combo = QComboBox()
        self.X_combo.addItem("Vd")
        self.X_combo.addItem("Vg")
        self.X_combo.addItem("Time")

        self.delay_label = QLabel("Delay (s)")
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setDecimals(3)
        self.delay_spin.setRange(0, 1)
        self.delay_spin.setSingleStep(0.01)
        self.delay_spin.setValue(0.1)

        self.measurement_layout.addWidget(self.Y1_axis_checkbox, 0, 0)
        self.measurement_layout.addWidget(self.Y1_combo, 1, 0)
        self.measurement_layout.addWidget(self.Y2_axis_checkbox, 0, 1)
        self.measurement_layout.addWidget(self.Y2_combo, 1, 1)
        self.measurement_layout.addWidget(self.X_label, 0, 2)
        self.measurement_layout.addWidget(self.X_combo, 1, 2)
        self.measurement_layout.addWidget(self.delay_label, 0, 3)
        self.measurement_layout.addWidget(self.delay_spin, 1, 3)

        # Start/stop and save buttons group
        self.buttons_group = QGroupBox("Actions")
        self.buttons_layout = QGridLayout()
        self.buttons_group.setLayout(self.buttons_layout)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.save_button = QPushButton("Save")

        self.columns_group = QGroupBox("Saving")
        self.columns_layout = QGridLayout()
        self.columns_group.setLayout(self.columns_layout)

        self.column_time_checkbox = QCheckBox("Time")
        self.column_Vg_checkbox = QCheckBox("Vg")
        self.column_Vd_checkbox = QCheckBox("Vd")
        self.column_Id_checkbox = QCheckBox("Id")
        self.column_Ig_checkbox = QCheckBox("Ig")

        self.columns_layout.addWidget(self.column_time_checkbox, 0, 0)
        self.columns_layout.addWidget(self.column_Vg_checkbox, 0, 1)
        self.columns_layout.addWidget(self.column_Vd_checkbox, 0, 2)
        self.columns_layout.addWidget(self.column_Id_checkbox, 0, 3)
        self.columns_layout.addWidget(self.column_Ig_checkbox, 0, 4)

        self.buttons_layout.addWidget(self.start_button, 0, 0)
        self.buttons_layout.addWidget(self.stop_button, 0, 1)
        self.buttons_layout.addWidget(self.save_button, 0, 2)
        self.buttons_layout.addWidget(self.columns_group, 1, 0, 1, 3)

        # Info group
        self.info_group = QGroupBox("Info")
        self.info_layout = QGridLayout()
        self.info_group.setLayout(self.info_layout)

        self.id_label = QLabel("Id: 0.0 A")
        self.ig_label = QLabel("Ig: 0.0 A")
        self.vd_label = QLabel("Vd: 0.0 V")
        self.vg_label = QLabel("Vg: 0.0 V")
        self.time_label = QLabel("Time: 0.0 s")
        self.info_label = QLabel("Information")

        self.info_layout.addWidget(self.id_label, 0, 0)
        self.info_layout.addWidget(self.ig_label, 0, 1)
        self.info_layout.addWidget(self.vd_label, 1, 0)
        self.info_layout.addWidget(self.vg_label, 1, 1)
        self.info_layout.addWidget(self.time_label, 2, 0, 1, 2)
        self.info_layout.addWidget(self.info_label, 3, 0, 1, 2)

        # Plot group
        self.plot_group = QGroupBox("Plots")
        self.plot_layout = QGridLayout()
        self.plot_group.setLayout(self.plot_layout)

        self.plot_widget = GraphicsLayoutWidget()
        self.plot_items = [
            self.plot_widget.addPlot(row=0, col=0),
            self.plot_widget.addPlot(row=1, col=0),
        ]
        for plot in self.plot_items:
            plot.showGrid(x=True, y=True)
        self.curves = [
            self.plot_items[i].plot(pen=None, symbol="o", symbolSize=10)
            for i in range(2)
        ]

        self.plot_layout.addWidget(self.plot_widget)

        # Main layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.mode_group, 0, 0)
        self.layout.addWidget(self.voltage_group, 1, 0)
        self.layout.addWidget(self.measurement_group, 2, 0)
        self.layout.addWidget(self.buttons_group, 3, 0)
        self.layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 4, 0
        )
        self.layout.addWidget(self.info_group, 5, 0)
        self.layout.addWidget(self.plot_group, 0, 1, 6, 2)
        self.layout.setColumnStretch(1, 2)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.set_connections()

        self.set_config(self.configs[self.mode])

    def set_connections(self):
        """Set up all widget connections"""
        self.config_combo.currentIndexChanged.connect(self.update_mode)
        self.restore_config_button.clicked.connect(self.restore_config)

        # Voltage gate connections
        self.Vg_mode_combo.currentIndexChanged.connect(
            lambda: self.update_config("Vg.mode", self.Vg_mode_combo.currentText())
        )
        self.Vg_bidirectional_checkbox.stateChanged.connect(
            lambda: self.update_config(
                "Vg.sweep.bidirectional", self.Vg_bidirectional_checkbox.isChecked()
            )
        )
        self.Vg_spin.valueChanged.connect(
            lambda: self.update_config("Vg.fixed.value", self.Vg_spin.value())
        )
        self.Vg_start_spin.valueChanged.connect(
            lambda: self.update_config("Vg.sweep.start", self.Vg_start_spin.value())
        )
        self.Vg_stop_spin.valueChanged.connect(
            lambda: self.update_config("Vg.sweep.stop", self.Vg_stop_spin.value())
        )
        self.Vg_step_spin.valueChanged.connect(
            lambda: self.update_config("Vg.sweep.steps", self.Vg_step_spin.value())
        )

        # Voltage drain connections
        self.Vd_mode_combo.currentIndexChanged.connect(
            lambda: self.update_config("Vd.mode", self.Vd_mode_combo.currentText())
        )
        self.Vd_bidirectional_checkbox.stateChanged.connect(
            lambda: self.update_config(
                "Vd.sweep.bidirectional", self.Vd_bidirectional_checkbox.isChecked()
            )
        )
        self.Vd_spin.valueChanged.connect(
            lambda: self.update_config("Vd.fixed.value", self.Vd_spin.value())
        )
        self.Vd_start_spin.valueChanged.connect(
            lambda: self.update_config("Vd.sweep.start", self.Vd_start_spin.value())
        )
        self.Vd_stop_spin.valueChanged.connect(
            lambda: self.update_config("Vd.sweep.stop", self.Vd_stop_spin.value())
        )
        self.Vd_step_spin.valueChanged.connect(
            lambda: self.update_config("Vd.sweep.steps", self.Vd_step_spin.value())
        )

        # Plot axis connections
        self.Y1_combo.currentIndexChanged.connect(
            lambda: self.update_config("Y1.axis", self.Y1_combo.currentText())
        )
        self.Y2_combo.currentIndexChanged.connect(
            lambda: self.update_config("Y2.axis", self.Y2_combo.currentText())
        )
        self.Y2_axis_checkbox.stateChanged.connect(
            lambda: self.update_config("Y2.enabled", self.Y2_axis_checkbox.isChecked())
        )
        self.X_combo.currentIndexChanged.connect(
            lambda: self.update_config("X.axis", self.X_combo.currentText())
        )

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.save_button.clicked.connect(self.save)

        self.column_time_checkbox.stateChanged.connect(
            lambda: self.update_config(
                "saving.Time", self.column_time_checkbox.isChecked()
            )
        )
        self.column_Vg_checkbox.stateChanged.connect(
            lambda: self.update_config("saving.Vg", self.column_Vg_checkbox.isChecked())
        )
        self.column_Vd_checkbox.stateChanged.connect(
            lambda: self.update_config("saving.Vd", self.column_Vd_checkbox.isChecked())
        )
        self.column_Id_checkbox.stateChanged.connect(
            lambda: self.update_config("saving.Id", self.column_Id_checkbox.isChecked())
        )
        self.column_Ig_checkbox.stateChanged.connect(
            lambda: self.update_config("saving.Ig", self.column_Ig_checkbox.isChecked())
        )

        self.Vd_start_spin.valueChanged.connect(self.update_Vd_step)
        self.Vd_stop_spin.valueChanged.connect(self.update_Vd_step)
        self.Vd_step_spin.valueChanged.connect(self.update_Vd_step)
        self.Vg_start_spin.valueChanged.connect(self.update_Vg_step)
        self.Vg_stop_spin.valueChanged.connect(self.update_Vg_step)
        self.Vg_step_spin.valueChanged.connect(self.update_Vg_step)

    def update_mode(self):
        """Update the mode and load its configuration"""
        self.mode = self.config_combo.currentText()
        self.set_config(self.configs[self.mode])

    def update_config(self, path, value):
        """
        Update a specific configuration value using a dot-notation path

        Args:
            path (str): Dot-notation path to the config value (e.g., 'Vg.mode' or 'Y1.axis')
            value: New value to set
        """
        cfg = self.configs[self.mode]
        keys = path.split(".")

        # Navigate to the nested location
        target = cfg
        for key in keys[:-1]:
            target = target[key]

        # Update the value
        target[keys[-1]] = value

        # Special handling for X axis unit
        if path == "X.axis":
            cfg["X"]["unit"] = "V" if value != "Time" else "s"

        # Automatically update Y2 axis based on Y1
        if path == "Y1.axis":
            if value == "Id":
                self.configs[self.mode]["Y2"]["axis"] = "Ig"
            else:
                self.configs[self.mode]["Y2"]["axis"] = "Id"
        if path == "Y2.axis":
            if value == "Id":
                self.configs[self.mode]["Y1"]["axis"] = "Ig"
            else:
                self.configs[self.mode]["Y1"]["axis"] = "Id"

        # Update plot labels and visibility
        self.plot_items[0].setLabel("bottom", cfg["X"]["axis"], units=cfg["X"]["unit"])
        self.plot_items[0].setLabel("left", cfg["Y1"]["axis"], units=cfg["Y1"]["unit"])
        self.plot_items[1].setLabel("bottom", cfg["X"]["axis"], units=cfg["X"]["unit"])
        self.plot_items[1].setLabel("left", cfg["Y2"]["axis"], units=cfg["Y2"]["unit"])

        # Handle visibility of Vg/Vd controls based on mode
        if path in ["Vg.mode", "Vd.mode"]:
            source = path.split(".")[0]
            self.update_source_visibility(source)

        # Save the updated configuration
        with open(os.path.join(user_dir, "user.json"), "w") as f:
            json.dump(self.configs, f)

        self.set_config(cfg)

    def update_source_visibility(self, source):
        """Update visibility of voltage source controls"""
        widgets = {
            "Vg": {
                "sweep": [
                    self.Vg_start_spin,
                    self.Vg_stop_spin,
                    self.Vg_step_spin,
                    self.Vg_start_label,
                    self.Vg_stop_label,
                    self.Vg_step_label,
                    self.Vg_step_value,
                    self.Vg_bidirectional_checkbox,
                ],
                "fixed": [self.Vg_value_label, self.Vg_spin],
            },
            "Vd": {
                "sweep": [
                    self.Vd_start_spin,
                    self.Vd_stop_spin,
                    self.Vd_step_spin,
                    self.Vd_start_label,
                    self.Vd_stop_label,
                    self.Vd_step_label,
                    self.Vd_step_value,
                    self.Vd_bidirectional_checkbox,
                ],
                "fixed": [self.Vd_value_label, self.Vd_spin],
            },
        }

        mode = self.configs[self.mode][source]["mode"]
        for widget in widgets[source]["sweep"]:
            widget.setVisible(mode == "Sweep")
        for widget in widgets[source]["fixed"]:
            widget.setVisible(mode == "Fixed")

    def update_Vd_step(self):
        """
        Update the Vd step
        """
        if self.Vd_step_spin.value() == 1:
            text = "Step value: error"
        else:
            text = f"Step value: {(self.Vd_stop_spin.value() - self.Vd_start_spin.value()) / (self.Vd_step_spin.value() - 1):.3f} V"

        self.Vd_step_value.setText(text)

    def update_Vg_step(self):
        """
        Update the Vg step
        """
        if self.Vg_step_spin.value() == 1:
            text = "Step value: error"
        else:
            text = f"Step value: {(self.Vg_stop_spin.value() - self.Vg_start_spin.value()) / (self.Vg_step_spin.value() - 1):.3f} V"

        self.Vg_step_value.setText(text)

    def set_config(self, cfg):
        """
        Set the configuration
        """

        fixed_widgets_vd = [
            self.Vd_value_label,
            self.Vd_spin,
        ]

        sweep_widgets_vd = [
            self.Vd_start_spin,
            self.Vd_stop_spin,
            self.Vd_step_spin,
            self.Vd_start_label,
            self.Vd_stop_label,
            self.Vd_step_label,
            self.Vd_step_value,
            self.Vd_bidirectional_checkbox,
        ]

        fixed_widgets_vg = [
            self.Vg_value_label,
            self.Vg_spin,
        ]

        sweep_widgets_vg = [
            self.Vg_start_spin,
            self.Vg_stop_spin,
            self.Vg_step_spin,
            self.Vg_start_label,
            self.Vg_stop_label,
            self.Vg_step_label,
            self.Vg_step_value,
            self.Vg_bidirectional_checkbox,
        ]

        self.Vg_mode_combo.setCurrentText(cfg["Vg"]["mode"])
        self.Vg_bidirectional_checkbox.setChecked(cfg["Vg"]["sweep"]["bidirectional"])
        self.Vg_spin.setValue(cfg["Vg"]["fixed"]["value"])
        self.Vg_start_spin.setValue(cfg["Vg"]["sweep"]["start"])
        self.Vg_stop_spin.setValue(cfg["Vg"]["sweep"]["stop"])
        self.Vg_step_spin.setValue(cfg["Vg"]["sweep"]["steps"])

        self.Vd_mode_combo.setCurrentText(cfg["Vd"]["mode"])
        self.Vd_bidirectional_checkbox.setChecked(cfg["Vd"]["sweep"]["bidirectional"])
        self.Vd_spin.setValue(cfg["Vd"]["fixed"]["value"])
        self.Vd_start_spin.setValue(cfg["Vd"]["sweep"]["start"])
        self.Vd_stop_spin.setValue(cfg["Vd"]["sweep"]["stop"])
        self.Vd_step_spin.setValue(cfg["Vd"]["sweep"]["steps"])

        self.Y1_axis_checkbox.setChecked(cfg["Y1"]["enabled"])
        self.Y1_combo.setCurrentText(cfg["Y1"]["axis"])
        self.Y2_axis_checkbox.setChecked(cfg["Y2"]["enabled"])
        self.Y2_combo.setCurrentText(cfg["Y2"]["axis"])
        self.Y2_combo.setEnabled(cfg["Y2"]["enabled"])
        self.X_combo.setCurrentText(cfg["X"]["axis"])

        self.column_time_checkbox.setChecked(cfg["saving"]["Time"])
        self.column_Vg_checkbox.setChecked(cfg["saving"]["Vg"])
        self.column_Vd_checkbox.setChecked(cfg["saving"]["Vd"])
        self.column_Id_checkbox.setChecked(cfg["saving"]["Id"])
        self.column_Ig_checkbox.setChecked(cfg["saving"]["Ig"])

        if cfg["Vd"]["mode"] == "Sweep":
            for widget in sweep_widgets_vd:
                widget.show()
            for widget in fixed_widgets_vd:
                widget.hide()
        else:
            for widget in sweep_widgets_vd:
                widget.hide()
            for widget in fixed_widgets_vd:
                widget.show()

        if cfg["Vg"]["mode"] == "Sweep":
            for widget in sweep_widgets_vg:
                widget.show()
            for widget in fixed_widgets_vg:
                widget.hide()
        else:
            for widget in fixed_widgets_vg:
                widget.show()
            for widget in sweep_widgets_vg:
                widget.hide()

        self.plot_items[0].setLabel("bottom", cfg["X"]["axis"], units=cfg["X"]["unit"])
        self.plot_items[0].setLabel("left", cfg["Y1"]["axis"], units=cfg["Y1"]["unit"])
        self.plot_items[1].setLabel("bottom", cfg["X"]["axis"], units=cfg["X"]["unit"])
        self.plot_items[1].setLabel("left", cfg["Y2"]["axis"], units=cfg["Y2"]["unit"])

        if cfg["Y2"]["enabled"]:
            self.plot_items[1].show()
        else:
            self.plot_items[1].hide()

    def restore_config(self):
        """
        Restore the configuration
        """
        with open(os.path.join(user_dir, "default.json"), "r") as f:
            self.configs = json.load(f)
            print(
                f"Restoring configuration from {os.path.join(user_dir, 'default.json')}"
            )

        self.set_config(self.configs[self.mode])

    def start(self):
        """
        Start the measurement
        """
        self.voltage_group.setEnabled(False)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.points = []
        modes = [self.Vg_mode_combo.currentText(), self.Vd_mode_combo.currentText()]
        bi = [
            self.Vg_bidirectional_checkbox.isChecked(),
            self.Vd_bidirectional_checkbox.isChecked(),
        ]
        values = [self.Vg_spin.value(), self.Vd_spin.value()]
        ranges = [
            [self.Vg_start_spin.value(), self.Vg_stop_spin.value()],
            [self.Vd_start_spin.value(), self.Vd_stop_spin.value()],
        ]
        steps = [self.Vg_step_spin.value(), self.Vd_step_spin.value()]
        temp = []

        for i, mode in enumerate(modes):
            if mode == "Sweep":
                temp.append(np.linspace(ranges[i][0], ranges[i][1], steps[i]))
                if bi[i]:
                    temp[-1] = np.concatenate([temp[-1], temp[-1][::-1]])
            else:
                temp.append([values[i]])

        for vg in temp[0]:
            for vd in temp[1]:
                self.points.append([vg, vd])

        self.recorder.start(self.points, self.delay_spin.value())

    def stop(self):
        """
        Stop the measurement
        """
        self.recorder.stop()

        self.voltage_group.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_plots(self):
        """
        Update the plot
        """
        self.id_label.setText(f"Id: {float_to_eng_string(self.recorder.id[-1])}A")
        self.ig_label.setText(f"Ig: {float_to_eng_string(self.recorder.ig[-1])}A")
        self.vd_label.setText(f"Vd: {self.recorder.vd[-1]:.2f} V")
        self.vg_label.setText(f"Vg: {self.recorder.vg[-1]:.2f} V")
        self.time_label.setText(f"Time: {self.recorder.time[-1]:.2f} s")

        if self.configs[self.mode]["X"]["axis"] == "Time":
            x = self.recorder.time
        elif self.configs[self.mode]["X"]["axis"] == "Vg":
            x = self.recorder.vg
        else:
            x = self.recorder.vd

        y1 = (
            self.recorder.id
            if self.configs[self.mode]["Y1"]["axis"] == "Id"
            else self.recorder.ig
        )
        y2 = (
            self.recorder.ig
            if self.configs[self.mode]["Y2"]["axis"] == "Ig"
            else self.recorder.id
        )

        self.curves[0].setData(x, y1)
        self.curves[1].setData(x, y2)

    def save(self):
        """
        Save the data
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data",
            "",
            "CSV Files (*.csv);;All Files (*)",
            options=options,
        )

        columns = [
            c
            for c in ["Time", "Vg", "Vd", "Id", "Ig"]
            if self.configs[self.mode]["saving"].get(c, False)
        ]

        if file_name:
            self.recorder.save(file_name, columns)
            self.info_label.setText("Data saved")
        else:
            self.info_label.setText("Data not saved")

    def closeEvent(self, event):
        """
        Close the application
        """
        self.recorder.stop()
        event.accept()
