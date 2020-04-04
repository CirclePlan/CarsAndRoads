import numpy as np
import pandas as pd
import os
import pyecharts


def read_file_list(file_path):
    '''
    函数功能：读取file_path路径下的所有csv文件
    :return:
    '''
    file_list = []
    all_list = os.listdir(file_path)
    for file in all_list:
        if os.path.splitext(file)[1] == ".csv":
            file_list.append(file)
    return file_list


def caculate(file_path, save_path):
    '''
    函数功能：分小时计算每日客流量
    :param file_path: 读取文件路径
    :param save_path: 保存文件路径
    :return:
    '''
    file_list = read_file_list(file_path)
    for i in range(9):
        print(file_path + file_list[i * 2])
        print(file_path + file_list[i * 2 + 1])
        df1 = pd.read_csv(file_path + file_list[i * 2])
        df2 = pd.read_csv(file_path + file_list[i * 2 + 1])
        hour_counts = []
        for j in range(14):
            tmp = df1["HOUR"] == j
            tmp = df1[tmp]
            car_number = len(dict(tmp["CARID"].value_counts()))
            hour_counts.append(car_number)
        for j in range(14, 24):
            tmp = df2["HOUR"] == j
            tmp = df2[tmp]
            car_number = len(dict(tmp["CARID"].value_counts()))
            hour_counts.append(car_number)
        pd.DataFrame(hour_counts, columns=["CarNumbers"]).to_csv(save_path + file_list[i * 2][:-16] + ".csv",
                                                                 index_label="Hour")


def draw_everyday(file_path, save_path):
    '''
    函数功能：绘制每日客流量折线图
    :param file_path: 读取文件路径
    :param save_path: 保存文件路径
    :return:
    '''
    car_number_list = read_file_list(file_path)
    for i in range(9):
        hour_counts = pd.read_csv(file_path + car_number_list[i], index_col=0)
        line = pyecharts.Line("各个时间段的车流量", car_number_list[i][:-4])
        line.add("各个时间段车流量", list(range(0, 24)), hour_counts["CarNumbers"], is_label_show=True)
        line.render(save_path + car_number_list[i] + ".html")


def draw_average(file_path, save_path):
    '''
    函数功能：绘制平均各个时间段车流量折线图
    :param file_path: 读取文件路径
    :param save_path: 保存文件路径
    :return:
    '''
    car_number_list = read_file_list(file_path)
    data = pd.DataFrame()
    for i in range(9):
        hour_counts = pd.read_csv(file_path + car_number_list[i], index_col=0)
        data[str(i)] = hour_counts["CarNumbers"]
    ave_car_numbers = []
    for i in range(24):
        ave_car_numbers.append(int(round(data.loc[i].mean(), 0)))
    line = pyecharts.Line("各个时间段的车流量", "平均值")
    line.add("各个时间段车流量", list(range(0, 24)), ave_car_numbers, is_label_show=True)
    line.render(save_path + "average-car-numbers.html")


if __name__ == '__main__':
    file_path = "./data/已处理数据/机场高速浮动车GPS数据集V2.00/"
    save_path = "./data/已处理数据/每日客流量/"
    caculate(file_path, save_path)
    draw_everyday(save_path, save_path)
    draw_average(save_path, save_path)
