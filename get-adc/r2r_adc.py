
import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        self.num_bits = len(self.bits_gpio)
        self.max_value = (1 << self.num_bits) - 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        self.number_to_dac(0)
        GPIO.cleanup(self.bits_gpio + [self.comp_gpio])
        if self.verbose:
            print("R2R_ADC деинициализирован")

    def number_to_dac(self, number):
        for i, pin in enumerate(self.bits_gpio):
            GPIO.output(pin, (number >> i) & 1)

    def successive_approximation_adc(self):
        result = 0
        bit_mask = 1 << (self.num_bits - 1)

        for _ in range(self.num_bits):
            test_value = result | bit_mask
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == 1:
                result = test_value

            bit_mask >>= 1

        return result

    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        voltage = (number / self.max_value) * self.dynamic_range
        return voltage

    def sequential_counting_adc(self):
        for number in range(self.max_value + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == 1:
                return number

        return self.max_value

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = (number / self.max_value) * self.dynamic_range
        return voltage


if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.290, verbose=True)
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение (SAR): {voltage:.3f} В")
    except KeyboardInterrupt:
        pass
    finally:
        adc.deinit()
