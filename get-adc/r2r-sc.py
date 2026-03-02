import time
import adc_plot
from r2r_adc import R2R_ADC   # предполагается, что r2r_adc.py лежит в родительской папке get

# Параметры эксперимента
DYNAMIC_RANGE = 3.3            # замените на реальное значение, измеренное мультиметром
COMPARE_TIME = 0.0001           # время сравнения для АЦП (из условия)
DURATION = 3.0                  # продолжительность измерений в секундах

# Списки для хранения данных
voltage_values = []
time_values = []

# Создаём объект АЦП
adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=COMPARE_TIME, verbose=False)

try:
    start_time = time.time()
    while time.time() - start_time < DURATION:
        # Измеряем напряжение
        voltage = adc.get_sc_voltage()
        # Записываем данные
        voltage_values.append(voltage)
        current_time = time.time() - start_time
        time_values.append(current_time)

        # Отображаем обновлённый график
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)

        # Можно добавить небольшую задержку, если нужно снизить частоту обновления
        # time.sleep(0.01)

except KeyboardInterrupt:
    print("\nИзмерения прерваны пользователем")
finally:
    # Явно удаляем объект АЦП – сработает деструктор (очистка GPIO)
    del adc
    print("Программа завершена")