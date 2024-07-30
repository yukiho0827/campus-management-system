import json
import socket
import struct
import datetime
import time
import threading


def res2status():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('172.31.121.23', 9501))
    server.listen(5)
    while True:
        conn, client_addr = server.accept()
        print('ip和端口：', client_addr)
        while True:
            try:
                header_top = conn.recv(4)  # 最大接收数据量1024Bytes
                if not header_top:
                    break
                header_length = struct.unpack('i', header_top)[0]
                header_json_str = conn.recv(header_length)
                header = json.loads(header_json_str)
                print(rf"header：{header}")

                # 获取状态码
                status = header.get("status_code")
                print(rf"状态码：{status}")
                # 如果文件里有内容 就send
                with open('status.txt', 'r', encoding='utf-8') as f:
                    status_code = f.readline().strip()
                print(status_code)
                if status_code:
                    header_bytes = status_code.encode('utf-8')
                else:
                    header_bytes = 'StatusIsNone'.encode('utf-8')
                top_header_bytes = struct.pack('i', len(header_bytes))
                conn.send(top_header_bytes)
                conn.send(header_bytes)
                with open('/www/wwwroot/campus_management/app01/utils/status.txt', 'w', encoding='utf-8') as f:
                    f.write('StatusIsNone')
            except Exception as err:
                # print('异常', err)
                break
        conn.close()
        print("-" * 50)


def get_file():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('172.31.121.23', 9000))
    server.listen(5)
    while True:
        conn, client_addr = server.accept()
        # print(conn)
        print('ip和端口：', client_addr, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        while True:

            try:
                time.sleep(2)
                header_top = conn.recv(4)  # 最大接收数据量1024Bytes
                if not header_top:
                    break
                header_length = struct.unpack('i', header_top)[0]
                header_json_str = conn.recv(header_length)
                header = json.loads(header_json_str)
                print(rf"header：{header}")
                # 获取文件长度
                file_size = header.get('file_size')
                print(rf"文件大小：{file_size}")

                with open(rf'save_files/{header.get("file_name")}', 'wb') as f:
                    total = 0
                    while total < file_size:
                        file_cont = conn.recv(1024)
                        f.write(file_cont)
                        total += 1024
                    print(total)
                    f.flush()
            except Exception as err:
                # print('异常', err)
                break

        conn.close()
        print("-" * 50)


t1 = threading.Thread(target=res2status, args=())
t2 = threading.Thread(target=get_file, args=())
t1.start()
t2.start()
