import random


class KeithleyDummy:
    """
    Dummy Keithley class to simulate the Keithley SMU for testing purposes.
    """

    def __init__(self, address):
        self.address = address
        self.output_state = {"a": False, "b": False}
        self.voltage = {"a": 0, "b": 0}
        self.current = {"a": 0, "b": 0}

    def reset(self):
        self.output_state = {"a": False, "b": False}
        self.voltage = {"a": 0, "b": 0}
        self.current = {"a": 0, "b": 0}

    def set_source_function(self, smu, function):
        pass

    def set_voltage_source(self, smu, voltage):
        self.voltage[smu] = voltage

    def set_current_source(self, smu, current):
        self.current[smu] = current

    def set_voltage_limit(self, smu, voltage):
        pass

    def set_current_limit(self, smu, current):
        pass

    def turn_output_on(self, smu):
        self.output_state[smu] = True

    def turn_output_off(self, smu):
        self.output_state[smu] = False

    def beep(self):
        print("Beep!")

    def source_i_level(self, smu):
        return self.current[smu]

    def source_v_level(self, smu):
        return self.voltage[smu]

    def measure_i(self, smu):
        if self.output_state[smu]:
            if smu == "a":  # Simulate n-type MOSFET current readings
                # Simulate p-type MOSFET current readings
                Vgs = self.voltage["b"]
                Vds = self.voltage["a"]
                Vth = 0  # Threshold voltage for p-type
                W_L = 635  # Width-to-length ratio
                Cox = 15e-9  # Oxide capacitance per unit area (F/cm^2)
                mobility = 0.01  # Mobility in cm/Vs
                Kp = W_L * Cox * mobility

                if Vgs > Vth:
                    Id = 0
                else:
                    if Vds > (Vgs - Vth):
                        Id = -Kp * ((Vgs - Vth) * Vds - 0.5 * Vds**2)  # Linear region
                    else:
                        Id = -0.5 * Kp * (Vgs - Vth) ** 2  # Saturation region
                return Id + random.uniform(-1e-12, 1e-12)
            else:
                return random.uniform(-1e-9, 1e-9)
        return 0

    def measure_v(self, smu):
        if self.output_state[smu]:
            return self.voltage[smu]  # Return the set voltage
        return 0

    def reset_smu(self, smu):
        self.voltage[smu] = 0
        self.current[smu] = 0

    def set_source_v_level(self, smu, level):
        self.voltage[smu] = level

    def set_source_i_level(self, smu, level):
        self.current[smu] = level
