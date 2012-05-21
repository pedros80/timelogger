#!/usr/bin/env python
""" 
time_logger.py

Store start and stop times for named tasks and calculate the previous time
spent on them.
Copyright (C) 2012 Peter Somerville

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

requires - python 2.x, Tkinter and MySQLdb.
run python setup_logger.py to start
change username and password in Logger() at bottom of script

"""

__author__ = "Peter Somerville"
__email__ = "peterwsomerville@gmail.com"
__version__ = "1.0.0"
__date__ = "21/5/12"


import MySQLdb as mdb
import sys


def main():
    if len(sys.argv)<4:
        print "usage: python %s db_host db_user password"%sys.argv[0]
        sys.exit(1)

    try:
        con = mdb.connect(sys.argv[1], sys.argv[2], sys.argv[3])
        cur = con.cursor()
        print "*"*8
        print
        print "connecting to mysql"
    except  mdb.Error as e:
        print "Failed to connect to mysql"
        sys.exit(1)
    try:
        cur.execute("DROP DATABASE IF EXISTS logger")
    except  mdb.Warning as e:
        pass
    try:
        cur.execute("CREATE DATABASE logger")
        print "creating logger database"
    except  mdb.Error as e:
        print "Failed to create new database"
        sys.exit(1)
    try:
        cur.execute("USE logger")
        print "switching to logger database"
    except  mdb.Error as e:
        print "Failed to connect to database"
        sys.exit(1)
    try:
        cur.execute("CREATE TABLE tasks (tid INT NOT NULL AUTO_INCREMENT,descript VARCHAR(200),PRIMARY KEY (tid))")
        print "creating tasks table"
        cur.execute("CREATE TABLE logs (tid INT NOT NULL,start DATETIME,stop DATETIME,PRIMARY KEY (tid, start))")
        print "creating logs table"
    except  mdb.Error as e:
        print "Failed to create tables"
        sys.exit(1)
    
    print
    print "*"*8
    print "database & tables created succesfully: now create a user."
    print "to match the user name and password in time_logger.py with the following"
    print "privileges; SELECT, INSERT, UPDATE & DELETE"
    
if __name__=="__main__":
    main()