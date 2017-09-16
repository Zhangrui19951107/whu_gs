# coding=utf-8
'''
使用临时文件
增加缓存
'''
import redis
import os
import tempfile
import marshal
#str to float
def to_float(x):
    return float(x)

#UTF-8 to unicode
def to_unicode(x):
    x=x.decode('UTF-8')
    return x


        
    #得到curpath路径
#     _curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
#     print _curpath


    
#数据初始化
def init_main():
#     cache_file=r"cache_file"
    cache_file = "/dev/shm/jb.cache"
    #print cache_file
#     print cache_file
    #需要读redis
    if not os.path.exists(cache_file):
        #10.95.130.184
        r = redis.Redis(host='192.168.2.132', port=6379, db=0)  # 如果设置了密码，就加上password=密码
        all_dic={}
        #传进来是utf-8 要转为unicode
        keys = r.keys()
        keys=map(to_unicode,keys)
        #转为float
        vals = r.mget(keys)
        vals=map(to_float,vals)
        kv = zip(keys, vals)
        for key,value in kv:
            all_dic[key]=value
        #序列化写入
        marshal.dump((all_dic,keys,vals),open(cache_file,'wb'))
        return all_dic,keys,vals
    else:
        all_dic,keys,vals = marshal.load(open(cache_file,'rb'))
#         print keys
#         print len(keys)
        return all_dic,keys,vals
        

#根据key生成 trie_tree
def init_tire(keys):
    trie_tree = {}
    for word in keys:
        p = trie_tree
        for single in word:
            if single not in p:
                p[single] ={}
            p = p[single]
        p['']='' #ending flag
    return trie_tree
    
    

def get_DAG(sentence):
    N = len(sentence)
    i,j=0,0
    #得到分词
    p = trie
    #返回的数据结构为key value 形式  {0: [0], 1: [1, 2, 3]}
    #key为下标 value为能和key下标组成词语的下标
    DAG = {}
    while i<N:
        c = sentence[j]
        if c in p:
            p = p[c]
            if '' in p:
                #如果第i个下标在DAG中没出现 则添加
                if i not in DAG:
                    DAG[i]=[]
                #如果出现就把能和下标组成词语的j加入
                DAG[i].append(j)               
            j+=1
            #如果j越界但是i可能还没有走到最后一个词 则重置i=i+1,j
            if j>=N:
                i+=1
                j=i
                p=trie
        #下一个词不在 p的子树里面 把p重新设置为根节点
        else:
            p = trie
            #i每次走一步
            i+=1
            j=i
    return DAG


def cut_all(sentence):
    dag = get_DAG(sentence)
    old_j = -1
    #k 为key表示下标 L为value 是能组成词的下标集合
    for k,L in dag.iteritems():
        #一个字的情况
        if len(L)==1 and k>old_j:
            yield sentence[k:L[0]+1]  #注释掉可以输出长度大于二的需要的词
            old_j = L[0]
        #多个字的情况
        else:
            for j in L:
                if j>k:
                    yield sentence[k:j+1]
                    old_j = j


#编码转换 把传进来的句子转成unicode
def bianma(sentence): 
    if not isinstance(sentence, unicode):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk','ignore')  
    return sentence
    
#给文章打总分
def get_grade():
    sum_score=grade_title()+grade_text()
#     print sum_score
    return sum_score
    
    
#给标题打分
def grade_title():
    title_score=0
    for i in cut_all(title):
        title_score=all_dic[i]+title_score  
    return title_score

def grade_text():
    text_len=len(text)
    text_score=0
    world_num=0
    for i in cut_all(text):
        text_score=all_dic[i]+text_score
        world_num=world_num+1
    text_score=text_score*(float(500*world_num)/text_len)**0.5
    return text_score
    


def mm(title1,text1):
    #编码转换 
    global title
    global text 
    global all_dic
    global keys
    global vals
    title=bianma(title1)
    text=bianma(text1)
    #设为全局变量很多地方要用到
    global trie
    #初始化 完成  all_dic 总词典  keys  vals 顺序是对应的
    all_dic,keys,vals=init_main()
#    初始化 trie
    trie=init_tire(keys)
    sum_score=get_grade()
    return sum_score

