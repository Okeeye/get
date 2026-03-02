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



    # Устанавливаем границы осей

    if time:                           # если список не пуст

        plt.xlim(0, max(time))         # правая граница – последний измеренный момент

    plt.ylim(0, max_voltage)



    plt.grid(True)

    plt.draw()

    plt.pause(0.001)                   # небольшая пауза для обновления окна

