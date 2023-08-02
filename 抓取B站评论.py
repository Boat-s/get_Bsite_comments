import requests
import time
import json
import csv
import random
import re
# 爬虫类（面向对象）
class JsonProcess:
    def __init__(self):
        self.Json_data = ''
        self.Barrage_data=''
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'
        }
	
    # 发送爬取评论数据请求
    def spider(self, URL):
        url = URL
        response = requests.get(url, headers=self.headers, verify=False)
        response.encoding = 'utf-8'
        self.Json_data = response.json()['data']['replies']
    #爬取弹幕
    def spider_Barrage(self,cid):
        url = f'http://comment.bilibili.com/{cid}.xml'
        resp = requests.get(url, headers=self.headers, verify=False)
        resp.encoding = 'utf-8'
        self.Barrage_data = re.findall('<d p=".*?">(.*?)</d>', resp.text)
        
#10位时间戳转换为时间字符串
def trans_date(v_timestamp):
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


# 爬取评论
def getReplies(jp, i):
    print("672756810 我不想做这样的人 981214823 不被大风吹倒 412935552 后浪")
    oid=int(input("请输入你要爬取评论的oid:"))

    # 不知道具体有多少页的评论，所以使用死循环一直爬
    print(oid)
    csvname=input("请输入你要保存的csv文件名:-->")
    with open(f'{csvname}.csv', 'a', encoding='gbk', newline='') as f:
        a = csv.writer(f)
        # 字段存储一次就行，无需放到循环体中
        field = ['评论id', '类型','用户昵称', '性别', '个性签名', '评论内容','评论时间', '点赞数']
        a.writerow(field)
        print([ '用户昵称', '性别', '个性签名', '评论内容','评论时间', '点赞数'])
        # 遍历输入的页数 
        while True:
            url = f'http://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={i}&type=1&oid={oid}&mode=3&plat=1'
            jp.spider(url)
            # 如果当前页为空（爬到头了），跳出循环，程序结束。
            if jp.Json_data is None:
                print("数据爬取完毕或者被封禁")
                break
            # 组装数据，存入csv。
            for node in jp.Json_data:
                print('===================')
                rpid = node['rpid']                     #id
                name = node['member']['uname']          #名称
                sex = node['member']['sex']             #性别
                sign = node['member']['sign']           #个性名称
                content = node['content']['message']    #评论
                like = node['like']                     #点赞数
                ctime = node['ctime']                    #评论时间
                ctime=trans_date(ctime)
                mode="主评论"
                list_data = [rpid, mode,name, sex, sign, content, ctime,like]
                try:
                    print(list_data)
                    a.writerow(list_data)               #csv写入数据
                except:
                    pass
                # 如果有子评论，爬取子评论
                if node['replies'] is not None:
                    reply = JsonProcess()
                    root=rpid
                        # 页数
                    pn = 1
                        # 不知道具体有多少页的评论，所以使用死循环一直爬
                    while True:
                        url = f'http://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={pn}&type=1&oid={oid}&ps=10&root={root}'
                        #防止封禁
                        time.sleep(random.uniform(0.8, 1.2))
                        reply.spider(url)
                            # 如果当前页为空（爬到头了），跳出子评论
                        if reply.Json_data is None:
                            break
                            # 组装数据，存入csv
                        for node in reply.Json_data:
                            rpid = node['rpid']                     #id
                            name = node['member']['uname']          #名称
                            sex = node['member']['sex']             #性别
                            sign = node['member']['sign']           #个性名称
                            content = node['content']['message']    #评论
                            like = node['like']                     #点赞数
                            ctime=node['ctime']                     #评论时间
                            ctime=trans_date(ctime)
                            mode="子评论"
                            list_data = [rpid, mode,name, sex, sign, content,ctime, like]
                            try:                                    #存储数据
                                print(list_data)
                                a.writerow(list_data)
                            except:
                                pass
                            # 每爬完一次，页数加1
                        pn += 1

            # 每爬完一页，页数加1
            i += 1
        print('-------------评论获取完毕！-------------')

def getBarrage(jp):
    print("我不想做这样的人  332877650 不被大风吹倒  710654199 后浪  186803402")
    cid=int(input("请输入你要爬取评论的cid:"))
    JP.spider_Barrage(cid)
    csvname=input("请输入你要保存的csv文件名:-->")
        # 获取所有评论内容
    
    with open(f'{csvname}.csv', 'a', encoding='gbk', newline='') as f:
        #a = csv.writer(f)
        print(jp.Barrage_data)
        for item in jp.Barrage_data:
            print(item)                
            #a.writerow(item)
            f.write(item + '\n')
                    
        print('-------------弹幕获取完毕！-------------')

if __name__ == '__main__':
    #targeturl=input("请输入你要爬取评论的url(网址):-->")
    print('\n================B站数据爬取程序启动================\n')
    flag=int(input("输入-1-爬取B站评论  &  输入-2-爬取B站弹幕\n"))
    if flag == 1:                                  
        print('\n================开始爬取B站评论================\n')
        JP = JsonProcess()
        getReplies(JP, 1)
        print('\n================存储完成================\n')
    elif flag == 2:
        print('\n================开始爬取B站弹幕================\n')
        JP = JsonProcess()
        getBarrage(JP)
        print('\n================存储完成================\n')
    else :
        print('\n================输入有误================\n')