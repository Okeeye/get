import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    if not plt.fignum_exists(1):
        plt.figure(figsize=(10, 6))
        plt.ion()
    else:
        plt.clf()

    plt.plot(time, voltage)
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.title('Зависимость напряжения от времени')

    if time:
        plt.xlim(0, max(time))
    plt.ylim(0, max_voltage)

    plt.grid(True)
    plt.draw()
    plt.pause(0.001)

def plot_sampling_period_hist(time):
    sampling_periods = [time[i+1] - time[i] for i in range(len(time)-1)]
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods)
    plt.title('Распределение периодов измерений')
    plt.xlabel('Период, с')
    plt.ylabel('Количество измерений')
    plt.xlim(0, 0.06)
    plt.grid(True)
    plt.show()