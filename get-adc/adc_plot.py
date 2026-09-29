
import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.title("Зависимость напряжения на выходе 8-bit DAC от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(left=0, right=max(time) if time else 1)
    plt.ylim(bottom=0, top=max_voltage)
    plt.grid(True)
    plt.show()

def plot_sampling_period_hist(time):
    if len(time) < 2:
        return
    sampling_periods = [time[i+1] - time[i] for i in range(len(time)-1)]
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=50)
    plt.title("Распределение периодов дискретизации измерений")
    plt.xlabel("Период дискретизации, с")
    plt.ylabel("Количество измерений")
    plt.xlim(0, 0.06)
    plt.grid(True)
    plt.show()
