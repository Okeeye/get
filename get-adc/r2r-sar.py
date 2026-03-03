import time
import r2r_adc
import adc_plot

DYNAMIC_RANGE = 3.295
adc = r2r_adc.R2R_ADC(dynamic_range=3.295, compare_time=0.001, verbose=False)

voltage_values = []
time_values = []

DURATION = 10.0

try:
    start_time = time.time()

    while time.time() - start_time < DURATION:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time() - start_time)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
    adc_plot.plot_sampling_period_hist(time_values)
    
finally:
    del adc