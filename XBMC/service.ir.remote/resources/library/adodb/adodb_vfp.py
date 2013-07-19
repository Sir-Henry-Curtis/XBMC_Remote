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
        
class adodb_vfp(adodb_pyodbc.adodb_pyodbc):
    databaseType = 'vfp'
    dataProvider = 'mxodbc'
    sysDate = 'date()'
    sysTimeStamp = 'datetime()'
    replaceQuote = "'+chr(39)+'"
        
    def _newcursor(self,rs):
        return cursor_vfp(rs,self)    
        
class cursor_vfp(adodb_pyodbc.cursor_pyodbc):
    def __init__(self,rs,conn):
        adodb_pyodbc.cursor_pyodbc.__init__(self,rs,conn)
        self._rowcount = rs.rowcount

if __name__ == '__main__':
    db = adodb_vfp()
    db.Connect("Driver=Microsoft Visual FoxPro Driver;UID=;PWD=;SourceDB=D:\\inetpub\\adodb\\adoxyz.DBC;SourceType=DBC;Exclusive=No;BackgroundFetch=No;Collate=Machine;Null=Yes;Deleted=Yes;")
    adodb.Test(db)