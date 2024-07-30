import os
import re
import pymysql
import datetime


def img2mysql(folder_path):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', charset="utf8",
                           db="sdszck")
    cursor = conn.cursor()
    file_name_list = os.listdir(folder_path)
    # print(file_name_list)
    while file_name_list:
        # 获取文件名
        file_name = file_name_list.pop()
        # 提取文件名信息
        file_info_list = file_name.split("-")
        # 提取状态
        status = file_info_list[0]
        # 提取时间
        ymd = "-".join((file_info_list[1], file_info_list[2], file_info_list[3]))
        create_time_info = file_info_list[4].split("_")
        create_time_info.pop()
        hms = ":".join(create_time_info)
        create_time = datetime.datetime.strptime(rf"{ymd} {hms}", "%Y-%m-%d %H:%M:%S")

        # 拼接存储数据库的文件路径
        file_path = os.path.join(rf"img", file_name)
        file_path = [*file_path]
        for i in range(len(file_path)):
            if file_path[i] == '\\':
                file_path[i] = r'//'
        file_path = "".join(file_path)
        # 执行SQL语句
        sql = 'replace into app01_uploadimginfo(create_time,res,photo) values("{}","{}","{}")'.format(create_time,
                                                                                                      status,
                                                                                                      file_path)
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()


img2mysql(r"D:\PycharmProjects\campus_management\app01\static\img")
