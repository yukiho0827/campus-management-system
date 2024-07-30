import os
import pymysql
import datetime


def data2mysql(folder_path):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', charset="utf8",
                           db="sdszck")
    cursor = conn.cursor()
    file_name_list = os.listdir(folder_path)
    while file_name_list:
        # 获取文件名
        file_name = file_name_list.pop()
        # 获取时间
        file_info_list = file_name.split("-")
        # 提取时间
        ymd = "-".join((file_info_list[0], file_info_list[1], file_info_list[2]))
        create_time_info = file_info_list[3].split("_")
        create_time_info.pop()
        hms = ":".join(create_time_info)
        create_time = datetime.datetime.strptime(rf"{ymd} {hms}", "%Y-%m-%d %H:%M:%S")
        # 拼接路径
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            f.readline()
            cont = "".join(f.readline()).split("\t")
            cont[-1] = cont[-1].replace("\n", "")
            # 解包
            humidity, temp, co2, liquid, gas = cont[0], cont[1], cont[2], cont[3], cont[4]

        sql = 'replace into app01_uploadfiledata(humidity, temp, co2, liquid, gas, create_time) values("{}","{}",' \
              '"{}","{}","{}","{}")'.format(
            humidity, temp, co2, liquid, gas, create_time)
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()


data2mysql(r"D:\PycharmProjects\campus_management\app01\data\info")
