import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        # Настройка ШИМ (PWM)
        # Создаем объект PWM на выбранном пине с указанной частотой
        self.pwm = GPIO.PWM(self.gpio_pin, pwm_frequency)
        # Запускаем ШИМ с коэффициентом заполнения 0% (0 Вольт)
        self.pwm.start(0)

    def set_voltage(self, voltage):
        """
        Устанавливает напряжение путем изменения скважности (Duty Cycle) ШИМ сигнала.
        Duty Cycle = (Target Voltage / Max Voltage) * 100%
        """
        # Проверка границ
        if voltage < 0:
            if self.verbose: print("Напряжение меньше 0, ставлю 0")
            voltage = 0
        elif voltage > self.dynamic_range:
            if self.verbose: print(f"Напряжение больше {self.dynamic_range}, ограничиваю")
            voltage = self.dynamic_range

        # Расчет скважности (от 0.0 до 100.0)
        duty_cycle = (voltage / self.dynamic_range) * 100.0
        
        # Применение скважности
        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(f"Set voltage: {voltage:.2f}V -> Duty Cycle: {duty_cycle:.2f}%")

    def deinit(self):
        """
        Останавливает ШИМ, сбрасывает пин в 0 и очищает GPIO.
        """
        self.pwm.stop()
        GPIO.output(self.gpio_pin, 0)
        GPIO.cleanup()

# Основной охранник (Main Guard)
if __name__ == "__main__":
    try:
        # Создаем экземпляр: Пин 12 (PWM0), Частота 500 Гц, Макс. напряжение 3.29В
        dac = PWM_DAC(12, 500, 3.290, True)
        
        while True:
            try:
                user_input = input("Введите напряжение в Вольтах: ")
                if not user_input:
                    continue
                    
                voltage = float(user_input)
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    finally:
        dac.deinit()
        print("GPIO cleanup completed")