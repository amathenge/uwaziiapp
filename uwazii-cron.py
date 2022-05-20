#!/usr/bin/env python3
import sys
import json
import http.client
import urllib.parse
import sqlite3
from sqlite3 import Error
import urllib.parse
from datetime import datetime
import cred

'''
Uwazii Mobile is an SMS service.

This script manages the FAIR_ACRES Sender ID. The FAIR_ACRES Sender ID is a transactional ID which means that it can send messages at any time. The other type of Sender ID is a Promotional ID - which is limited in the time of day messages can be sent, limited in the length of messages, and also limited in the quantity (repetition) of messages that can be sent.
'''

now = datetime.now()
dnow = now.strftime('%Y-%m-%d')
tnow = now.strftime('%H:%M:%S')

try:
    conn = sqlite3.connect(cred.dbfile)
    conn.row_factory = sqlite3.Row
except Error as e:
    sys.exit(-1)
    
cur = conn.cursor()
sql = '''
    select id, uptime, EAT from log where id = (select max(id) from log)
'''
res = cur.execute(sql)
data = res.fetchone()
conn.close()

msg = 'Last uptime reading from Mac server:\n'
msg += 'when = date: {}, time: {}\n'.format(dnow, tnow)
msg += 'db record: {}\n'.format(data['EAT'])
msg += 'id: {} and message: {}'.format(data['id'], data['uptime'])

jsondata = {
    "SenderId": cred.SenderID,
    "Is_Unicode": False,
    "Is_Flash": False,
    "SchedTime": "",
    "GroupId": "",
    "ServiceId": "",
    "CoRelator": "",
    "LinkId": "",
    "MobileNumbers": cred.MobileNumbers,
    "Message": msg,
    "ApiKey": cred.ApiKey,
    "ClientId": cred.ClientId
}

jsondata = json.dumps(jsondata)

headers = {
    "content-type": "application/json",
    "cache-control": "no-cache"
}

conn = http.client.HTTPSConnection(cred.UwaziiAPIUrl)
conn.request("POST", cred.UwaziiAPIRequest, body=jsondata, headers=headers)
res = conn.getresponse()
data = res.read()
conn.close()

# print(data)
