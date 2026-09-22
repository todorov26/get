import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000


def get_triangle_wave_amplitude(freq, t):
    phase = (freq * t) % 1.0
    if phase < 0.5:
        return 2.0 * phase
    else:
        return 2.0 * (1.0 - phase)


try:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, False)

    t = 0.0
    while True:
        amplitude_value = get_triangle_wave_amplitude(signal_frequency, t)
        voltage = amplitude_value * amplitude
        dac.set_voltage(voltage)

        t += 1.0 / sampling_frequency
        sg.wait_for_sampling_period(sampling_frequency)

finally:
    dac.deinit()
