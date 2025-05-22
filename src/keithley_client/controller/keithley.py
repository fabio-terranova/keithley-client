import pyvisa


class Keithley:
    """
    Keithley class to control the Keithley SMU
    """

    def __init__(self, address):
        self.instrument = pyvisa.ResourceManager("@py").open_resource(address)
        self.reset()

    def __del__(self):
        self.instrument.close()

    def reset(self):
        self.instrument.write("*RST")
        self.instrument.write("smua.measure.rangei = 1e-6")
        self.instrument.write("smub.measure.rangei = 1e-6")
        self.instrument.write("smua.source.limiti = 10e-6")
        self.instrument.write("smub.source.limiti = 10e-6")
        self.beep()

    def set_source_function(self, smu, function):
        self.instrument.write(f"smu{smu}.source.func = smu{smu}.{function}")

    def set_voltage_source(self, smu, voltage):
        self.instrument.write(f"smu{smu}.source.levelv = {voltage}")

    def set_current_source(self, smu, current):
        self.instrument.write(f"smu{smu}.source.leveli = {current}")

    def set_voltage_limit(self, smu, voltage):
        self.instrument.write(f"smu{smu}.source.limitv = {voltage}")

    def set_current_limit(self, smu, current):
        self.instrument.write(f"smu{smu}.source.limiti = {current}")

    def turn_output_on(self, smu):
        self.instrument.write(f"smu{smu}.source.output = smu{smu}.OUTPUT_ON")

    def turn_output_off(self, smu):
        self.instrument.write(f"smu{smu}.source.output = smu{smu}.OUTPUT_OFF")

    def beep(self):
        self.instrument.write("beeper.enable = beeper.ON")
        self.instrument.write("beeper.beep(1, 1200)")
        self.instrument.write("beeper.enable = beeper.OFF")

    def source_i_level(self, smu):
        return self.instrument.query(f"print(smu{smu}.source.leveli)")

    def source_v_level(self, smu):
        return self.instrument.query(f"print(smu{smu}.source.levelv)")

    def measure_i(self, smu):
        res = self.instrument.query(f"print(smu{smu}.measure.i())")
        return float(res)

    def measure_v(self, smu):
        res = self.instrument.query(f"print(smu{smu}.measure.v())")
        return float(res)

    def reset_smu(self, smu):
        self.instrument.write(f"smu{smu}.reset()")

    def set_source_v_level(self, smu, level):
        self.instrument.write(f"smu{smu}.source.levelv = {level}")

    def set_source_i_level(self, smu, level):
        self.instrument.write(f"smu{smu}.source.leveli = {level}")
