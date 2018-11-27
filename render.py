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
images = json.loads(open('images.json', 'r').read())


if os.path.exists('.image.json'):
    with open('.image.json', 'r') as f:
        image_map = json.loads(f.read())
else:
    image_map = {}


def get_image(_id):
    global image_map
    if _id in image_map:
        return image_map[_id]
    else:
        image = random.choice(images)
        image_map[_id] = image
        return image

dirs = [
    ('花间集', '赵崇祚'),
    ('南唐二主词', '李煜 李璟'),
    ('唐诗三百首', '蘅塘退士'),
    ('宋词三百首', ''),
    ('教科书选诗', '教科书出版社\n包含人民教育出版社、江苏教育出版社等'),
    ('古诗十九首', '无名氏'),
]

paths = []

for n, a in dirs:
    pfiles  = os.listdir(u'./data/%s/' % n)

    for pfile in pfiles:
        if 'json' not in pfile:
            continue

        if 'author' in pfile:
            continue

        path = os.path.join(u'./data/%s/' % n, pfile)
        juan = pfile.split('.')[1]
        paths.append((n, path, juan))
        

books = defaultdict(list)

for book, path, juan in paths:

    books[(book, dict(dirs)[book])].append(juan)

    with open(path, 'r') as f:
        content = f.read()

    poetrys = json.loads(content)
    for poetry in poetrys:
        notes = []

        poetry["id"] = str(hash(juan + poetry["title"])).replace('-','')
        
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

        root = '../../'
        image = get_image(poetry["id"])
        template = template_env.get_template(WORD_TEMPLATE_FILE)
        output = template.render(poetry=poetry, juan=juan, image=image, root=root)
        
        html_filename = 'www/poetrys/%s.html' % poetry["id"]
        
        with open(html_filename, 'w') as f:
             f.write(output)

    
    root = '../../'
    image = get_image(juan)
    template = template_env.get_template('list.html')
    output = template.render(poetrys=poetrys, juan=juan, image=image, root=root, book=book)
    with open('www/list/%s.html' % juan, 'w') as f:
        f.write(output)

for book, juans in books.items():
    root = '../'        
    image = get_image(str(hash(book[0])).replace('-', ''))
    template = template_env.get_template('book.html')
    output = template.render(book=book, juans=juans, image=image, root=root)
            
    with open('www/%s.html' % book[0], 'w') as f:
        f.write(output)
        
root = './'
image = get_image('index')
template = template_env.get_template('index.html')
output = template.render(books=books, image=image, author="", root=root)
with open('index.html' ,'w') as f:
    f.write(output)
        

with open('.image.json', 'w') as f:
    f.write(json.dumps(image_map, indent=2, ensure_ascii=False))
    
