import sys
import time
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

sys.path.append('..')

import adc_plot

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose


        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        self.number_to_dac(0)
        GPIO.cleanup(self.bits_gpio + [self.comp_gpio])

    def number_to_dac(self, number):
        for i in range(8):
            bit = (number >> i) & 1
            GPIO.output(self.bits_gpio[i], bit)
        if self.verbose:
            print(f"Установлено число {number} на ЦАП")

    def sequential_counting_adc(self):
        for code in range(256):
            self.number_to_dac(code)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"Превышение при коде {code}")
                return code

        if self.verbose:
            print("Превышение не достигнуто, возвращаю 255")
        return 255

    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        voltage = code * self.dynamic_range / 255.0
        if self.verbose:
            print(f"Код: {code}, напряжение: {voltage:.3f} В")
        return voltage


DYNAMIC_RANGE = 3.3
COMPARE_TIME = 0.000001
DURATION = 30.0

voltage_values = []
time_values = []

adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=COMPARE_TIME, verbose=False)

try:
    start_time = time.time()
    while time.time() - start_time < DURATION:
        voltage = adc.get_sc_voltage()
        voltage_values.append(voltage)
        current_time = time.time() - start_time
        time_values.append(current_time)
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)

    plt.ioff()
    adc_plot.plot_sampling_period_hist(time_values)

except KeyboardInterrupt:
    print("\nИзмерения прерваны пользователем")
finally:
    del adc
    print("Программа завершена")