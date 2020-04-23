import json
import os
import xlwt
import xlrd
import requests
import pandas as pd

# 读excel文件，返回list
def read_excel():
    data = pd.read_excel('自然减员名单.xlsx',sheet_name=0)
    d = data.duplicated(subset='身份证号码',keep='last')
    d = d[d]
    new = data.iloc[d.index]
    pd.DataFrame(new).to_excel('new.xls')

if __name__ == '__main__':
    read_excel()
