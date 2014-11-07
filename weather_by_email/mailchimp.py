#!/usr/bin/python
from mailsnake import MailSnake
import json


opts = {'stream': True}
export = MailSnake('7726f9f014ed1511f11722f300bbbd43-us9', api='export', requests_opts=opts)
resp = export.list(id='1b1f1ee8be')

lines = 0
for list_member in resp():
    if lines > 0: # skip header row
        print list_member[0]
        print list_member[1]
        print list_member[2]

    lines += 1
    
