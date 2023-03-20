#File name:     sqlfunctions.py
#Description:   Contains several functions for connecting to sql server database
#               and execute sql server
#Author(s):     Connor Weldy, Nozomu Ohno, Michael Laramie

import pyodbc #used for executing sql statements

#Name:      executeSQL
#Purpose:   executes an sql query
#Input:     string sqlStatement - the query to be executed
#Output:    a cursor that contains the results of the query
def executeSQL(sqlStatement):
    crsr = connectSQLServer() #connect to the server
    return crsr.execute(sqlStatement) #return the cursor of the sql query

#Name:      insertSQL
#Purpose:   executes an sql query that changes a record in the database
#Input:     string sqlStatement - the query to be executed
#Output:    nothing - void. the tuple is inserted into the database
def insertSQL(sqlStatement):
    conn_str = ( #connection string for SQL Server
        r'DRIVER={SQL Server};Server=CS1;Database=FinancialManagement;UID=XXXXXXXXXXXX; PWD=XXXXXXXXXXXX;'
    )
    cnxn = pyodbc.connect(conn_str) #connect to sql server
    crsr = cnxn.cursor()
    variable = crsr.execute(sqlStatement) #execute the sql
    cnxn.commit() #commit the changes to the database since it is inserting (or deleting) a tuple in/from a table
    return variable #void variable

#Name:      connectSQLServer
#Purpose:   connects user to sql server for querying - used in executeSQL() and insertSQL()
#Input:     none
#Output:    cnxx.cursor() for sql server
def connectSQLServer():
    conn_str = ( #connection string for SQL Server
        r'DRIVER={SQL Server};Server=CS1;Database=FinancialManagement;UID=XXXXXXXXXXXX; PWD=XXXXXXXXXXXX;'
    )
    cnxn = pyodbc.connect(conn_str) #connect to sql server
    return cnxn.cursor()