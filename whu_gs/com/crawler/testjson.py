__author__ = 'bohaohan'
import json
f=open('cntongshan.json')
c = json.load(f)
print c['title']