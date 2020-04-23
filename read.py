import json
import os
import xlwt
import xlrd
import requests

base_url = 'http://19.120.100.24:7001/Jmrlzy/train/ajaxListWorkType.do'
add_url = 'http://19.120.100.24:7001/Jmrlzy/train/ajaxSaveWorkType.do'

WORKTYPECODE = 'WORKTYPECODE'
WORKTYPENAME = 'WORKTYPENAME'
ORDERCODE = 'ORDERCODE'

header = {
        'cookie':'sessionTime=5000; sessionTimeout=7; JSESSIONID=FB00FC7905C78E00E0713E04911745D3;'
    }

# 读excel文件，返回list
def read_excel():
    book = xlrd.open_workbook('新增工种名.xls')
    sheet1 = book.sheets()[0]
    nrows = sheet1.nrows
    ncols = sheet1.ncols
    data_list = []
    for i in range(1,nrows):
        item = {}
        workTypeCode = sheet1.row_values(i)[0]
        workTypeName = sheet1.row_values(i)[1]
        orderCode = int(sheet1.row_values(i)[2])
        item.update(WORKTYPECODE=workTypeCode)
        item.update(WORKTYPENAME=workTypeName)
        item.update(ORDERCODE=orderCode)
        data_list.append(item)
    return data_list;

# 将json数据提取出来，并以list形式返回
def parse_json(content):
    list = []
    data = content['Rows']
    print(data)
    for item in data:
        job_name = item['workTypeName']
        list.append(job_name)
    return list

def write_to_excel(content):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('output')
    sheet.write(0,0,'工种名')
    data_list = parse_json(content)
    print(data_list)
    for i in range(1,len(data_list)):
        sheet.write(i,0,data_list[i-1])
    book.save('output.xls')

def getData():
    data = {
        'keyword':'',
        'page':'1',
        'pagesize':'940',
        'flipInfo.currentpage':'1',
        'flipInfo.pageSize':'940'
    }
    res = requests.post(base_url,data=data,headers=header)
    # print(res.text)
    content = json.loads(res.text)
    write_to_excel(content)
    # parse_json(content)

def add_work():
    data_list = read_excel()
    for i in range(0,len(data_list)):
        item = data_list[i]
        print(item)
        data = {
            'workType.workTypeCode':item['WORKTYPECODE'],
            'workType.workTypeName':item['WORKTYPENAME'],
            'workType.orderNo':item['ORDERCODE']
        }
        res = requests.post(add_url,headers=header,data=data)
        print(res.text)
    return ;

if __name__ == '__main__':
    add_work()
    # read_excel()
    # getData()