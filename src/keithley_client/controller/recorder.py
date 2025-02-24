import pandas
import time

from PyQt5.QtCore import QThread, pyqtSignal

from collections import deque

from .keithley import Keithley
# from .keithley_dummy import KeithleyDummy as Keithley


class Recorder(QThread):
    data_ready = pyqtSignal()

    def __init__(self, keithley_address, smu_cfg):
        super().__init__()
        self.keithley = Keithley(keithley_address)
        self.smu_cfg = smu_cfg
        self.points = []
        self.id = deque()
        self.ig = deque()
        self.vd = deque()
        self.vg = deque()
        self.time = deque()
        self.recording = False

    def set_points(self, points):
        self.points = points

    def start(self, points, delay=1):
        # reset the keithley
        self.keithley.reset()
        self.keithley.set_source_function("a", "OUTPUT_DCVOLTS")
        self.keithley.set_source_function("b", "OUTPUT_DCVOLTS")

        # start the measurementù
        self.keithley.turn_ouput_on("a")
        self.keithley.turn_ouput_on("b")

        self.points = points
        self.delay = delay

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

        if len(self.points) == 1:
            while self.recording:
                [vg, vd] = self.points[0]
                self.keithley.set_voltage_source("a", vg)
                self.keithley.set_voltage_source("b", vd)
                time.sleep(self.delay)
                self.time.append(time.time() - start_time)
                self.vg.append(vg)
                self.vd.append(vd)
                self.id.append(self.keithley.measure_i("a"))
                self.ig.append(self.keithley.measure_i("b"))
                self.data_ready.emit()

        for [vg, vd] in self.points:
            if not self.recording:
                break
            self.keithley.set_voltage_source("a", vg)
            self.keithley.set_voltage_source("b", vd)
            time.sleep(self.delay)
            self.time.append(time.time() - start_time)
            self.vg.append(vg)
            self.vd.append(vd)
            self.id.append(self.keithley.measure_i("a"))
            self.ig.append(self.keithley.measure_i("b"))
            self.data_ready.emit()

    def stop(self):
        self.recording = False
        self.keithley.turn_output_off("a")
        self.keithley.turn_output_off("b")

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
