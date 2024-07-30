class Unzip(object):
    def __init__(self, obj):
        self.obj = obj

    def unzip_req_post(self) -> dict:
        obj2dic = {**self.obj}
        for key, value in obj2dic.items():
            if type(value) == list and len(value) == 1:
                obj2dic[key] = value[0]
        return obj2dic
