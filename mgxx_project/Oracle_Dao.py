import cx_Oracle
from functools import wraps

class Oracle(object):
    # def __init__(self):
    #     self.reset = True  # 定义一个类属性，稍后在装饰器里更改
    #     self.func = True
    #     在类里定义一个装饰器

    def clothes(func):  # func接收body
        @wraps(func)
        def ware(self, *args, **kwargs):  # self,接收body里的self,也就是类实例
            self.conn = cx_Oracle.connect('zhfyssfw','zhfyssfw','43.228.77.55:1521/ORCLPDB')
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
    def Select_Data(self,limit,*args,**config):
        print(limit)
        select_sql = limit
        self.cursor.execute(select_sql)
        result_data = self.cursor.fetchall()
        return result_data