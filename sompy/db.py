#coding=utf-8
import MySQLdb
import sys, os
import numpy as np
import ConfigParser
from itertools import chain
from mysm import Mysm

abpath = os.path.abspath("conf.ini")
cf = ConfigParser.ConfigParser()
cf.read(abpath)

DADABASE = cf.get("sql_info","DATABASE")
USER = cf.get("sql_info","USER")
PASSWORD = cf.get("sql_info","PASSWORD")
HOST = cf.get("sql_info","HOST")
PORT = int(cf.get("sql_info","PORT"))
TABLE = cf.get("sql_info","TABLE")

select_sql = "SELECT id, cnt,appid FROM " + TABLE
count_sql = "SELECT count(*) FROM " + TABLE
test = None

def read_mysql():
    try:
        conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWORD,db=DADABASE,port=PORT)
        cursor = conn.cursor()
        cursor.execute(count_sql)
        count = 0
        #显示总数
        for row1 in cursor:
            count = row1[0];
            print(row1)
        
        test = np.arange(count*3).reshape(count,3)
        numrows = cursor.execute(select_sql)
        index = 0
        for row in cursor:
            print(row)
            test[index,] = np.fromiter(row, np.dtype(int,int),count=3)
            index = index+1
        
        conn.commit()
        cursor.close()
        conn.close()

    except MySQLdb.Error:
        e = sys.exc_info()[1]
        print "MySql Error %d:%s"%(e.args[0],e.args[1])
    
    return test

data = read_mysql()

names = ['id', 'cnt','appid']


if data is None :
    print("data is None")
else:
    som = Mysm(data=data,names=names)
    som.easytest()