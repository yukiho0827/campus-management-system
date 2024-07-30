from datetime import datetime


class CreateTime(object):
    """
    查看模式，修改模式，自定义模式
    """

    def __init__(self, models='l'):
        self.models_dic = {
            "s": "%Y-%m-%d",
            "l": "%Y-%m-%d-%H-%M-%S",
        }
        self.time_fields = {}
        self.time = None
        self.__models = None
        self.set_model(models)
        self.__long_time_field = None

    def set_model(self, model):

        if model in self.models_dic:
            self.__models = model
        else:
            raise ValueError("非法的模式")

    def get_model(self):
        return self.__models

    def create_time(self):
        if self.__models == 's':
            self.time = datetime.now().strftime(self.models_dic["s"])
        if self.__models == 'l':
            self.time = datetime.now().strftime(self.models_dic["l"])
            self.__long_time_field = datetime.now().strftime(self.models_dic["l"]).split('-')
            # print(self.__long_time_field)
        return self.time

    def get_time_field(self):
        if not self.time:
            self.create_time()
        if self.__models == 's':
            self.time_fields['year'], self.time_fields['month'], self.time_fields['day'] = self.time.split('-')

        else:
            self.time_fields['year'], self.time_fields['month'], self.time_fields['day'], self.time_fields['hour'], \
            self.time_fields['min'], self.time_fields['s'] = self.__long_time_field
        return self.time_fields
