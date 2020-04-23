from lxml import etree
import requests
from urllib import parse

base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/44/4407.html'
countrytr = 'countytr'
towntr = 'towntr'
village = 'villagetr'



# 爬取的内容转换为字典
def parse_to_dictionary(name_list,index):
    length = len(name_list)
    i = 0
    data_list = []
    while i<length:
        item = {}
        url = name_list[i]
        area = name_list[i+1]
        prefix = ''
        if index==6:
            prefix = url[2:4]
        elif index==9:
            prefix = url[4:6]
        item['url'] = prefix+'/'+url[0:index]+'.html'
        item['area'] = area
        i = i+2
        data_list.append(item)
    return data_list


def parse_code_html(base_html, flag, index, url):
    result = base_html.xpath("//tr[@class='{0}']/td/a".format(flag))
    data_list = []
    for data in result:
        data = data.xpath('text()')[0]
        data_list.append(data)
    top_list = parse_to_dictionary(data_list, index)
    print('市区内各街道页面：')
    print(top_list)
    for data in top_list:
        # 获取下一级区划代码页面
        next_url = data['url']
        area = data['area']
        new_url = parse.urljoin(url, next_url)
        print('街道：'+area + ':' + new_url)

#解析街道页面
def parse_next_html(base_html, flag, index, url):
    result = base_html.xpath("//tr[@class='{0}']/td/a".format(flag))
    data_list = []
    for data in result:
        data = data.xpath('text()')[0]
        data_list.append(data)
    top_list = parse_to_dictionary(data_list, index)
    print('各市区内页面：')
    print(top_list)
    for data in top_list:
        # 获取下一级区划代码页面
        next_url = data['url']
        area = data['area']
        new_url = parse.urljoin(url, next_url)
        print('镇区：'+area + ':' + new_url)
        base_data = getHtml(url)
        base_html = base_data[0]
        url = base_data[1]
        base_html = etree.HTML(base_html)
        parse_code_html(base_html, village, index, url)

# 解析江门市区页面
def parse_html(html,flag,index,url):
    result = html.xpath("//tr[@class='{0}']/td/a".format(flag))
    data_list = []
    for data in result:
        data = data.xpath('text()')[0]
        data_list.append(data)
    top_list = parse_to_dictionary(data_list,index)
    print('江门市三区四市页面：')
    print(top_list)
    for data in top_list:
        # 获取下一级区划代码页面
        next_url = data['url']
        area = data['area']
        new_url = parse.urljoin(url,next_url)
        print('市区：'+area+':'+new_url)
        base_data = getHtml(url)
        base_html = base_data[0]
        url = base_data[1]
        base_html = etree.HTML(base_html)
        parse_next_html(base_html, towntr, index, url)
        # start(new_url,'towntr',9)


def distinct(mData):
    new_data = []
    for data in mData:
        if data not in new_data:
            new_data.append(data)
    return new_data


def getHtml(url):
    html = requests.get(url)
    html.encoding='gb2312'
    return html.text,html.url


def start(url,flag,index):
    base_data = getHtml(url)
    base_html = base_data[0]
    url = base_data[1]
    base_html = etree.HTML(base_html)
    parse_html(base_html, flag,index,url)


if __name__ == '__main__':
    start(base_url,countrytr,6)