# Description: DAViCal CardDAV to SquirrelMail address book format (.abook) converter
# License: GPL, following the license of DAViCal
# Author: Pander Musubi <pander@users.sourceforge.net>

import psycopg2, re, sys

if len(sys.argv) != 2:
    sys.stderr.write('Missing required argument DAViCal username\n')
    exit(1)
username = sys.argv[1]
if not re.match("^[A-Za-z0-9_-]*$", username):
    sys.stderr.write('Username contains illegal characters\n')

conn = psycopg2.connect('dbname=davical user=davical_dba')
cur = conn.cursor()
cur.execute("select addressbook_resource.n, addressbook_address_email.type, addressbook_address_email.email, addressbook_address_tel.type,addressbook_address_tel.tel from addressbook_address_tel left join addressbook_address_email on addressbook_address_tel.dav_id = addressbook_address_email.dav_id left join addressbook_resource on addressbook_resource.dav_id = addressbook_address_email.dav_id left join caldav_data on caldav_data.dav_id = addressbook_resource.dav_id left join usr on usr.user_no = caldav_data.user_no where usr.username = %s;", (username, ))

data = {}
for i in cur:
    name = i[0].split(';')
    last = name[0].strip()
    first = name[1].strip()

    nick = first.replace(' ', '') + last.replace(' ', '')
    emailtype = i[1].strip().upper().replace('INTERNET~|~', '')
    if emailtype == 'HOME':
        nick += ':H'
    elif emailtype == 'WORK':
        nick += ':W'
    else:
        sys.stderr.write('Unknown addressbook_address_email.type: {0}\n'.format(emailtype))

    email = i[2].strip().lower()

    teltype = i[3].strip().upper().replace('~|~VOICE', '')
    tel = '+' + i[4].strip().replace(' ', '').replace('+', '')
    if teltype == 'CELL':
        tel = 'M:' + tel
    elif teltype == 'HOME':
        tel = 'H:' + tel
    elif teltype == 'WORK':
        tel = 'W:' + tel
    else:
        sys.stderr.write('Unknown addressbook_address_tel.type: {0}\n'.format(teltype))

    key = nick+'|'+first+'|'+last+'|'+email+'|'
    if key not in data:
        data[key] = tel
    else:
        data[key] = data[key] + ' ' + tel

cur.close()
conn.close()

for key in sorted(data.keys()):
    print key + data[key]
