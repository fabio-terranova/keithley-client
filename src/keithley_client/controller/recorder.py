import time
from collections import deque

import numpy as np
import pandas
from PyQt5.QtCore import QThread, pyqtSignal

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

    def start(self, points, delay=1, n_points=1, pulse_info=None):
        # reset the keithley
        self.keithley.reset()

        # start the measurement
        self.keithley.turn_output_on("b")
        self.keithley.turn_output_on("a")

        self.points = points
        self.delay = delay
        self.n_points = n_points

        # Handle pulse information
        if pulse_info is not None:
            self.pulse_info = pulse_info
        else:
            self.pulse_info = [{"enabled": False}, {"enabled": False}]

        self.recording = True
        self.process = QThread()
        self.process.run = self.record
        self.process.start()

    def get_response_time(self, n_points=1, n=3):
        # Calculate the response time of the Keithley
        times = []
        for _ in range(n):
            start_time = time.time()
            for _ in range(n_points):
                self.keithley.measure_i("a")
                self.keithley.measure_i("b")
                self.keithley.source_v_level("a")
                self.keithley.source_v_level("b")
            end_time = time.time()
            times.append(end_time - start_time)
        return sum(times) / len(times)

    def record(self):
        self.id.clear()
        self.ig.clear()
        self.vd.clear()
        self.vg.clear()
        self.time.clear()

        start_time = time.time()

        def measure(n=1):
            current_time = time.time() - start_time
            self.time.append(current_time)

            Id = np.zeros(n)
            Ig = np.zeros(n)
            Vd = np.zeros(n)
            Vg = np.zeros(n)

            for i in range(n):
                Id[i] = self.keithley.measure_i("a")
                Ig[i] = self.keithley.measure_i("b")
                Vd[i] = self.keithley.source_v_level("a")
                Vg[i] = self.keithley.source_v_level("b")

            self.id.append(np.mean(Id))
            self.ig.append(np.mean(Ig))
            self.vd.append(np.mean(Vd))
            self.vg.append(np.mean(Vg))

            self.data_ready.emit()

        if len(self.points) == 1:
            [vg_base, vd_base] = self.points[0]

            # Calculate pulse parameters
            vg_pulse_enabled = self.pulse_info[0].get("enabled", False)
            vd_pulse_enabled = self.pulse_info[1].get("enabled", False)

            # Extract pulse parameters for Vd and Vg
            if vd_pulse_enabled:
                vd_delta = self.pulse_info[1]["delta"]
                vd_delay = self.pulse_info[1]["delay"]

            if vg_pulse_enabled:
                vg_delta = self.pulse_info[0]["delta"]
                vg_delay = self.pulse_info[0]["delay"]

            while self.recording:
                self.keithley.set_voltage_source("a", vd_base)
                self.keithley.set_voltage_source("b", vg_base)

                if vg_pulse_enabled or vd_pulse_enabled:
                    pulse_delay = vg_delay if vg_pulse_enabled else vd_delay

                    time.sleep(pulse_delay)

                    if vd_pulse_enabled:
                        self.keithley.set_voltage_source("a", vd_base + vd_delta)
                    if vg_pulse_enabled:
                        self.keithley.set_voltage_source("b", vg_base + vg_delta)

                    time.sleep(pulse_delay)

                measure(n=self.n_points)
                if vg_pulse_enabled or vd_pulse_enabled:
                    if vd_pulse_enabled:
                        self.keithley.set_voltage_source("a", vd_base)
                    if vg_pulse_enabled:
                        self.keithley.set_voltage_source("b", vg_base)

                time.sleep(
                    self.delay - 2 * pulse_delay if vg_pulse_enabled else self.delay
                )

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
