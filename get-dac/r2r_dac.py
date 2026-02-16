import RPi.GPIO as GPIO

class R2R_DAC:
    # ИСПРАВЛЕНО: __init__ вместо init
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        # Настройка пинов
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=GPIO.LOW)
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        # УЛУЧШЕНИЕ: вычисляем макс. значение динамически (2^N - 1)
        max_val = 2**len(self.gpio_bits) - 1
        number = max(0, min(max_val, int(number)))

        # УЛУЧШЕНИЕ: используем длину списка пинов вместо хардкода "8"
        dac_val_list = [int(bit) for bit in bin(number)[2:].zfill(len(self.gpio_bits))]

        GPIO.output(self.gpio_bits, dac_val_list)

        if self.verbose:
            print(f"Output number: {number} -> {dac_val_list}")

    def set_voltage(self, voltage):
        if voltage < 0.0:
            if self.verbose: print("Напряжение меньше 0, ставлю 0")
            voltage = 0
        elif voltage > self.dynamic_range:
            # ИСПРАВЛЕНО: была опечатка synamic_range
            if self.verbose: print(f"Напряжение больше {self.dynamic_range}, ограничиваю")
            voltage = self.dynamic_range

        # Вычисляем макс значение снова для пересчета
        max_val = 2**len(self.gpio_bits) - 1
        value = int(round((voltage / self.dynamic_range) * max_val))

        self.set_number(value)


# ДОПИСАНО: Основной блок (Main Guard) из задания №6
if __name__ == "__main__":
    try:
        # Создаем объект класса. Пины и напряжение взяты из задания.
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        
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
        print("\nПрограмма остановлена")
    finally:
        # Важно: вызываем деструктор при выходе
        dac.deinit()