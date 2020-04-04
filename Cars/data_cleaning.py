import numpy as np
import pandas as pd
import os

file_path = "data/机场高速浮动车GPS数据集V1.00/"


def read_file_list():
    '''
    函数功能：读取file_path路径下的所有文件
    :return:
    '''
    file_list = os.listdir(file_path)
    return file_list


def check(file_list):
    '''
    函数功能：检查除SIGNALTIME之外的列有无缺失值
    :param file_list: 文件列表
    :return:
    '''
    for file in file_list:
        print(file_path + file)
        data = pd.read_excel(file_path + file)
        print(data.describe())
        for i in data:
            if i == "SIGNALTIME":
                break
            for j in range(len(data[i])):
                if str(data[i][j]) == 'nan':
                    print(j)


def date_segmentation(file_list):
    '''
    函数功能：完成对时间的分割，并保存处理后的数据到新文件
    :param file_list: 文件列表
    :return:
    '''
    for i in range(len(file_list)):
        data = pd.read_excel(file_path + file_list[i])
        print(i, file_list[i])
        data["SIGNALTIME"] = data["SIGNALTIME"].map(lambda e: str(str(e).split()[0]))
        hour = []
        minute = []
        second = []
        for j in range(len(data["SIGNALTIME"])):
            if data["SIGNALTIME"][j] == 'nan':
                print(j)
                data.drop(j, inplace=True)
            else:
                tmp = data["SIGNALTIME"][j].split(":")
                hour.append(tmp[0])
                minute.append(tmp[1])
                second.append(tmp[2])
        data["HOUR"] = hour
        data["MINUTE"] = minute
        data["SECOND"] = second
        data.drop(["SIGNALTIME"], axis=1, inplace=True)
        data.to_csv("./data/已处理数据/" + file_list[i][:-5] + ".csv", index=None)


if __name__ == '__main__':
    file_list = read_file_list()
    check(file_list)
    date_segmentation(file_list)
