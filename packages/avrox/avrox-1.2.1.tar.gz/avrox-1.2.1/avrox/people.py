class People():
    def __init__(self,
                 name=None,
                 gender=None,
                 age=None,
                 work=None,
                 hobby=None,
                 characteristic=None):
        self.__name = name
        self.__gender = gender
        self.__age = age
        self.__work = work
        self.__hobby = hobby
        self.__characteristic = characteristic

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_age(self):
        return self.__age

    def get_work(self):
        return self.__work

    def get_hobby(self):
        return self.__hobby

    def get_characteristic(self):
        return self.__characteristic

    def change_name(self, __name):
        self.__name = __name

    def change___gender(self, __gender):
        self.__gender = __gender

    def change_age(self, __age):
        self.__age = __age

    def change___hobby(self, __hobby):
        self.__hobby = __hobby

    def change___characteristic(self, __characteristic):
        self.__characteristic = __characteristic
