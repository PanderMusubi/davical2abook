#!/usr/bin/env python3

# Description: DAViCal CardDAV to SquirrelMail address book (.abook) converter
# License: GPL, following the license of DAViCal
# Author: Pander Musubi <pander@users.sourceforge.net>

import psycopg2
import re
from sys import argv, stderr

if len(argv) != 2:
    stderr.write('Missing required argument DAViCal username\n')
    exit(1)
username = argv[1]
if not re.match("^[A-Za-z0-9_-]*$", username):
    stderr.write('Username contains illegal characters\n')

conn = psycopg2.connect('dbname=davical user=davical_dba')
cur = conn.cursor()
cur.execute('select addressbook_resource.n, addressbook_address_email.type, '
            'addressbook_address_email.email, addressbook_address_tel.type, '
            'addressbook_address_tel.tel, caldav_data.dav_id from '
            'addressbook_address_tel left '
            'join addressbook_address_email on '
            'addressbook_address_tel.dav_id = '
            'addressbook_address_email.dav_id left join addressbook_resource '
            'on addressbook_resource.dav_id = '
            'addressbook_address_email.dav_id left join caldav_data on '
            'caldav_data.dav_id = addressbook_resource.dav_id left join usr '
            'on usr.user_no = caldav_data.user_no where usr.username = %s;',
            (username, ))

data = {}
for i in cur:
    name = i[0].split(';')
    last = name[0].strip()
    first = name[1].strip()

    nick = first.replace(' ', '').replace('-', '') + last.replace(' ', '').replace('-', '')
    emailtype = i[1].strip().upper()
    if 'HOME' in emailtype:
        nick += ':H'
    elif 'WORK' in emailtype:
        nick += ':W'
    else:
        stderr.write(
            'Unknown email type {0} for {1}\n'.format(emailtype, nick))

    email = i[2].strip().lower()

    teltype = i[3].strip().upper()
    tel = '+' + i[4].strip()
    tel = tel.replace(' ', '')
    tel = tel.replace('+', '')
    if 'CELL' in teltype:
        tel = 'M:' + tel
    elif 'HOME' in teltype:
        tel = 'H:' + tel
    elif 'WORK' in teltype:
        tel = 'W:' + tel
    else:
        stderr.write(
            'Unknown telephone type {0} for {1}\n'.format(teltype, nick))

    key = i[5] # id
    if key not in data:
        data[key] = '{}|{}|{}|{}|{}'.format(nick, first, last, email, tel)
    else:
        data[key] = '{} {}'.format(data[key], tel)

cur.execute('select addressbook_resource.n, addressbook_address_tel.type, '
            'addressbook_address_tel.tel, caldav_data.dav_id from '
            'addressbook_address_tel left '
            'join addressbook_resource '
            'on addressbook_resource.dav_id = '
            'addressbook_address_tel.dav_id left join caldav_data on '
            'caldav_data.dav_id = addressbook_resource.dav_id left join usr '
            'on usr.user_no = caldav_data.user_no where usr.username = %s;',
            (username, ))

# without email
tels = {}
for i in cur:
    name = i[0].split(';')
    last = name[0].strip()
    first = ''
    if len(name) > 1:
        first = name[1].strip()

    nick = first.replace(' ', '').replace('-', '') + last.replace(' ', '').replace('-', '')

    teltype = i[1].strip().upper()
    tel = '+' + i[2].strip()
    tel = tel.replace(' ', '')
    tel = tel.replace('+', '')
    if 'CELL' in teltype:
        tel = 'M:' + tel
    elif 'HOME' in teltype:
        tel = 'H:' + tel
    elif 'WORK' in teltype:
        tel = 'W:' + tel
    else:
        stderr.write(
            'Unknown telephone type {0} for {1}\n'.format(teltype, nick))

    key = i[3] # id
    if key not in data:
        if key not in tels:
            tels[key] = '{}|{}|{}|{}|{}'.format(nick, first, last, 'd@um.my', tel)
        else:
            tels[key] = '{} {}'.format(tels[key], tel)

cur.close()
conn.close()

data.update(tels)

# sort on id, newest entries at top
for key in sorted(data.keys(), reverse=True):
    print(data[key])
