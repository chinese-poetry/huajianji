# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


import os, json

images = os.listdir(u'./images/')


datas = []

for i in images:
    if 'renrenxiaozhan' in i:
        link = "http://zhan.renren.com/chinastyle?checked=true"
        author = "人人小站"
        p = 1
    elif 'pola' in i:
        link = "http://www.polayoutu.com/collections"
        author = "泼辣有图"
        p = 1
    elif 'jackeygao' in i:
        link = "https://jackeygao.io"
        author = "JackeyGao"
        p = 1
    else:
        link = "#"
        author = "互联网"
        p = 1
        

    for _ in range(p):
        data = {
            "src": i,
            "link": link,
            "author": author
        }

        datas.append(data)


with open('config/images.json', 'w') as f:
    f.write(json.dumps(datas, indent=2, ensure_ascii=False))

