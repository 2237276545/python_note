from Oracle_Dao import Oracle
import json
# mysql = MySql()  # 实例化类
# res = mysql.Select_User_Data()  # 运行body
# print(res)
#云南省最高人民法院,云南省高院,云南省最高院,云南省最高法院,云南省人民法院,云南省法院
#高级人民法院，高院，人民法院
#中级人民法院，人民法院，中院
#基层院，人民法院，基层人民法院，
#检查院，人民检查院
gj_list = ['高级人民法院','高院','人民法院','人民检查院','检查院']
zj_list = ['中级人民法院','中院','人民法院','人民检查院','检查院']
jc_list = ['基层人民法院','基层院','人民法院','人民检查院','检查院']
oracle = Oracle()
gj_result = oracle.Select_Data('SELECT SFDM,SFMC FROM YZ_SFXX')
zs_result = oracle.Select_Data('SELECT ZSDM,ZSMC FROM YZ_ZSXX')
xq_result = oracle.Select_Data('SELECT XQDM,XQMC FROM YZ_XQXX')
print(gj_result)
with open('mgc_vobac/mgc.json','a+',encoding='utf-8') as f:
    for index,names in gj_result:
        for i in gj_list:
            if names in ['北京','上海','重庆','天津']:
                f.write(names + '市' + i + '\n')
            elif names is '内蒙古':
                f.write(names + '自治区' + i + '\n')
            elif names is '新疆':
                f.write(names + '维吾尔族自治区' + i + '\n')
            elif names is '宁夏':
                f.write(names + '回族自治区' + i + '\n')
            elif names is '广西':
                f.write(names + '壮族自治区' + i + '\n')
            elif names is '西藏':
                f.write(names + '自治区' + i + '\n')
            elif names in ['香港','澳门']:
                pass
            else:
                f.write(names + '省' + i + '\n')
    for index,names in zs_result:
        for i in zj_list:
            f.write(names+i+'\n')
    for index,names in xq_result:
        for i in jc_list:
            f.write(names+i+'\n')



