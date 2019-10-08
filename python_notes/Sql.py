import os, pprint,uuid
import cx_Oracle as oracle
from functools import wraps

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


#这是函数装饰器
def robust(actual_do):
    @wraps(actual_do)
    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except:
            print('Error execute: %s' % actual_do.__name__)
            # traceback.print_exc()
    return add_robust

# 返回是一个列表，数据库中的每一行对应列表中的一个元组
class ZhfyYqxx(object):
    def __enter__(self):
        self.conn = oracle.connect('zhfyssfw/zhfyssfw@222.197.219.12:1521/ORCLPDB')
        self.cursor = self.conn.cursor()
        return self

    @robust
    def selectData(self):
        select_YQXX_sql = '''SELECT YQBH,YQBT,TO_CHAR ( FBSJ ,'YYYY-MM-DD hh24:mi:ss' ) FBSJ,CLBZ  FROM YD_YQXX WHERE TO_CHAR ( ZQRQ, 'YYYY-MM-DD  hh24:mi:ss' ) >= TO_CHAR ( SYSDATE - 30, 'YYYY-MM-DD  hh24:mi:ss' ) AND TO_CHAR ( ZQRQ, 'YYYY-MM-DD' ) <= TO_CHAR ( SYSDATE, 'YYYY-MM-DD' ) '''
        self.cursor.execute(select_YQXX_sql)
        result_data = self.cursor.fetchall()
        return result_data

    @robust
    def selectDataCount(self):
        select_YQXX_sql = '''SELECT COUNT(*) FROM YD_YQXX WHERE TO_CHAR ( ZQRQ, 'YYYY-MM-DD' ) >= TO_CHAR ( SYSDATE - 30, 'YYYY-MM-DD' ) AND TO_CHAR ( ZQRQ, 'YYYY-MM-DD' ) <= TO_CHAR ( SYSDATE, 'YYYY-MM-DD' ) '''
        self.cursor.execute(select_YQXX_sql)
        result_data = self.cursor.fetchall()
        return result_data

    @robust
    def selectTopNumber(self, number):
        select_YQXX_sql = "SELECT YQBH,YQBT,FBSJ,CLBZ   FROM YD_YQXX WHERE SUBSTR(CLBZ,5,1) = '0' AND TO_CHAR ( FBSJ, 'YYYY-MM-DD' ) >= TO_CHAR ( '2019-06-15' )  AND TO_CHAR ( FBSJ, 'YYYY-MM-DD' ) <= TO_CHAR ( '2019-09-15')  AND ROWNUM<'{}'".format(
            number + 1)
        self.cursor.execute(select_YQXX_sql)
        result_data = self.cursor.fetchall()
        return result_data

    def insertZYYQ(self,dict):
        insert_ZYYQ_sql = "INSERT INTO YD_ZYYQ (ZYBH,ZYTJ,YQBT,FBSJ,YLXX) VALUES (:ZYBH,:ZYTJ,:YQBT,:FBSJ,:YLXX)"
        self.cursor.execute(insert_ZYYQ_sql,dict)
        self.conn.commit()
        return "YES"

    @robust
    def insertZYYQGL(self,ZYBH,YQBH="",SJBH="",AJBH=""):
        insert_ZYYQGL_sql = "INSERT INTO YD_ZYYQGL (ZYBH,YQBH,SJBH,AJBH ) VALUES ('{}','{}','{}','{}')".format(ZYBH,YQBH,SJBH,AJBH)
        self.cursor.execute(insert_ZYYQGL_sql)
        self.conn.commit()
        return "YES"

    def updateZYYQ(self,dict):
        update_ZYYQ_sql = "UPDATE YD_ZYYQ set ZYTJ=:ZYTJ,YQBT=:YQBT,FBSJ=:FBSJ,YLXX=:YLXX WHERE ZYBH=:ZYBH"
        self.cursor.execute(update_ZYYQ_sql,dict)
        self.conn.commit()
        return "YES"

    @robust
    def OmnipotentMethod(self,sql):
        select_sql = sql
        self.cursor.execute(select_sql)
        result_data = self.cursor.fetchall()
        return result_data

    def updateYQXXCLBZ(self,YQBH):
        update_ZYYQ_sql = "	UPDATE YD_YQXX SET  CLBZ = SUBSTR(CLBZ,0,5) || '1'  WHERE YQBH='{}'".format(YQBH)
        self.cursor.execute(update_ZYYQ_sql)
        self.conn.commit()
        return "YES"

    def selectDataZYYQ(self):
        select_YQXX_sql = '''SELECT ZYBH,ZYTJ,YQBT,KSSJ,JSSJ FROM YD_ZYYQ'''
        self.cursor.execute(select_YQXX_sql)
        result_data = self.cursor.fetchall()
        return result_data

    def emptyTable(self,table):
        empty_Table_sql = "TRUNCATE TABLE {}".format(table)
        self.cursor.execute(empty_Table_sql)
        self.conn.commit()
        return "YES"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()



def main():
    with ZhfyYqxx() as z:
        res = z.selectTopNumber(2)
    for result in res:
        ZYBH = uuid.uuid1()
        dict = {
            "ZYBH": str(ZYBH),
            "ZYTJ": 1,
            "YQBT": result[1],
            "FBSJ": result[2],
            "YLXX": ""
        }
        with ZhfyYqxx() as z:
            z.insertZYYQ(dict)
            z.insertZYYQGL(ZYBH=ZYBH, YQBH=result[0])
            z.updateYQXXCLBZ(result[0])


def emptyT():
    with ZhfyYqxx() as z:
        print(z.emptyTable("YD_ZYYQGL"))


if __name__ == '__main__':
    main()