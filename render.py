# -*- coding: utf-8 -*-
import jinja2
import random
import os, json
import sys
from uuid import uuid4
from os.path import splitext
from collections import defaultdict
from datetime import datetime
#from pagination import Pagination

version = uuid4().hex

reload(sys)
sys.setdefaultencoding('utf-8')

template_loader = jinja2.FileSystemLoader(searchpath="templates")
template_env = jinja2.Environment(loader=template_loader)
WORD_TEMPLATE_FILE = "detail.html"


pfiles  = os.listdir(u'./data/花间集/')
images = os.listdir(u'./images/')
juans = []

for pfile in pfiles:
    if 'json' not in pfile:
        continue

    juan = pfile.split('.')[1]
    juans.append(juan)
    path = os.path.join('./data/花间集/', pfile)

    with open(path, 'r') as f:
        content = f.read()

    poetrys = json.loads(content)
    for poetry in poetrys:
        notes = []

        poetry["id"] = str(hash(poetry["title"])).replace('-','')
        
        for note in poetry["notes"]:
            if '--' in note:
                left, right = note.split('--')
            elif '-' in note:
                left, right = note.split('-')
            else:
                left, right = '1', right

            first = left[0]
            if first.isdigit():
                left = left.replace(first, '').replace('.', '')
        
            first = right[0]
            if first.isdigit():
                right  = right.replace(first, '').replace('.', '')
            notes.append((left, right))
        
        poetry["notes"] = notes

        image = random.choice(images)
        
        template = template_env.get_template(WORD_TEMPLATE_FILE)
        output = template.render(poetry=poetry, juan=juan, image=image)
        
        html_filename = 'www/poetrys/%s.html' % poetry["id"]
        
        with open(html_filename, 'w') as f:
             f.write(output)

    
    image = random.choice(images)
    template = template_env.get_template('list.html')
    output = template.render(poetrys=poetrys, juan=juan, image=image)
    with open('www/list/%s.html' % juan, 'w') as f:
        f.write(output)

        


image = random.choice(images)
template = template_env.get_template('index.html')
output = template.render(juans=juans, image=image, author="赵崇祚")
        
with open('index.html', 'w') as f:
    f.write(output)
        
