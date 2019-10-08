import pymysql
from functools import wraps
config = {
    'host':'localhost'
    ,'user':'root'
    ,'password':'zy940808'
    ,'database':'cclzc'
    ,'charset':'utf8'
    ,'port':3306   #注意端口为int 而不是str
}

class MySql(object):
    # def __init__(self):
    #     self.reset = True  # 定义一个类属性，稍后在装饰器里更改
    #     self.func = True
    #     在类里定义一个装饰器

    def clothes(func):  # func接收body
        @wraps(func)
        def ware(self, *args, **kwargs):  # self,接收body里的self,也就是类实例
            self.conn = pymysql.connect(**config)
            self.cursor = self.conn.cursor()
            try:
                result_data = func(self, *args, **kwargs)
                self.conn.commit()
                self.cursor.close()
                self.conn.close()
                return result_data
            except:
                self.conn.rollback()
                print('Error execute: %s' % func.__name__)
        return ware

    @clothes
    def Select_User_Data(self,*args,**config):
        select_sql = '''select * from d_user_order where TELEPHTONE='15155417971' '''
        self.cursor.execute(select_sql)
        result_data = self.cursor.fetchall()
        return result_data


# b = MySql()  # 实例化类
# res = b.Select_User_Data()  # 运行body
# print(res)