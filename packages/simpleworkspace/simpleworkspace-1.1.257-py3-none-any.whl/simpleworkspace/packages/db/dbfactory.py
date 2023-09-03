class DBFactory:
    @classmethod
    def SQLite3_Memory(cls):
        import sqlite3
        return sqlite3.connect(':memory:')
    
    @classmethod
    def SQLite3_File(cls, databasePath:str):
        '''creates a new sqlite3 file db, or reuses if already existing at specified path'''
        import sqlite3
        return sqlite3.connect(databasePath)
    
    @classmethod
    def MSSQL_LocalDB(cls, database:str="tempdb", instanceName='MSSQLLocalDB'):
        '''when database is not specified an temporary one will be created, and deleted at end of python script'''
        return cls.MSSQL(server=f"(localdb)\\{instanceName}", database=database, UseWindowsAuthentication=True)
    
    @classmethod
    def MSSQL(cls, server:str, database:str=None, driver="{ODBC Driver 17 for SQL Server}", UseWindowsAuthentication=True):
        import pyodbc

        connString = f"Driver={driver};Server={server};Database={database};"
        if(UseWindowsAuthentication):
            connString += "Integrated Security=SSPI;"

        return pyodbc.connect(connString)