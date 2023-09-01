#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   dbmodule.py
@Time    :   2023/08/16 09:42:54
Python Version:  3.10
@Version :   1.0
@Desc    :   
数据驱动层, 也叫DAO层,是用于封装对数据库的访问。
在Python中,我们可以创建一个通用的数据驱动层接口,然后分别为MongoDB,MySQL和Oracle,Redis实现这个接口。
SQLAlchemy 主要用于关系型数据库，并且不直接支持 MongoDB 和 Redis,所以对于这两种类型的数据库我们需要单独处理。
'''

# import logging
# from sqlalchemy.ext.declarative import declarative_base

import hashlib

def orm_update_or_insert(session, data, filtkeys, table, update=False, updatekeys=None):
    """
    基于orm更新/插入数据
    :param session: sessionmaker(),
    :param data: dict/series,
    :param filtkeys: list, 键名, 用于筛选数据
    :param table:
    :param update: bool, 是否update数据
    :param updatekeys: list, 键名, 用于update数据
    example: 
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        conn = create_engine(settings.DSN)
        sessmaker = sessionmaker(conn)
        sess = sessmaker()
        for eh, ehrow in df.iterrows():
            ehrow = ehrow.dropna()  # 删除nan值
            ehdict = ehrow.to_dict()
            update_keys = list(set(ehdict.keys()) - set(primary_keys))
            dbmodule.orm_update_or_insert(sess, ehdict, primary_keys, tables.JztReportidea,
                                            update=True, updatekeys=update_keys)
        sessmaker.close_all()
    """
    filt_dict = dict()
    for ehfkey in filtkeys:
        filt_dict[ehfkey] = data[ehfkey]
    res_filted = session.query(table).filter_by(**filt_dict).all()
    # print(len(res_filted))
    # update
    if len(res_filted) > 0:
        if (update is True) and isinstance(updatekeys, list):
            for ehrf in res_filted:
                for ehukey in updatekeys:
                    # print(ehukey, data[ehukey])
                    if hasattr(ehrf, ehukey):
                        setattr(ehrf, ehukey, data[ehukey])
                session.commit()
    # insert
    elif len(res_filted) <= 0:
        data_insert = table(**data)
        session.add(data_insert)
        session.commit()


def update_or_insert(session, data, filtkeys, tbn, update=False, updatekeys=None):
    """
    基于sql语句更新/插入数据
    :param session: sessionmaker(),
    :param data: dict/series,
    :param filtkeys: list, 键名, 用于筛选数据
    :param tbn: str, table name
    :param update: bool, 是否update数据
    :param updatekeys: list, 键名, 用于update数据
    """
    filt_dict = dict()
    for ehfkey in filtkeys:
        filt_dict[ehfkey] = data[ehfkey]
    filt_str = ['`%s`="%s"' % (x, filt_dict[x]) for x in filt_dict.keys()]
    filt_str = ' AND '.join(filt_str)
    sql = 'SELECT * FROM `%s` WHERE %s' % (tbn, filt_str)
    print(sql)
    res = session.execute(sql)
    if res.rowcount > 0:
        if update is True:
            update_str = ['`%s`="%s"' % (x, data[x]) for x in updatekeys]
            update_str = ', '.join(update_str)
            sql = 'UPDATE `%s` SET %s WHERE %s' % (tbn, update_str, filt_str)
        else:
            return None
    else:
        sql = 'INSERT INTO `%s` (`%s`) VALUES (%s)' % \
              (tbn, '`, `'.join(list(data.keys())), ', '.join(['"%s"' % data[x] for x in data.keys()]))
    print(sql)
    session.execute(sql)
    session.commit()


def replace_c(session, data, filtkeys, tbn, update=False, updatekeys=None):
    """
    改版 update_or_insert 省去 第一步查询
    基于sql语句更新/插入数据
    :param session: sessionmaker(),
    :param data: dict/series,
    :param filtkeys: list, 键名, 用于筛选数据
    :param tbn: str, table name
    :param update: bool, 是否update数据
    :param updatekeys: list, 键名, 用于update数据
    """
    sql = 'REPLACE INTO `%s` (`%s`) VALUES (%s)' % \
          (tbn, '`, `'.join(list(data.keys())), ', '.join(['"%s"' % data[x] for x in data.keys()]))
    # if update is True:
    #     filt_dict = dict()
    #     for ehfkey in filtkeys:
    #         filt_dict[ehfkey] = data[ehfkey]
    #     filt_str = ['`%s`="%s"' % (x, filt_dict[x]) for x in filt_dict.keys()]
    #     filt_str = ' AND '.join(filt_str)
    #     update_str = ['`%s`="%s"' % (x, data[x]) for x in updatekeys]
    #     update_str = ', '.join(update_str)
    #     sql = 'UPDATE `%s` SET %s WHERE %s' % (tbn, update_str, filt_str)
    # else :
    #     sql = 'REPLACE INTO `%s` (`%s`) VALUES (%s)' % \
    #           (tbn, '`, `'.join(list(data.keys())), ', '.join(['"%s"' % data[x] for x in data.keys()]))
    #print(sql)
    session.execute(sql)
    session.commit()


def read_sql(filepath=None):
    # 读取 sql 文件文本内容
    sql = open(filepath, 'r', encoding='utf8')
    sqltxt = sql.readlines()
    # 此时 sqltxt 为 list 类型
    # 读取之后关闭文件
    sql.close()
    # list 转 str
    sql = "".join(sqltxt)
    return sql
    # print(sql)


from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete,and_, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback
# SQLAlchemy for MySQL and Oracle
class SQLDatabase(object):
    def __init__(self, db_string):
        """
        Description:
            SQLDatabase init 
        Args:
            db_string (str): db_string
        Returns:
            None
        Example:
        Raises:
            Exception: error
        """
        try:
            self.engine = create_engine(url = db_string)
            self.metadata = MetaData()
            # self.connection = self.engine.connect()
            ### Please refer to session.close_all_sessions()
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            print(f"Failed to connect to database with error: {e}")
            print(traceback.format_exc())
    def get_table_field_comment(self, table_name):
        """
        Description:
            get table field comment
        Args:
            table_name (str): The first integer to add.
        Returns:
            int: 
        Example:
            >>> 
        Raises:
            Exception: error
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        return table.comment
    
    def _table_exists(self, table_name):
        return inspect(self.engine).has_table(table_name=table_name)
        # return self.engine.dialect.has_table(connection=self.engine,table_name=table_name)
        
    def create_table(self, table_name=None, columns=None, declarative_base_table=None):
        """
        Description:
            create first table name 
        Args:
            table_name (str): The first integer to add.
            columns (Column): Column('id', Integer, primary_key=True)
        Returns:
            int: The sum of a and b.
        Example:
            >>> columns = [
                    Column('id', Integer, primary_key=True),
                    Column('name', String(255)),
                    Column('age', Integer)
                    ]
            >>> create_table(table_name="test",columns=columns)
        Raises:
            Exception: error
        """
        try:
            if not self._table_exists(table_name=table_name):
                print('Table"{}" not exists'.format(table_name))
                declarative_base_table.metadata.create_all(self.engine) if declarative_base_table else Table(
                        table_name, 
                        self.metadata,
                        *columns
                    ).metadata.create_all(bind=self.engine)
            else:
                print('Table"{}" exists'.format(table_name))
        except SQLAlchemyError as e:
            print("Error occurred during Table creation!")
            print(str(e))
            return False
        else:
            return True

    def fetch(self, table_name,filt_dict=None):
        """
        Description:
            sql fetch table  in filt_dict 
        Args:
            table_name (str): table name 
            filt_dict (dict): filt dict
        Returns:
            fetchall
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        if filt_dict :
            conditions = [table.c[key] == value for key, value in filt_dict.items()]
            query = select(table).where(and_(*conditions))
        else: 
            query = select(table)
        result = self.session.execute(query)
        return result.fetchall()
    def insert_data(self, table_name, data_dict):
        """
        Description:
            insert data with table name in dict
        Args:
            table_name (str): table name 
            data_dict (dict): data dict  {"A":123}
        Returns:
            bool
        Example:

        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            stmt = insert(table).values(data_dict)
            # self.connection.execute(stmt)
            # self.connection.commit()
            self.session.execute(stmt)
        except IntegrityError as e :
            print(e.args[0] + " pass !!")
        except SQLAlchemyError as e:
            self.session.rollback()
            print("Error occurred during record insertion!")
            print(str(e))
        else:
            self.session.commit()
            return True
    def update_data(self, table_name, condition_dict, new_data_dict):
        """
        Description:
            update data in table name condition_dict with new_data_dict
        Args:
            table_name (str): table name
            condition_dict (dict): condition dict
            new_data_dict (dict): new data dict
        Returns:
            bool
        Example:
            >>> add(1, 2)
            3
        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            where_clause = and_(*[table.columns[key] == value for key, value in condition_dict.items()])
            stmt = update(table).where(where_clause).values(new_data_dict)
            self.session.execute(stmt)
            # self.connection.execute(stmt)
            # self.connection.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print("Error occurred during record update!")
            print(str(e))
            return False
        else:
            self.session.commit()
            return True
    def delete_data(self, table_name, condition_dict):
        """
        Description:
            delete data with table name in condition dict
        Args:
            table_name (str): table name
            condition_dict (dict): condition dict
        Returns:
            bool 
        Example:
            >>> 
        Raises:
            Exception: error
        """
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            where_clause = and_(*[table.columns[key] == value for key, value in condition_dict.items()])
            stmt = delete(table).where(where_clause)
            self.session.execute(stmt)
            # self.connection.execute(stmt)
            # self.connection.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print("Error occurred during record deletion!")
            print(str(e))
            return False
        else:
            self.session.commit()
            return True
    def close(self):
        try:
            self.session.close()
            self.engine.dispose() # Dispose the engine
            return True
        except Exception as e:
            print("Error occurred while closing the connection!")
            print(str(e))
            return False

from pymongo import MongoClient, errors as mongo_errors

# ###  PyMongo for MongoDB
class MongoDB:
    def __init__(self, connection_string, db_name):
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[db_name]
        except mongo_errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB with error: {e}")
            print(traceback.format_exc())
    def fetch(self, collection_name, query={}):
        collection = self.db[collection_name]
        return collection.find(query)
    def insert_data(self, collection_name, data):
        collection = self.db[collection_name]
        collection.insert_one(data)
    def update_data(self, collection_name, condition, new_data):
        collection = self.db[collection_name]
        collection.update_one(condition, {"$set": new_data})
    def delete_data(self, collection_name, condition):
        collection = self.db[collection_name]
        collection.delete_one(condition)
# Redis-Py for Redis
import redis
class RedisDB:
    def __init__(self, host, port):
        try:
            self.db = redis.Redis(host=host, port=port)
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis with error: {e}")
            print(traceback.format_exc())
    def fetch(self, name):
        return self.db.get(name)
    def insert_data(self, name, value):
        self.db.set(name, value)
    def update_data(self, name, value):
        self.insert_data(name, value)
    def delete_data(self, key):
        self.db.delete(key)