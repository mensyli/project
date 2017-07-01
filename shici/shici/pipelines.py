# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
import pymysql
import sqlite3
from pymongo import MongoClient

class ShiciPipeline(object):
    def process_item(self, item, spider):

        print('TXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXTTXT')
        basedir = 'F:/Images/temp/shici/'
        dynast_name = item['dynast']
        shier_name = item['author']
        shi_name = item['title']
        shici_content = item['body']
        shici_shangxi = item['shangxi']
        path = basedir + dynast_name + '/' + shier_name + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        i = 1
        while True:
            if os.path.exists(path + shi_name + '.txt'):
                if '_' in shi_name:
                    shi_name = re.sub(r'_\d+','',shi_name)
                shi_name = shi_name + '_' + str(i)
                i += 1
            else:
                break
        with open(path + shi_name + '.txt','a') as f:
            f.write('朝代:' + dynast_name + '\n')
            f.write('作者:' + shier_name + '\n')
            f.write('诗名:' + shi_name + '\n\n\n')
            for line in shici_content:
                f.write(line.strip() + '\n')
            for line in shici_shangxi:
                f.write(line.strip() + '\n')
            f.write('\n\n')
        return item


class Data2MysqlPipeline(object):


    def precess_item(self,item,spider):

        print('MYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQLMYSQL')
        dynast_name = item['dynast']
        shier_name = item['author']
        shi_name = item['title']
        shici_content = item['body']
        shici_shangxi = item['shangxi']

        connection =pymysql.connect(
            host='localhost',
            port=3306,
            user='mensyli',
            password='xiaoming98',
            db='shiciDB',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)


        try:
            with connection.cursor() as cursor:
                sql = '''
                    INSERT INTO SHICI(dynast,author,title,body,shangxi)
                        VALUES (%s,%s,%s,%s,%s)
                '''
                cursor.execute(sql,(dynast_name,shier_name,shi_name,shici_content,shici_shangxi))
            connection.commit()

        finally:
            connection.close()

        return item


class Data2SqlitePipeline(object):

    def precess_item(self,item,spider):

        print('SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3SQLITE3')
        dynast_name = item['dynast']
        shier_name = item['author']
        shi_name = item['title']
        shici_content = item['body']
        shici_shangxi = item['shangxi']

        connection = sqlite3.connect('F:/Images/temp/sqlite3/db/shici.db')

        try:
            with connection.cursor() as cursor:
                sql = '''
                    create table if not exists shici(
                        id int auto_increment primary key,
                        dynast varchar(50) null,
                        author varchar(200) null,
                        title varchar(300) null,
                        body text null,
                        shangxi text null,
                        constraint shici_id_uindex unique (id)
                        );
                '''
                cursor.execute(sql)

                sql2 = '''
                    INSERT INTO shici(dynast,author,title,body,shangxi)
                        VALUES (%s,%s,%s,%s,%s)
                '''
                cursor.execute(sql,(dynast_name,shier_name,shi_name,shici_content,shici_shangxi))
            connection.commit()
        
        finally:
            connection.close()

        return item



class Data2MongoDBPipeline(object):
    def precess_item(self,item,spider):

        print('MONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODBMONGODB')
        dynast_name = item['dynast']
        shier_name = item['author']
        shi_name = item['title']
        shici_content = item['body']
        shici_shangxi = item['shangxi']

        conn = MongoClient('27.0.0.1', 27017)

        db = conn.shicidb

        my_set = db.shici_set

        my_set.insert(item) 

        return item


