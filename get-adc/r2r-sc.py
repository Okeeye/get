import time
import matplotlib.pyplot as plt
import r2r_adc
import adc_plot

DYNAMIC_RANGE = 3.3
COMPARE_TIME = 0.001  # Уменьшено: 100мс → 1мс (R-2R устанавливается быстро)
DURATION = 30.0
PLOT_INTERVAL = 0.5   # Обновлять график не чаще чем раз в 0.5 сек

adc = r2r_adc.R2R_ADC(
    dynamic_range=DYNAMIC_RANGE,
    compare_time=COMPARE_TIME,
    verbose=False
)

voltage_values = []
time_values = []

try:
    start_time = time.time()
    last_plot_time = start_time

    while True:
        current_time = time.time()
        elapsed = current_time - start_time

        if elapsed >= DURATION:
            break

        # Измерение
        voltage = adc.get_sc_voltage()
        time_values.append(elapsed)
        voltage_values.append(voltage)

        # Обновляем график только по таймеру, а не каждую итерацию
        if current_time - last_plot_time >= PLOT_INTERVAL:
            adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
            last_plot_time = current_time

    # Финальная отрисовка
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    plt.ioff()
    adc_plot.plot_sampling_period_hist(time_values)

except KeyboardInterrupt:
    print("\nИзмерения прерваны пользователем")

finally:
    del adc
    print(f"Програм��а завершена. Собрано {len(voltage_values)} отсчётов.")
