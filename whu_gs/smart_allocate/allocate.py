# min(max) edition
# coding=utf-8
'''
@author：Zetary-L
@introduction：a function to allocate netspeed
'''
import string
from datetime import *
import time
import datetime
from site import *
from math import *


def allocate(sitelist, interval, U):
    n = len(sitelist)
    list_inuse = []
    list_else = []
    for i in range(n):
        sitelist[i].v = 0
        if(sitelist[i].inuse==1):
            list_inuse.append(sitelist[i])
        else:
            sitelist[i].v=0
            list_else.append(sitelist[i])
    n = len(list_inuse)
    #allocate
    sum_weight = 0.0
    for i in range(n):
        sum_weight += list_inuse[i].weight
    list_inuse.sort(key=lambda site: site.limit)
    U_remain = U
    for i in range(n):
        if list_inuse[i].limit == 0:
            continue
        else:
            if sum_weight > U_remain * list_inuse[i].limit:
                list_inuse[i].v = list_inuse[i].weight / list_inuse[i].limit
                U_remain -= list_inuse[i].v
                sum_weight -= list_inuse[i].weight
            else:
                break
    for i in range(n):
        if list_inuse[i].v == 0:
            list_inuse[i].v = U_remain * list_inuse[i].weight / sum_weight
    for i in range(n):
        list_inuse[i].v = int(ceil(list_inuse[i].v))
    sitelist = list_inuse + list_else
    return sitelist
