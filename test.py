# select addressbook_resource.n, addressbook_address_email.type, addressbook_address_email.email, addressbook_address_tel.type,addressbook_address_tel.property from addressbook_address_tel left join addressbook_address_email on addressbook_address_tel.dav_id = addressbook_address_email.dav_id left join addressbook_resource on addressbook_resource.dav_id = addressbook_address_email.dav_id limit 20;


#addressbook_address_tel
#dav_id type tel property

#addressbook_address_email
#dav_id type email property  

#addressbook_resource
#dav_id uid fn n


testdata = (
('jan ', 'smit', 'jan@smit.nl', 'j@smit.nl', '+31612341234', '+31612341234', '+31612341234', '+31612341234'),
('pieter', ' smit', 'p@smit.nl', '', '', '+31612341234', '+31612341234', '+31612341234'),
('kees', 'smit', '', '', '', '+31612341234', '+31612341234', '+31612341234 '),
('johan', 'smit', '', ' johan@smit.nl', '', '', '', ''),
)
Abook = {}

for test in testdata:
    (first, last, prefemail, email, mobtel, hometel, worktel, fax, ) = test

    # initialisation
    First = ''
    Last = ''
    Nick = ''
    Email = ''
    Info = ''

    # use Info for all telephone numbers
    firsttel = True
    if mobtel:
        if firsttel:
            firsttel = False
        else:
            Info += ' '
        Info += 'M:'+ mobtel.replace('|', '').strip()
    if hometel:
        if firsttel:
            firsttel = False
        else:
            Info += ' '
        Info += 'H:'+ hometel.replace('|', '').strip()
    if worktel:
        if firsttel:
            firsttel = False
        else:
            Info += ' '
        Info += 'W:'+ worktel.replace('|', '').strip()
    if fax:
        if firsttel:
            firsttel = False
        else:
            Info += ' '
        Info += 'F:'+ fax.replace('|', '').strip()

    # names
    if first != '' and last == '':
        First = first.replace('|', '').strip()
        Nick = First.replace(' ','')
    if first == '' and last != '':
        Last = last.replace('|', '').strip()
        Nick = Last.replace(' ','')
    if first != '' and last != '':
        First = first.replace('|', '').strip()
        Last = last.replace('|', '').strip()
        Nick = First.replace(' ','') + Last.replace(' ','')

    # entry for preferred email
    if prefemail != '':
        Email = prefemail.replace('|', '').strip()
        if first == '' and last == '':
            Nick = Email.replace(' ', '')
        if Nick in Abook:
            print 'Warning: Duplicate nickname:', Nick
        else:
            Abook[Nick] = Nick+'|'+First+'|'+Last+'|'+Email+'|'+Info

    # entry for other email
    if email != '':
        Email = email.replace('|', '').strip()
        if first == '' and last == '':
            Nick = Email.replace(' ', '')
        else:
            Nick += 'Add'
        if Nick in Abook:
            print 'Warning: Duplicate nickname:', Nick
        else:
            Abook[Nick] = Nick+'|'+First+'|'+Last+'|'+Email+'|'+Info


# write address book
for nick in sorted(Abook.keys()):
    print Abook[nick]
