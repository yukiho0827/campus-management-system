# access_token = "24.930403f0fa5c120a6127a09c3dbff834.2592000.1654857016.282335-26209481"
import ast
import base64
import requests


def result_code(data):
    res = 0
    # 先简单判断 后面再丰富
    for words in data:
        if '阳性' in words['words']:
            res = 1
            break
        if '阴性' in words['words']:
            res = 2
            break
    print(f'核酸是{res}')
    return res


def health_code(data):
    res = 4

    # 检测是否是当天的健康码 用正则

    # 检测是否是绿码
    for words in data:
        if '绿码' in words['words']:
            res = 9
            break
    print(f"健康码是{res}")
    return res


def img2words(img_path, pic_type):
    # 获取access_token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    appid = "26209481"
    client_id = "LUstDco42isZjIKCWdKkfKeq"
    client_secret = "pu5GTRfvnNLRtg9XGG3mPy1aA08icfD5"

    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

    response = requests.get(host)
    access_token = response.json().get("access_token")

    # 调用通用文字识别高精度版接口
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 以二进制方式打开图文件
    # 参数image：图像base64编码
    # 下面图片路径请自行切换为自己环境的绝对路径
    with open(img_path, "rb") as f:
        image = base64.b64encode(f.read())

    body = {
        "image": image,
        "language_type": "auto_detect",
        "detect_direction": "false",
        "paragraph": "true",
        "probability": "false",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    request_url = f"{request_url}?access_token={access_token}"
    response = requests.post(request_url, headers=headers, data=body)

    content = response.content.decode("UTF-8")

    content = ast.literal_eval(content)
    words_content = content['words_result']
    # 根据图片类别调用函数
    img_type = {
        'result_code': result_code,
        "health_code": health_code,
    }
    print(img_type[pic_type](words_content))
    return img_type[pic_type](words_content)
