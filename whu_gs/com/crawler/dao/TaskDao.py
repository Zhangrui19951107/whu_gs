#coding=UTF-8
'''
Created on 2015年7月26日

@author: 龚兵
@说明: 任务表数据库操作
'''
from com.crawler.models.TaskModel import Tb_Task
from com.crawler.utils.BaseDB import BaseDB

class TaskDaoImp(BaseDB):
    '''
    classdocs
    '''
    
    '''
                保存任务
    '''
    def saveTask(self,Tb_Task):
        
        conn = self.getConn();
        cur = conn.cursor()
        sql = "insert into tb_task(id,classify_id,url,priority,status) values(%s,%s,%s,%s,%s)"
        

        cur.execute(sql, (Tb_Task.id,Tb_Task.classify_id,Tb_Task.url,Tb_Task.priority,Tb_Task.status));
        
        conn.commit()
        cur.close()
        conn.close()
        
    
    '''
                保存列表任务到数据库
    ''' 
    def saveTaskList(self,list):
        
        conn = self.getConn();
        cur = conn.cursor()
        sql = "insert into tb_task(id,classify_id,url,urlType,priority,status) values(%s,%s,%s,%s,%s,%s)"
        
        if len(list) > 0 :
            cur.executemany(sql, list);
        
        conn.commit()
        cur.close()
        conn.close()
    
    
    '''
        通过任务id，修改任务状态
    '''
    def updateTaskStatusById(self,id,status):
        
        conn = self.getConn();
        cur = conn.cursor()
        sql = "update  tb_task set status = %s where id = %s"
        
        cur.execute(sql, (status,id));
        
        conn.commit()
        cur.close()
        conn.close()


    '''
            通过分类id和任务状态，获取指定任务
    '''
    def getTaskStatusByClassifyId(self,classifyid,status):
        
        conn = self.getConn();
        cur = conn.cursor()
        sql = "select * from tb_task where classify_id = %s and status = %s"
        
        cur.execute(sql, (classifyid,status));
        rows = cur.fetchall()      
        
        listBean=list()

        for row in rows:
            task=Tb_Task()
            task.id=row["id"]
            task.classify_id=row["classify_id"]
            task.url=row["url"]
            task.urlType=row["urlType"]
            task.priority=row["priority"]
            task.status=row["status"]
            listBean.append(task)
         
        cur.close()
        conn.close()   
        
        return listBean      
    
    
    '''
                获取url信息
    '''
    def getIsUrlByUrl(self,urlStr):
        conn = self.getConn()
        cur = conn.cursor()
#        sql = "select * from tb_task where url = %s"
        sql = "select * from tb_task where url = '"+urlStr+"'"
        cur.execute(sql)
        rows = cur.fetchone()
          
        if rows== None : return False
        else : return True
        #print rows
        
        cur.close()
        conn.close()       
        
        
        
        