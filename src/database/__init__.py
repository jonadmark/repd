import json
import os
import sqlite3
import time

class Database:
    def __init__(self, filename, timetoexpire):
        """Form the repd database handler

        Arguments:
        filename -- the filename (possibly with path) to store the database
        """
        self.filename = filename
        self.timetoexpire = timetoexpire
        self.statements = {
            'select_table': '''SELECT * FROM SQLITE_MASTER
                                WHERE LOWER(TYPE)='table'
                                  AND LOWER(NAME)=LOWER(?);''',
            'create_table': '''CREATE TABLE %s(
                                   RID INTEGER PRIMARY KEY,
                                   TIMESTAMP INTEGER,
                                   VALUE TEXT
                               );''',
            'insert_values': 'INSERT INTO %s(TIMESTAMP, VALUE)VALUES(?,?);',
            'select_interval': '''SELECT * FROM %s
                                   WHERE TIMESTAMP BETWEEN ? AND ?;''',
            'remove_expired': '''DELETE FROM %s WHERE TIMESTAMP < ?;'''
        }

    def insert(self, timestamp, resource, metric, value):
        """Insert new value for a metric in the database

        Arguments:
        timestamp -- timestamp in which the value was collected
        resource -- the resource name related to the metric
        metric -- the metric name
        value -- the value which was collected
        """
        table_name = resource.lower() + '_' + metric.lower()

        self._guarantee_table_exists(table_name)

        dbc = sqlite3.connect(self.filename)
        try:
            sql = self.statements['insert_values'] % (table_name, )
            parameters = (timestamp, value)
            dbc.execute(sql, parameters)
            dbc.commit()
        finally:
            dbc.close()
        if self.timetoexpire > 0:
            self._remove_expired(table_name)

    def get_values_interval(self, resource, metric, interval):
        """Select values related to the metric within the interval and return 
        then as a float list.

        Arguments:
        resource -- the resource name related to the metric
        metric -- the metric name
        interval -- a tuple of timestamps (begin, end)
        """
        table_name = resource.lower() + '_' + metric.lower()
        value_list = None

        dbc = sqlite3.connect(self.filename)
        try:
            sql = self.statements['select_interval'] % (table_name, )
            parameters = interval
            value_list = dbc.execute(sql, parameters).fetchall()
        finally:
            dbc.close()
            return value_list

    def _guarantee_table_exists(self, table_name):
        """Create a table if it does not exist."""
        dbc = sqlite3.connect(self.filename)
        try:
            sql = self.statements['select_table']
            parameters = (table_name, )
            if not dbc.execute(sql, parameters).fetchone():
                sql = self.statements['create_table'] % (table_name, )
                dbc.execute(sql)
                dbc.commit()
        finally:
            dbc.close()

    def _remove_expired(self, table_name):
        """Remove the metrics that have expired from the database table."""
        lasttimestamp = int(time.time()) - self.timetoexpire
        dbc = sqlite3.connect(self.filename)
        try:
            sql = self.statements['remove_expired'] % (table_name, )
            parameters = (lasttimestamp, )
            dbc.execute(sql, parameters)
            dbc.commit()
        finally:
            dbc.close()