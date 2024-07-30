import os
import re
import gzip
import zipfile
import pymysql


def unzip(folder_path, img_path, data_path):
    # 制定正则规则
    rule1 = re.compile(r'.txt$')
    rule2 = re.compile(r'.jpg|.png$')
    # 目录下的文件
    file_list = os.listdir(folder_path)
    # 遍历目录下的文件
    for files in file_list:
        # 拼接文件路径
        file_path = os.path.join(folder_path, files)
        print(file_path)
        with gzip.open('../../app01/data/zip/data-1.gz', 'rb') as f:

            file_content = b""
            total = os.path.getsize('../../app01/data/zip/data-1.gz')
            while total > 0:
                file_content += f.read(1024)
                total -= 1024
            print(file_content)
        file_split = file_path.split(".")
        if file_split[1] == 'gz':
            file_split[1] = 'zip'
        print(file_split)
        new_file_path = ".".join(file_split)
        print(new_file_path)
        os.rename(file_path, new_file_path)

        with zipfile.ZipFile(new_file_path, 'r') as zf:
            # 遍历文件列表
            for file in zf.namelist():
                print(file)
                # 文件名如果符合规则1，就再判断
                if rule1.findall(file):
                    # 文件名如果在data目录下没有重复，就解压（可以先对目录中的数字文件名排序，用二分查找提升效率）
                    if file not in os.listdir(data_path):
                        zf.extract(file, data_path)
                # 文件名如果符合规则2，就再判断
                if rule2.findall(file):
                    # 文件名如果在img目录下没有重复，就解压
                    if file not in os.listdir(img_path):
                        zf.extract(file, img_path)
                # 可以删除解压过的文件夹，有需求时添加功能即可


def update_db(folder_path):
    # 文件名列表
    file_name_list = os.listdir(folder_path)
    # 规则
    rule = re.compile(r'\d+', flags=re.S)
    # 连接数据库
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', charset="utf8",
                           db="sdszck")
    cursor = conn.cursor()
    # 图片路径
    photo_folder_path = os.path.dirname(folder_path)
    # 给路径添加双斜杠（单斜杠在mysql里会被转义不显示）
    photo_folder_path = [*photo_folder_path]
    for i in range(len(photo_folder_path)):
        if photo_folder_path[i] == '\\':
            photo_folder_path[i] = r'\\'
    photo_folder_path = "".join(photo_folder_path) + r"\\img"
    # 栈实现循环读取文件内容
    while file_name_list:
        filename = file_name_list.pop()
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            cont = f.readlines()
            temperature, num = cont[0].strip(), cont[3].strip()
            photo_path = rf'{photo_folder_path}\\{rule.findall(filename)[0]}.jpg'

            # 执行SQL语句
            sql = 'replace into app01_abnormalinfo(num,photo_path,temperature) values("{}","{}","{}")'.format(num,
                                                                                                              photo_path,
                                                                                                              temperature)
            cursor.execute(sql)
            conn.commit()

            # 关闭数据库连接
    cursor.close()
    conn.close()


zip_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'data\zip')
save_folder_path = os.path.dirname(zip_folder_path)
# unzip(zip_folder_path, rf'{save_folder_path}\img', rf'{save_folder_path}\info')
# update_db(rf'{save_folder_path}\info')
