#!/usr/bin/python

import imaplib, getopt, sys
import time
import MySQLdb as mdb

def main (argv):
        user = ''
        password = ''
        server = ''

        try:
                opts, args = getopt.getopt (argv, 'u:p:s:', ['uuser=', 'ppassword=', 'sserver='])
        except getopt.GetoptError as err:
                print str (err)
                print 'Syntax: emailcount.py -s <servername> -u <username> -p <password>'
                sys.exit (2);

        for opt, arg in opts:
                if opt == '-s':
                        server = arg
                elif opt == '-p':
                        password = arg
                elif opt == '-u':
                        user = arg

        mail = imaplib.IMAP4_SSL(server);
        status = mail.login (user, password)
	status, count_array = mail.select ('Deleted Items');
	deleted_count = count_array [0];

        status, count_array = mail.select ('inbox');

        inbox_count = count_array [0];

        unread_count = len (mail.search (None, 'UnSeen') [1][0].split ());

	con = mdb.connect ('localhost', 'loader', 'password', 'qs')

	with con:
		cur = con.cursor ()
		cur.execute ('insert into inbox (check_dt_tm, inbox_unread, inbox_total, deleted_total) \
			values (%s, %s, %s, %s)', (time.strftime ("%Y-%m-%d %H:%M:%S"), str (unread_count),
			inbox_count, deleted_count))
		

        print time.strftime ("%Y-%m-%d %H:%M:%S") + ', ' + str (unread_count) + ', ' + inbox_count + ', ' + deleted_count;
if __name__ == '__main__':
        main (sys.argv [1:])

