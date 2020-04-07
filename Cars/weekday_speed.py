import os
import numpy as np
import pandas as pd


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


def translate_data(file_path, save_path):
    file_list = read_file_list(file_path)
    total = pd.DataFrame(columns=["Week", "RoadID", "Offset", "MaxSpeed", "MeanSpeed"])
    index = 0
    for i in range(9):
        data1 = pd.read_csv(file_path + file_list[i * 2])
        data2 = pd.read_csv(file_path + file_list[i * 2 + 1])
        data = data1.append(data2)
        data.reset_index(drop=True, inplace=True)

        road_13 = data[((data["ROADID"] == 13) & (data["SPEED"] > 0))]
        road_105 = data[((data["ROADID"] == 105) & (data["SPEED"] > 0))]
        road_106 = data[((data["ROADID"] == 106) & (data["SPEED"] > 0))]

        for j in [road_13, road_105, road_106]:
            offset = list(dict(j["OFFSET"].value_counts()).keys())
            offset.sort()
            for dis in offset:
                tmp = j[j["OFFSET"] == dis]
                total.loc[index] = [i + 1, tmp["ROADID"][tmp.index[0]], dis, tmp["SPEED"].max(),
                                    round(tmp["SPEED"].mean(), 2)]
                index += 1

    total["Week"] = total["Week"].astype(int)
    total["RoadID"] = total["RoadID"].astype(int)
    total["Offset"] = total["Offset"].astype(int)
    total["MaxSpeed"] = total["MaxSpeed"].astype(int)
    total.to_csv(save_path + "everyday_speed.csv", index=None)


def distribute_weekday_weekends(file, save_path):
    print(file)
    data = pd.read_csv(file)
    weekday = data[(data["Week"] != 1) & (data["Week"] != 7) & (data["Week"] != 8)]
    weekends = data[(data["Week"] == 1) | (data["Week"] == 7) | (data["Week"] == 8)]

    weekday_mean = weekday.pivot_table(index=["RoadID", "Offset"], values=["MeanSpeed"])
    weekday_mean["MeanSpeed"] = weekday_mean["MeanSpeed"].map(lambda e: round(e, 2))
    weekday_max = weekday.pivot_table(index=["RoadID", "Offset"], values=["MaxSpeed"], aggfunc=np.max)
    weekday_total = weekday_max.join(weekday_mean)
    weekday_total.to_csv(save_path + "weekday_speed.csv", index_label=["RoadID", "Offset"])

    weekends_mean = weekends.pivot_table(index=["RoadID", "Offset"], values=["MeanSpeed"])
    weekends_mean["MeanSpeed"] = weekends_mean["MeanSpeed"].map(lambda e: round(e, 2))
    weekends_max = weekends.pivot_table(index=["RoadID", "Offset"], values=["MaxSpeed"], aggfunc=np.max)
    weekends_total = weekends_max.join(weekends_mean)
    weekends_total.to_csv(save_path + "weekends_speed.csv", index_label=["RoadID", "Offset"])


if __name__ == '__main__':
    file_path = "./data/已处理数据/机场高速浮动车GPS数据集V2.00/"
    save_path = "./data/已处理数据/每日速度/"
    # translate_data(file_path, save_path)
    distribute_weekday_weekends(save_path + "everyday_speed.csv", save_path)
