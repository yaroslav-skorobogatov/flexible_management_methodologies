import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Функция для построения трех гистограмм для одного параметра
def plot_histograms(df, parameter_name, dir_save):
    data = df[parameter_name]

    # Разделим данные на num_groups равных частей
    df['Group'] = pd.cut(df.index, bins=20, labels=False)

    # Вычисление средних и размахов для каждой группы
    group_means = df.groupby('Group')[parameter_name].mean()
    group_ranges = df.groupby('Group')[parameter_name].apply(lambda x: x.max() - x.min())

    fig = plt.figure(figsize=(10, 10))

    # 1. Гистограмма для всех измерений
    plt.subplot(3, 1, 1)
    data.hist(bins=20, edgecolor='black')
    plt.title(f'Гистограмма для всех измерений ({parameter_name})')

    # 2. Гистограмма для 20 групповых средних
    plt.subplot(3, 1, 2)
    group_means.hist(bins=20, edgecolor='black')
    plt.title(f'Гистограмма для 20 групповых средних ({parameter_name})')

    # 3. Гистограмма для 20 групповых размахов
    plt.subplot(3, 1, 3)
    group_ranges.hist(bins=20, edgecolor='black')
    plt.title(f'Гистограмма для 20 групповых размахов ({parameter_name})')

    # Плотность графиков
    plt.tight_layout()
    #plt.show()
    os.makedirs(dir_save, exist_ok=True)
    output_file = dir_save + "/" + parameter_name.replace(" ", "_")
    plt.savefig(output_file)
    plt.close(fig)


# Константы для контроля пределов в зависимости от размера подгруппы
constants = {
    2: {'A_2': 1.880, 'D_3': None, 'D_4': 3.268},
    3: {'A_2': 1.023, 'D_3': None, 'D_4': 2.574},
    4: {'A_2': 0.729, 'D_3': None, 'D_4': 2.282},
    5: {'A_2': 0.577, 'D_3': None, 'D_4': 2.114},
    6: {'A_2': 0.483, 'D_3': None, 'D_4': 2.004},
    7: {'A_2': 0.419, 'D_3': 0.076, 'D_4': 1.924},
    8: {'A_2': 0.373, 'D_3': 0.136, 'D_4': 1.864},
    9: {'A_2': 0.337, 'D_3': 0.184, 'D_4': 1.816},
    10: {'A_2': 0.308, 'D_3': 0.223, 'D_4': 1.777}
}


# Функция для расчета и построения карт Шухарта (X-карты и R-карты)
def plot_control_charts(df, parameter_name, n, dir_save):
    # Разделим данные на n равных частей
    df['Group'] = pd.cut(df.index, bins=20, labels=False)

    # Вычисление средних и размахов для каждой группы
    group_means = df.groupby('Group')[parameter_name].mean()
    group_ranges = df.groupby('Group')[parameter_name].apply(lambda x: x.max() - x.min())

    # Средние значения для всех средних и всех размахов
    X_bar = np.mean(group_means)
    R_bar = np.mean(group_ranges)

    # Получаем значения A_2, D_3, D_4 для данного n
    A_2 = constants[n]['A_2']
    D_3 = constants[n]['D_3']
    D_4 = constants[n]['D_4']

    # Расчет контрольных пределов для X-карты и R-карты
    UCL_X = X_bar + A_2 * R_bar
    LCL_X = X_bar - A_2 * R_bar
    UCL_R = D_4 * R_bar
    LCL_R = D_3 * R_bar if D_3 is not None else 0

    # Создание фигуры и осей для двух подграфиков (X-карта сверху и R-карта снизу)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # Построение X-карты (средние значения) на верхней оси
    ax1.plot(group_means, marker='o', label='Средние по группам', color='blue')
    ax1.axhline(X_bar, color='green', linestyle='--', label='Центральная линия X̅')
    ax1.axhline(UCL_X, color='red', linestyle='--', label='UCL X̅')
    ax1.axhline(LCL_X, color='red', linestyle='--', label='LCL X̅')
    ax1.set_title(f"X-карта для {parameter_name}")
    ax1.legend()

    # Построение R-карты (размахи) на нижней оси
    ax2.plot(group_ranges, marker='o', label='Размахи по группам', color='orange')
    ax2.axhline(R_bar, color='green', linestyle='--', label='Центральная линия R̅')
    ax2.axhline(UCL_R, color='red', linestyle='--', label='UCL R̅')
    ax2.axhline(LCL_R, color='red', linestyle='--', label='LCL R̅')
    ax2.set_title(f"R-карта для {parameter_name}")
    ax2.legend()

    # Плотность графиков
    plt.tight_layout()
    #plt.show()
    os.makedirs(dir_save, exist_ok=True)
    output_file = dir_save + "/" + parameter_name.replace(" ", "_")  + "_control_charts"
    plt.savefig(output_file)
    plt.close(fig)

# Пути к Excel-файлам
file_path_list = ['source/20-1.xlsx', 'source/30-1.xlsx', 'source/40-1.xlsx']

for file_path in file_path_list:
    # Названия столбцов для данных
    column_names = ['Fmax', 'σ_M', 'dL при Fmax']
    df = pd.read_excel(file_path, skiprows=1, decimal=',', usecols=[2, 3, 4], names=column_names)
    #print(df.head())
    dir_save = f"result/{file_path.strip().split('/')[-1].split('.')[0]}"

    for param in column_names:
        plot_histograms(df, param, dir_save)  # Гистограммы для каждого параметра
        plot_control_charts(df, param, 10, dir_save)  # Карты Шухарта для каждого параметра