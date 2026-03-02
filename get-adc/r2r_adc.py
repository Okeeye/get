import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose

        # Пины для 8 бит ЦАП (младший бит - первый в списке)
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

if __name__ == "__main__":
    DYNAMIC_RANGE = 3.3  # замените на измеренное значение

    adc = None
    try:
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, verbose=True)
        print("Начало измерений. Для остановки нажмите Ctrl+C")
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nИзмерения прерваны пользователем")
    finally:
        if adc:
            del adc
        print("Программа завершена")