#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File: dict2class.py
@Date: 2023/04/23 17:05:09
@Version: 1.0
@Description: None
'''

import datetime
import time

class Dict2Class:
    @classmethod
    def __static_ctor__(cls):
        cls.LF = '\n'
        cls.imports = '''import datetime
'''
        cls.def_code_template = '''class UserDefined{timestamp}():
    def __init__(self, {params_split_with_comma}) -> None:
{assignments_split_with_lf}
    
    def __str__(self) -> str:
        return f"UserDefined{timestamp}({values_split_with_comma})"
'''
        cls.init_code_template = '''__ret__ = UserDefined{timestamp}({values_split_with_comma})
'''


    def __init__(self) -> None:
        self.def_codes = []


    def convert(self, obj: dict, recursive: bool=False):
        params = []
        values = []
        assignments = []
        for key in obj.keys():
            params.append(key)
            if type(obj[key]) is int or type(obj[key]) is float or type(obj[key]) is bool or type(obj[key]) is complex:
                values.append(str(obj[key]))
            elif type(obj[key]) is str:
                values.append(f"'{obj[key]}'")
            elif type(obj[key]) is tuple or type(obj[key]) is list or type(obj[key]) is set or type(obj[key]) is dict:
                if not recursive:
                    values.append(str(obj[key]))
                else:
                    if type(obj[key]) is dict:
                        ud = self.convert(obj[key])
                        values.append(str(ud))
                    elif type(obj[key]) is list:
                        new_list = []
                        for it in obj[key]:
                            if type(it) is dict:
                                it_ud = self.convert(it)
                                new_list.append(str(it_ud))
                            else:
                                new_list.append(it)
                        values.append(str(new_list).replace('"', ''))
                    elif type(obj[key]) is tuple:
                        new_tpl = ()
                        for it in obj[key]:
                            if type(it) is dict:
                                it_ud = self.convert(it)
                                new_tpl += (str(it_ud),)
                            else:
                                new_tpl += (it,)
                        values.append(str(new_tpl).replace('"', ''))
                    else:
                        values.append(str(obj[key]))
            elif type(obj[key]) is datetime.datetime:
                dt = f"datetime.datetime({obj[key].year}, {obj[key].month}, {obj[key].day}, {obj[key].hour}, {obj[key].minute}, {obj[key].second}, {obj[key].microsecond})"
                values.append(dt)
            elif type(obj[key]) == type(None):
                values.append('None')
            else:
                raise NotImplementedError('The current type is unsupported.')
            assignments.append(f"        self.{key} = {key}")
        timestamp = str(round(time.time() * 1000))
        def_code = Dict2Class.def_code_template.format(
            timestamp=timestamp,
            params_split_with_comma=','.join(params),
            assignments_split_with_lf='\n'.join(assignments),
            values_split_with_comma=','.join(values))
        self.def_codes.append(def_code)
        def_code_text = '\n'.join(self.def_codes)
        
        init_code_text = Dict2Class.init_code_template.format(
            timestamp=timestamp,
            values_split_with_comma=','.join(values))
        
        local_param = { '__ret__': None }
        exec('\n'.join([Dict2Class.imports, def_code_text, init_code_text]), {}, local_param)
        
        return local_param['__ret__']


Dict2Class.__static_ctor__()
