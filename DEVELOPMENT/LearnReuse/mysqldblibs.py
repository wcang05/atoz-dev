#############################################################################################################################
## mysqldblibs.py
## Contain functions that related to Database management and processing.
## Contain functions that CRUD to MYSQL database.
##
## Author SY
## Start Date: 15-Mar-2018
## Last Modified: 15-Mar-2018
## Version: 1.0.01
##
## 19-Mar-2018  Successfully connecting to DB - Using pip install MySQL-python - Connector 6.0.2 x86
## 
##
#############################################################################################################################

import MySQLdb

#############################################################################################################################
## Global variable setting and configuration.
#############################################################################################################################
DB_SERVER   = "localhost"
DB_USERNM   = "brp2_db_service_acc"
DB_PASSWORD = "C0mm0nP@ssw0rd"
DB_SCHEMA   = "atoz_dev"
DB_TEST_TBL = "test_dev"

#def sql_insert(conn, tbl_nm, lst_field, lst_value):
#    try:
#        with conn.cursor() as cursor:
#            sql = "INSERT INTO %s (%s) VALUES(%s)"
#            cursor.execute(sql, 


def get_db_conn():
    # Open database connection
    db = MySQLdb.connect(DB_SERVER, DB_USERNM, DB_PASSWORD, DB_SCHEMA)
    return db


def test_db_conn():
    db = MySQLdb.connect(DB_SERVER, DB_USERNM, DB_PASSWORD, DB_SCHEMA)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        # Check if anything at all is returned
        if results:
            print (results)
            return True
        else:
            return False

    except MySQLdb.Error, e:
        print "ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1])

    finally:
        db.close()

    return False


def test_insert(conn):
    sql = """INSERT INTO %s(col1, col2, col3)
             VALUES ('ut-1', 'ut-2', 'ut-3')""" % DB_TEST_TBL
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()        
        return True
    except MySQLdb.Error, e:
        print "ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
    return False

def test_delete(conn):
    sql = """DELETE FROM %s WHERE idtest_dev = 1""" % DB_TEST_TBL
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        return True
    except MySQLdb.Error, e:
        print "ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()
    return False


def main():
    #################################################### 
    ## Unit test area for functions to be imported.
    #################################################### 
    print "Unit Test Area Started ...\n\n"

    if test_db_conn():
        print "Successfully connect DB : %s ...\n" % DB_SCHEMA

        ## Test insert record in table.        
        print "Test INSERT record into table %s ..." % DB_TEST_TBL
        conn = get_db_conn()    ## Obtain & Open DB connection.
        if test_insert(conn):
            print "Successfully INSERT record ...\n"

        ## Test delete record in table.        
        print "Test DELETE record into table %s ..." % DB_TEST_TBL
        conn = get_db_conn()    ## Obtain & Open DB connection.
        if test_delete(conn):
            print "Successfully DELETE record ...\n"

    print "Unit Test Completed ..."


if __name__ == "__main__":
    main()