#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__version__ = 1.0
__init_date__ = '2023/09/01 09:14:17'
__maintainer__ = 'Guanjie Wang'
__update_date__ = '2023/09/01 09:14:17'

import os
import sqlite3

from alksqlite3.table import AlkSqllite3Table


class AlkSqlite3DB(object):
    
    def __init__(self, db_fp, table_name: str = None, columns_and_types: tuple = None):
        self._db_fp = db_fp
        self._db, self._nowtable = None, None
        self.inited = False
        self.connect_db()
        if (table_name is not None) and (columns_and_types is not None):
            self._table = AlkSqllite3Table(table_name=table_name, columns_and_types=columns_and_types)
        else:
            self._table = None
    
    @property
    def table(self):
        return self._table
    
    @table.setter
    def table(self, table: AlkSqllite3Table):
        self._table = table
    
    @property
    def table_name(self):
        return self.table.name
    
    def _view_alldb(self):
        _ = self._nowtable.execute("SELECT * FROM %s" % self.table_name)
        print(_.fetchall())
    
    def connect_db(self):
        self._db = sqlite3.connect(self._db_fp)
        self._nowtable = self._db.cursor()
    
    def init(self, force_init: bool = False):
        if force_init:
            self.rm_dbfile()
            self.connect_db()
        
        if not self.inited:
            if self._table is None:
                raise ValueError(
                    "Set table: self._table ="
                    " AlkSqllite3Table(table_name=table_name, columns_and_types=columns_and_types)")
            
            try:
                self._nowtable.execute("CREATE TABLE %s (%s)" % (self.table_name, self.table.query_str))
                self._db.commit()
                return True
            except sqlite3.OperationalError:
                return False
        return False
    
    def insert(self, *args):
        _data = self.table.add_data_sequence(*args)
        self._nowtable.execute("INSERT INTO %s VALUES (%s)" % (self.table_name, _data))
        self._db.commit()
    
    def update(self, condation: tuple, data: tuple):
        """
        condataion = (('tablename', '123'), ('ll', 'test'))
        data = ('num', 1)

        :param condation: 根据该条件在数据库中查询
        :param data: 将数据库中的data[0]对应的标签值更新为data[1]
        :return:
        """
        query_label = " AND ".join(["%s=?" % i[0] for i in condation])
        data_label = [self.table_name, data[0], query_label]
        query_value = [data[1]] + [i[1] for i in condation]
        self._nowtable.execute("UPDATE {0} SET {1}=? WHERE {2}".format(*data_label), query_value)
        self._db.commit()
    
    def query(self, condation: tuple):
        query_label = " AND ".join(["%s=?" % i[0] for i in condation])
        data_label = [self.table_name, query_label]
        query_value = [i[1] for i in condation]
        _d = self._nowtable.execute("SELECT * FROM {0} WHERE {1}".format(*data_label), query_value)
        return _d.fetchone()
    
    def rm_dbfile(self, no_remove=False):
        if not no_remove:
            os.remove(self._db_fp)
        pass

