import jieba

with open('E:\\pycharm_project\\PyRouge-master\\Data_processing\\law_rouge.json','r',encoding='utf-8') as f:
    law_data = f.readlines()
with open('E:\\pycharm_project\\PyRouge-master\\Data_processing\\law_other_rouge.json','r',encoding='utf-8') as f:
    law_other_data = f.readlines()