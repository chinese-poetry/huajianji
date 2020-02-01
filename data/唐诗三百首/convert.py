# -*- coding: utf-8 -*-
import json, sys, re

reload(sys)

sys.setdefaultencoding('utf-8')


#string = 'abe(ac)ad)'
p1 = re.compile(r'[(](.*?)[)]', re.S)  #最小匹配
# p2 = re.compile(r'[(](.*)[)]', re.S)   #贪婪匹配

with open(sys.argv[1], 'r') as f:
    content = f.read()


data = json.loads(content)


ALL = []

for poetry in data:
    notes = []
    paras = []
    for p in poetry["paragraphs"]:
        mathed = re.findall(p1, p)

        p = re.sub(p1, '', p)
        paras.append(p)

        for m in mathed:
            if u'；' in m:
                mathed.append(m.split(u'；')[0])
                mathed.append(m.split(u'；')[1])
                continue

            if u'一作' in m:
                left, right = m.split(u'一作')
                notes.append("%s--一作 %s" % (left.strip(), right.strip()))
            elif u'通' in m:
                left, right = m.split(u'通')
                notes.append("%s--通 %s" % (left.strip(), right.strip()))
            else:
                pass
                #print m
                
    poetry["notes"] = notes
    poetry["paragraphs"] = paras

    ALL.append(poetry)


with open('out.json', 'w') as f:
    f.write(json.dumps(ALL, indent=2, ensure_ascii=False))

    #for i in notes:
    #    print i
    


