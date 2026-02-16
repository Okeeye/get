import RPi.GPIO as GPIO

dac = [22, 27, 17, 26, 25, 21, 20, 16]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

dynamic_range = 3.18

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжние выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0

    return int(voltage / dynamic_range * 255)


def number_to_dac(value):
    for i in range(8):
        bit_value = (value >> i) & 1
        GPIO.output(dac[i], bit_value)

print("Введите напряжение (0 - 3.18 В). Для выхода нажмите Ctrl+C")

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            value = voltage_to_number(voltage)
            number_to_dac(value)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()