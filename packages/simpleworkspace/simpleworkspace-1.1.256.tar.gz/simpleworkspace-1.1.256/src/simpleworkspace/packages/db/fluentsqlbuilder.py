import time
from typing import List, Optional, Generator
from ...utility.stopwatch import StopWatch
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from pyodbc import Connection as MsSqlConnection
from pyodbc import Cursor as MsSqlCursor
import pyodbc
import mysql
import sqlite3
from sqlite3 import Connection as Sqlite3Connection
from sqlite3 import Cursor as Sqlite3Cursor


class _FluentSqlBuilderExecuteResults:
    def __init__(self, executed_statement: Sqlite3Cursor|MsSqlCursor|MySQLCursor, execution_time_ms):
        self._executed_statement = executed_statement
        self.execution_time_ms = execution_time_ms
        self._FetchMode_Dictionary = True

    def _OnGetRow(self, row: tuple):
        '''row is by default cursors expected to be numeric index mode'''

        if not (self._FetchMode_Dictionary):
            return row
        
        row_dict = {}
        for i, value in enumerate(row):
            column_name = self._executed_statement.description[i][0]
            row_dict[column_name] = value
        return row_dict
    
    def FirstOrDefault(self) -> dict|tuple|None:
        for row in self.Iterator():
            return row
        return None

    def ToArray(self) -> List[dict]|List[tuple]|None:
        return list(self.Iterator())

    def Iterator(self) -> Generator[int, dict|tuple, None]:
        while True:
            row = self._executed_statement.fetchone()
            if row is None:
                break
            yield self._OnGetRow(row)

    def AffectedRowCount(self) -> int:
        return self._executed_statement.rowcount

    def SetFetchMode_Dictionary(self):
        self._FetchMode_Dictionary = True
        return self
    
    def SetFetchMode_NumericIndex(self):
        self._FetchMode_Dictionary = False
        return self

    def __del__(self):
        self._executed_statement.close()


class FluentSqlBuilderError(Exception):
    def __init__(self, operation: str, message: str):
        if operation:
            message = f"{operation}: {message}"
        super().__init__(message)

