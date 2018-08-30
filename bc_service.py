#!/usr/bin/env python
from properties import *
import requests
import json

'''
 Service to connect to the blockchain REST API
'''

def register_bc(id, balance=None):
    balance = balance or "0"
    data = {"name": id, "balance": balance}
    res = requests.post(REG_URL, json.dumps(data, ensure_ascii=False), headers=JSON_HEADER).json()
    return res


def add_thank(id, thank):
    res = requests.post(POST_THX_URL + str(id),
                        json.dumps(thank, ensure_ascii=False),
                        headers=JSON_HEADER,
                        timeout=300).json()
    return res


def get_thank(id):
    res = requests.get(GET_THX_URL + str(id), headers=JSON_HEADER).json()
    return res


def _example():
    thx = {"name": "JOHN",
           "type": "ta",
           "message": "thankssss"}
    #res = register_bc("001")
    #print(res)
    res = add_thank("001", thx)
    print(res)
    res = get_thank("001")
    print(res)


if __name__ == '__main__':
    _example()

