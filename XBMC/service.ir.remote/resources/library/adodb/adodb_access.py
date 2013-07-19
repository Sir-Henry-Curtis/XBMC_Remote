########################################################################
# Vers 2.10 16 July 2008, (c)2004-2008 John Lim (jlim#natsoft.com) All Rights Reserved
# Released under a BSD-style license. See LICENSE.txt.
# Download: http://adodb.sourceforge.net/#pydownload
########################################################################

import adodb,adodb_pyodbc,datetime

try:
    True, False
except NameError:
    # Maintain compatibility with Python 2.2
    True, False = 1, 0
        
class adodb_access(adodb_pyodbc.adodb_pyodbc):
    databaseType = 'access'
    dataProvider = 'pyodbc'
    sysDate = "FORMAT(NOW,'yyyy-mm-dd')"
    sysTimeStamp = 'NOW'
    
    def _newcursor(self,rs):
        return cursor_access(rs,self)    
        
class cursor_access(adodb_pyodbc.cursor_pyodbc):
    def __init__(self,rs,conn):
        adodb_pyodbc.cursor_pyodbc.__init__(self,rs,conn)
        self._rowcount = rs.rowcount

if __name__ == '__main__':
    db = adodb_access()
    db.Connect("Driver={Microsoft Access Driver (*.mdb)};Dbq=d:\\inetpub\\adodb\\northwind.mdb;Uid=Admin;Pwd=;")
    adodb.Test(db)