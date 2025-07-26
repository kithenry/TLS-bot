#!/usr/bin/env python3


import json



def read_generic(fname):
    with open(fname,'r') as f:
        return f.read()


def write_generic(fname, write_data):
    with open(fname, 'w') as f:
        [f.write(write_data) if write_data else print('nothing to write')]
        [print("Data written to ", fname) if write_data else '']


def read_json(fname, encoding=None):
    if not encoding:
        encoding = 'utf-8'
    with open(fname,mode='r',encoding=encoding) as read_file:
        read_data = json.load(read_file)
        return read_data

def write_csv():
    pass

def read_csv():
    pass


def write_excel():
    pass

def read_excel():
    pass


def write_json(fname, dump_data, encoding=None):
    if not encoding:
        encoding = 'utf-8'
    with open(fname, mode='w', encoding=encoding) as write_file:
        [json.dump(dump_data, write_file,indent=4,ensure_ascii=False) if dump_data else print('nothing to dump')]
        [print("Data written to: ", fname) if dump_data else '']

#def fio_main(fname, ftype, action, data, encoding=None):
#    if ftype == 'json':
#        if action == 'r':
#            return json_read(fname,encoding)
#        elif action == 'w':
#            return json_write(fname=fname,dump_data=data,encoding=encoding)
#    else:
#        if action == 'r':
#            return plain_read(fname)
#
#           return plain_write(fname,write_data=data)


# helpful articles
# -- Json
# 1. https://realpython.com/python-json/
