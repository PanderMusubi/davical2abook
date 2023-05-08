# davical2abook

## Introduction

[DAViCal](https://en.wikipedia.org/wiki/DAViCal) CardDAV to [SquirrelMail](https://en.wikipedia.org/wiki/SquirrelMail) address book format (.abook) converter

This license is GPL, following the license of DAViCal.

Author is Pander Musubi <pander@users.sourceforge.net>

## Prerequisitsts

Please install Python 3 support for PostgreSQL with:

    sudo apt-get install python3-psycopg2

or

    sudo pip install -U psycopg2

Of course, have PostrgeSQL, DAViCal and SquirrelMail services running on the system.

## Usage

To schedule this script, one can add it to a file in `/etc/cron.d/`

Below is an example for a user called username to nightly override the personal
address book in SquirrelMail with the addresses from DAViCal:

```
57 05 * * * root su - postgres -c "python3 davical2abook.py username" > /var/lib/squirrelmail/data/username.abook
```

For this example, `davical2abook.py` can reside in `/var/lib/postgresql/`

Note that output is reverse sorted on id from DAViCal, listing the most
recently added address at the top. Also, addresses without emails but with
telephone numbers are also included, but with the dummy email addres `d@um.my`.
