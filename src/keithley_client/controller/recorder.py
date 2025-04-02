import pandas
import time

from PyQt5.QtCore import QThread, pyqtSignal

from collections import deque

from .keithley import Keithley
from .keithley_dummy import KeithleyDummy


class Recorder(QThread):
    data_ready = pyqtSignal()
    data_ended = pyqtSignal()

    def __init__(self, keithley_address, dummy=False):
        super().__init__()
        self.keithley = (
            KeithleyDummy(keithley_address) if dummy else Keithley(keithley_address)
        )
        self.keithley.set_source_function("b", "OUTPUT_DCVOLTS")
        self.keithley.set_source_function("a", "OUTPUT_DCVOLTS")
        self.points = []
        self.id = deque()
        self.ig = deque()
        self.vd = deque()
        self.vg = deque()
        self.time = deque()
        self.recording = False
        self.pulse_info = [{"enabled": False}, {"enabled": False}]

    def set_points(self, points):
        self.points = points

    def start(self, points, delay=1, pulse_info=None):
        # reset the keithley
        self.keithley.reset()

        # start the measurement
        self.keithley.turn_output_on("b")
        self.keithley.turn_output_on("a")

        self.points = points
        self.delay = delay

        # Handle pulse information
        if pulse_info is not None:
            self.pulse_info = pulse_info
        else:
            self.pulse_info = [{"enabled": False}, {"enabled": False}]

        self.recording = True
        self.process = QThread()
        self.process.run = self.record
        self.process.start()

    def record(self):
        self.id.clear()
        self.ig.clear()
        self.vd.clear()
        self.vg.clear()
        self.time.clear()

        start_time = time.time()

        # For continuous measurement mode (single point)
        if len(self.points) == 1:
            [vg_base, vd_base] = self.points[0]

            # Calculate pulse parameters
            vg_pulse_enabled = self.pulse_info[0].get("enabled", False)
            vd_pulse_enabled = self.pulse_info[1].get("enabled", False)

            # Extract pulse parameters for Vg
            if vg_pulse_enabled:
                vg_delta = self.pulse_info[0]["delta"]
                vg_period = self.pulse_info[0]["period"]
                vg_duty = self.pulse_info[0]["duty"]

            if vd_pulse_enabled:
                vd_delta = self.pulse_info[1]["delta"]
                vd_period = self.pulse_info[1]["period"]
                vd_duty = self.pulse_info[1]["duty"]

            while self.recording:
                current_time = time.time() - start_time

                # Calculate pulse voltage values
                vg = vg_base
                vd = vd_base

                if vg_pulse_enabled:
                    vg_pos = (current_time % vg_period) / vg_period
                    if vg_pos >= (1 - vg_duty / 100):
                        vg = vg_base + vg_delta

                if vd_pulse_enabled:
                    vd_pos = (current_time % vd_period) / vd_period
                    if vd_pos >= (1 - vd_duty / 100):
                        vd = vd_base + vd_delta

                # Set voltages
                self.keithley.set_voltage_source("a", vd)
                self.keithley.set_voltage_source("b", vg)
                time.sleep(self.delay)

                # Measure and store data
                self.time.append(current_time)
                self.vg.append(vg)
                self.vd.append(vd)
                self.id.append(self.keithley.measure_i("a"))
                self.ig.append(self.keithley.measure_i("b"))
                self.data_ready.emit()
        else:
            # Standard sweep measurement
            for [vg, vd] in self.points:
                if not self.recording:
                    break
                self.keithley.set_voltage_source("a", vd)
                self.keithley.set_voltage_source("b", vg)
                time.sleep(self.delay)
                self.time.append(time.time() - start_time)
                self.vg.append(vg)
                self.vd.append(vd)
                self.id.append(self.keithley.measure_i("a"))
                self.ig.append(self.keithley.measure_i("b"))
                self.data_ready.emit()

        self.data_ended.emit()

    def stop(self):
        self.recording = False
        time.sleep(0.1)
        self.keithley.turn_output_off("b")
        self.keithley.turn_output_off("a")

    def save(self, filename, columns=None):
        if columns is None:
            columns = ["Time", "Vg", "Vd", "Id", "Ig"]
        data = {
            "Time": self.time,
            "Vg": self.vg,
            "Vd": self.vd,
            "Id": self.id,
            "Ig": self.ig,
        }
        df = pandas.DataFrame(data)
        df = df[columns]
        df.to_csv(filename, index=False, sep="\t")
        return df
