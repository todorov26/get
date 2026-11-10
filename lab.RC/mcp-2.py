
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

from mcp3021_driver import MCP3021


def plot_voltage_vs_time(time_list, voltage_list, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, voltage_list)
    plt.title("Зависимость напряжения на входе MCP3021 от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, max(time_list))
    plt.ylim(0, max_voltage)
    plt.grid(True)


def plot_sampling_period_hist(time_list):
    # длительность каждого измерения = разница между соседними отсчётами времени
    periods = [t2 - t1 for t1, t2 in zip(time_list, time_list[1:])]

    plt.figure(figsize=(10, 6))
    plt.hist(periods, bins=30)
    plt.title("Распределение измерений по продолжительности")
    plt.xlabel("Продолжительность измерения, с")
    plt.ylabel("Количество измерений")
    plt.xlim(0, max(periods))
    plt.grid(True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--range", type=float, default=5.0,
                        help="динамический диапазон АЦП, В (измерьте на PWR мультиметром)")
    parser.add_argument("-d", "--duration", type=float, default=10.0,
                        help="продолжительность измерений, с")
    args = parser.parse_args()

    voltage_values = []
    time_values = []

    adc = None
    try:
        adc = MCP3021(dynamic_range=args.range)

        start = time.time()
        while time.time() - start < args.duration:
            voltage_values.append(adc.get_voltage())
            time_values.append(time.time() - start)
    except KeyboardInterrupt:
        pass
    finally:
        if adc is not None:
            adc.deinit()

    if len(time_values) < 2:
        print("Недостаточно данных для построения графиков")
        return

    print(f"Измерений: {len(time_values)}, "
          f"средний период: {time_values[-1] / (len(time_values) - 1) * 1000:.2f} мс")

    plot_voltage_vs_time(time_values, voltage_values, args.range)
    plt.savefig('rc-plot.png', dpi=300)

    data_to_save = np.column_stack((time_values, voltage_values))

    np.savetxt(
        'data.csv',
        data_to_save,
        delimiter=',',
        comments='',
        fmt='%.6f'
    )



if __name__ == "__main__":
    main()