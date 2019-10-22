#encoding:utf-8--
import requests
import time
import re
import json
import os
from random import randint
import pandas as pd
GOODS_EXCEL_PATH = 'taobao_goods.xlsx'
class taobao():
    def __init__(self):
    #淘宝既需要用户的缓存数据，也需要用户代理识别
    #可以直接用chrome浏览器获取xpath
    #你要爬取的内容是在一个json脚本中,etree用不了的，和微博不同
        self.i=0#计数
        self.header={'cookie':''
                        ,'user-agent':''
    }
    def _save_excel(self,goodslist,filename):
        if os.path.exists(filename):#excel只能先读后写，不能追加
            df = pd.read_excel(filename)
            df = df.append(goodslist)
        else:
            df = pd.DataFrame(goodslist)

        writer = pd.ExcelWriter(filename)#重新写
        df.to_excel(excel_writer=writer, columns=['title', 'price', 'location', 'sales'], index=False,
                    encoding='utf-8', sheet_name='Sheet')
        writer.save()
        writer.close()
    def _get_goods_info(self, goods_str):#读取json的内容
        goods_json = json.loads(goods_str)
        goods_items = goods_json['mods']['itemlist']['data']['auctions']#方括号里面的标签不是并列的，而是层层递进
        goods_list = []
        #http://www.bejson.com/
        #也可以用VS code。
        #来剖析json文件
        for goods_item in goods_items:
            goods = {'title': goods_item['raw_title'],
                     'price': goods_item['view_price'],
                     'location': goods_item['item_loc'],
                     'sales': goods_item['view_sales']}
            self.i+=1
            goods_list.append(goods)
            print("("+str(self.i)+"):  "+str(goods))
        return goods_list
    def get_onePage(self,keyword,pagenum,filename):
        pagenum=44*pagenum
        url="https://s.taobao.com/search?q=%s&sort=sale-desc&s=%d"%(keyword,pagenum)
        html=requests.get(url,headers=self.header).text
        goods_match=re.search(r'g_page_config = (.*?)}};',html)#正则表达式提前json
        goods_str = goods_match.group(1) + '}}'#构建成完整的json
        goods_list = self._get_goods_info(goods_str)
        self._save_excel(goods_list,filename)
    def get_allPage(self,keyword,filename):
        for k in range(0,100):
            try:
                w=k+1
                print('第'+str(w)+'页')
                self.get_onePage(keyword,k,filename)
                time.sleep(randint(30,35))
            except:
                continue
d=taobao()
d.get_allPage('T恤','WholeTaobaoData.xlsx')
#前者是搜索的关键词，后者是保存的路径
#自行补充完整header