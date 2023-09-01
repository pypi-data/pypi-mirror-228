#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__version__ = 1.0
__init_date__ = '2023/09/01 09:14:07'
__maintainer__ = 'Guanjie Wang'
__update_date__ = '2023/09/01 09:14:07'


class AlkSqllite3Table(object):
    
    def __init__(self, table_name, columns_and_types):
        self._table_name = table_name
        self._query_head_str = ', '.join(['%s %s' % (str(ks), str(kt)) for ks, kt in columns_and_types])
        self.columns = [ks for ks, _ in columns_and_types]
        self.cty = [kt for _, kt in columns_and_types]
    
    @property
    def name(self):
        return self._table_name
    
    @property
    def query_str(self):
        return self._query_head_str
    
    def add_data_sequence(self, *args):
        assert len(self.columns) == len(args)
        # return {self.columns[i]: args[i] for i in range(len(args))}
        _fd = []
        for i in range(len(args)):
            if self.cty[i] == 'text':
                _fd.append("'%s'" % args[i])
            elif self.cty[i] == 'real':
                _fd.append("%f" % args[i])
        return ', '.join(_fd)
    
    def add_data_dict(self, data_dict: dict):
        return [data_dict[i] for i in self.columns]