class FluentSqlBuilder:
    def __init__(self, connection: MySQLConnection|MsSqlConnection|Sqlite3Connection):
        self._connection = connection
        self._segments = []
        self._params = []
        self._fetchModeDictionary = True

    def CreateTable(self, table_name: str, ignoreIfExists: bool = True):
        if not table_name:
            raise FluentSqlBuilderError("create_table", "No table name specified")

        sql = f"CREATE TABLE IF NOT EXISTS {table_name}" if ignoreIfExists else f"CREATE TABLE {table_name}"
        self.Append(sql)
        return self

    def Column(self, column_name: str, attributes: str, foreignKeyReference: Optional[str] = None):
        if not column_name or not attributes:
            raise FluentSqlBuilderError("column", "Empty column name or attributes")

        last_segment = self.GetLastSegment()
        if not isinstance(last_segment, _FluentSqlBuilderChainableClauseColumn):
            last_segment = _FluentSqlBuilderChainableClauseColumn()
            self._segments.append(last_segment)

        last_segment.Add(f"{column_name} {attributes}")
        if foreignKeyReference:
            last_segment.Add(f"FOREIGN KEY ({column_name}) REFERENCES {foreignKeyReference}")
        return self

    def Select(self, *column_names: str):
        if not column_names:
            raise FluentSqlBuilderError("select", "Nothing selected")

        sql = f"SELECT {', '.join(column_names)}"
        self.Append(sql)
        return self

    def From(self, table_name: str):
        if not table_name:
            raise FluentSqlBuilderError("from_table", "Table name not specified")

        sql = f"FROM {table_name}"
        self.Append(sql)
        return self

    def Insert(self, table_name: str, *key_value_pairs: dict):
        if not table_name or not key_value_pairs:
            raise FluentSqlBuilderError("insert", "Empty or invalid table/keyValuePairs")

        column_names = list(key_value_pairs[0].keys())
        value_placeholder_template = "(" + self.GeneratePreparedPlaceholders(len(column_names)) + ")"
        value_placeholders = []

        for row_mapping in key_value_pairs:
            self._params.extend(list(row_mapping.values()))
            value_placeholders.append(value_placeholder_template)

        column_names = ', '.join(column_names)
        value_placeholders = ', '.join(value_placeholders)
        sql = f"INSERT INTO {table_name} ({column_names}) VALUES {value_placeholders}"
        self.Append(sql)
        return self

    def OnDuplicateKeyUpdate(self):
        if not self._IsStatementInsert():
            raise FluentSqlBuilderError("on_duplicate_key_update", "Used in conjunction with insert statements only")

        self.Append("ON DUPLICATE KEY UPDATE")
        return self

    def Update(self, table_name: str):
        if not table_name:
            raise FluentSqlBuilderError("update", "Empty table")

        self.Append(f"UPDATE {table_name} SET")
        return self

    def Set(self, sql: str, *params):
        if not sql:
            raise FluentSqlBuilderError("set", "Empty assignment")

        last_segment = self.GetLastSegment()
        if not isinstance(last_segment, _FluentSqlBuilderChainableClauseSet):
            last_segment = _FluentSqlBuilderChainableClauseSet()
            self._segments.append(last_segment)

        last_segment.Add(sql)
        self._params.extend(params)
        return self

    def Delete(self):
        self.Append("DELETE")
        return self

    def Join(self, table_name: str, on_condition: str):
        if not table_name or not on_condition:
            raise FluentSqlBuilderError("join", "Empty tableName/onCondition")

        self.Append(f"JOIN {table_name} ON {on_condition}")
        return self

    def Where(self, condition: str, *params):
        if not condition:
            raise FluentSqlBuilderError("where", "Empty condition")

        self.Append(f"WHERE {condition}", *params)
        return self

    def WhereIn(self, column_name: str, *params):
        self.GenericInClause("WHERE", column_name, *params)
        return self

    def WhereNotIn(self, column_name: str, *params):
        self.GenericNotInClause("WHERE", column_name, *params)
        return self

    def And(self, condition: str, *params):
        if not condition:
            raise FluentSqlBuilderError("And", "Empty condition")

        self.Append(f"AND {condition}", *params)
        return self

    def AndNot(self, condition: str, *params):
        if not condition:
            raise FluentSqlBuilderError("AndNot", "Empty condition")

        self.Append(f"AND NOT {condition}", *params)
        return self

    def AndIn(self, column_name: str, *params):
        self.GenericInClause("AND", column_name, *params)
        return self

    def AndNotIn(self, column_name: str, *params):
        self.GenericNotInClause("AND", column_name, *params)
        return self

    def Or(self, condition: str, *params):
        if not condition:
            raise FluentSqlBuilderError("Or", "Empty condition")

        self.Append(f"OR {condition}", *params)
        return self

    def OrNot(self, condition: str, *params):
        if not condition:
            raise FluentSqlBuilderError("OrNot", "Empty condition")

        self.Append(f"OR NOT {condition}", *params)
        return self

    def OrIn(self, column_name: str, *params):
        self.GenericInClause("OR", column_name, *params)
        return self

    def OrNotIn(self, column_name: str, *params):
        self.GenericNotInClause("OR", column_name, *params)
        return self

    def Append(self, sql: str, *params):
        if not sql:
            raise FluentSqlBuilderError("append", "Empty SQL")

        self._segments.append(sql)
        if params:
            self._params.extend(params)
        return self

    def OrderByAscending(self, column_name: str):
        return self.OrderBy(column_name, "ASC")

    def OrderByDescending(self, column_name: str):
        return self.OrderBy(column_name, "DESC")

    def OrderBy(self, column_name: str, direction: str):
        if not column_name or not direction:
            raise FluentSqlBuilderError("ORDERBY", "Empty column name or direction")

        last_segment = self.GetLastSegment()
        if not isinstance(last_segment, _FluentSqlBuilderChainableClauseOrderBy):
            last_segment = _FluentSqlBuilderChainableClauseOrderBy()
            self._segments.append(last_segment)

        last_segment.Add(column_name, direction)
        return self

    def Limit(self, max_row_count: int):
        self.Append(f"LIMIT {max_row_count}")
        return self

    def Execute(self):
        sw = StopWatch()
        sw.Start()
        self._ValidateBuiltQuery()

        cursor = self._connection.cursor()
        cursor.execute(str(self), self._params)

        sw.Stop()
        return _FluentSqlBuilderExecuteResults(cursor, sw.GetElapsedMilliseconds())

    def __str__(self):
        return " ".join(str(segment) for segment in self._segments)

    def _ValidateBuiltQuery(self):
        if not self._segments:
            raise FluentSqlBuilderError("Execute", "No query")

        if self._IsStatementUpdate() or self._IsStatementDelete():
            if not self._HasClauseWhere():
                raise FluentSqlBuilderError("Execute", "Safety check error, Update/Delete queries must have a where condition, otherwise all rows in the table would be altered")

    def _HasClauseWhere(self):
        for segment in self._segments:
            if not (isinstance(segment, str)): #where queries are only part of string segments
                continue
            if segment.startswith("WHERE"):
                return True
        return False

    def _IsStatementInsert(self):
        if not self._segments:
            return False
        return str(self._segments[0]).startswith("INSERT")

    def _IsStatementUpdate(self):
        if not self._segments:
            return False
        return str(self._segments[0]).startswith("UPDATE")

    def _IsStatementDelete(self):
        if not self._segments:
            return False
        return str(self._segments[0]).startswith("DELETE")

    def GenericInClause(self, prefix: str, column_name: str, *params):
        if not params or not column_name:
            raise FluentSqlBuilderError("generic_in_clause", "Nothing compared")

        placeholders = self.GeneratePreparedPlaceholders(len(params))
        self.Append(f"{prefix} {column_name} IN ({placeholders})", *params)

    def GenericNotInClause(self, prefix: str, column_name: str, *params):
        if not params or not column_name:
            raise FluentSqlBuilderError("generic_not_in_clause", "Nothing compared")

        placeholders = self.GeneratePreparedPlaceholders(len(params))
        self.Append(f"{prefix} {column_name} NOT IN ({placeholders})", *params)

    @staticmethod
    def GeneratePreparedPlaceholders(placeholder_count: int) -> str:
        if placeholder_count <= 0:
            return ""
        return ', '.join(['?'] * placeholder_count)

    def GetSegmentCount(self) -> int:
        return len(self._segments)

    def GetLastSegment(self):
        if not self._segments:
            return None
        return self._segments[-1]


class _FluentSqlBuilderChainableClauseColumn:
    def __init__(self):
        self._segments = []

    def Add(self, sql: str):
        self._segments.append(sql)

    def __str__(self):
        return '(' + ', '.join(self._segments) + ')'


class _FluentSqlBuilderChainableClauseSet:
    def __init__(self):
        self._segments = []

    def Add(self, sql: str):
        self._segments.append(sql)

    def __str__(self):
        return ', '.join(self._segments)


class _FluentSqlBuilderChainableClauseOrderBy:
    def __init__(self):
        self._segments = []

    def Add(self, column_name: str, direction: str):
        self._segments.append(f"{column_name} {direction}")

    def __str__(self):
        return "ORDER BY " + ', '.join(self._segments)


