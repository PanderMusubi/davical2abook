#!/usr/bin/env python3
'''Convert DAViCal CardDAV to SquirrelMail address book (.abook).'''

# License: GPL, following the license of DAViCal
# Author: Pander Musubi <pander@users.sourceforge.net>

import re
import sys
import psycopg2

if len(sys.argv) != 2:
    sys.stderr.write('Missing required argument DAViCal username\n')
    sys.exit(1)
username = sys.argv[1]
if not re.match("^[A-Za-z0-9_-]*$", username):
    sys.stderr.write('Username contains illegal characters\n')

conn = psycopg2.connect('dbname=davical user=davical_dba')
cur = conn.cursor()
cur.execute('SELECT addressbook_resource.n, addressbook_address_email.type, '
            'addressbook_address_email.email, addressbook_address_tel.type, '
            'addressbook_address_tel.tel, caldav_data.dav_id '
            'FROM addressbook_address_tel '
            'LEFT JOIN addressbook_address_email ON '
            'addressbook_address_tel.dav_id = '
            'addressbook_address_email.dav_id '
            'LEFT JOIN addressbook_resource ON '
            'addressbook_resource.dav_id = '
            'addressbook_address_email.dav_id '
            'LEFT JOIN caldav_data ON '
            'caldav_data.dav_id = '
            'addressbook_resource.dav_id '
            'LEFT JOIN usr ON '
            'usr.user_no = '
            'caldav_data.user_no '
            'WHERE usr.username = %s;', (username, ))

data = {}
for i in cur:
    name = i[0].split(';')
    last = name[0].strip()
    first = name[1].strip()

    nick = first.replace(' ', '').replace('-', '') + last.replace(' ', '').replace('-', '')
    try:
        emailtype = i[1].strip().upper()
    except AttributeError:
        sys.stderr.write(f'Unstrippable input {i} for {nick}, probably missing email type\n')
        continue
    if 'HOME' in emailtype:
        nick += ':H'
    elif 'WORK' in emailtype:
        nick += ':W'
    elif 'OTHER' in emailtype:
        nick += ':O'
    elif 'CELL' in emailtype:
        nick += ':C'
    else:
        sys.stderr.write(f'Unsupported email type {emailtype} for {nick}\n')

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
    elif 'VOICE' in teltype:
        tel = 'V:' + tel
    else:
        sys.stderr.write(f'Unsupported telephone type {teltype} for {nick}\n')

    key = i[5] # id
    if key not in data:
        data[key] = f'{nick}|{first}|{last}|{email}|{tel}'
    else:
        data[key] = f'{data[key]} {tel}'

cur.execute('SELECT addressbook_resource.n, addressbook_address_tel.type, '
            'addressbook_address_tel.tel, caldav_data.dav_id '
            'FROM addressbook_address_tel '
            'LEFT JOIN addressbook_resource ON '
            'addressbook_resource.dav_id = addressbook_address_tel.dav_id '
            'LEFT JOIN caldav_data ON '
            'caldav_data.dav_id = addressbook_resource.dav_id '
            'LEFT JOIN usr ON '
            'usr.user_no = caldav_data.user_no '
            'WHERE usr.username = %s;', (username, ))

# without email
tels = {}
for i in cur:
    name = i[0].split(';')
    last = name[0].strip()
    first = name[1].strip()
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
    elif 'VOICE' in teltype:
        tel = 'V:' + tel
    else:
        sys.stderr.write(f'Unsupported telephone type {teltype} for {nick}\n')

    key = i[3] # id
    if key not in data:
        if key not in tels:
            tels[key] = f'{nick}|{first}|{last}|d@um.my|{tel}'
        else:
            tels[key] = f'{tels[key]} {tel}'

cur.close()
conn.close()

data.update(tels)

# sort on id, newest entries at top
for key in sorted(data.keys(), reverse=True):
    print(data[key])
