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