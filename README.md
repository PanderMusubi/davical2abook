davical2abook
=============

DAViCal CardDAV to SquirrelMail address book format (.abook) converter

This license is GPL, following the license of DAViCal.

Author is Pander Musubi <pander@users.sourceforge.net>

To schedule this script, one can add it to a file in /etc/cron.d/

Below is an example for a user called username to nightly override the personal
address book in SquirrelMail with the addresses from DAViCal:

```
57 05 * * * root su - postgres -c "python davical2abook.py username" > /var/lib/squirrelmail/data/username.abook
```

For this example, davical2abook.py resides in /var/lib/postgresql/
