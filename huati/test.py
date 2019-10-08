import cx_Oracle
conn=cx_Oracle.connect('zhfyssfw','zhfyssfw','222.197.219.12:1521/ORCLPDB')
c=conn.cursor()
x = c.execute('select * from yz_qg')
x.fetchone()
c.close()
conn.close()

