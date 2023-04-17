import sqlite3
from constants import *


class DataModel():

    def __init__(self, database: str, table_data: list[tuple], db_schema_path: str, table_name: str):
        '''Construct Call object
        :param database: name of database_file
        :param table_data: data to be inserted in database table
        :db_schema_path: path to file with database schema
        :table_name: name of database table'''
        self.database = database
        self.table_data = table_data
        self.db_schema_path = db_schema_path
        self.table_name = table_name

    def get_db_connection(self) -> sqlite3.Connection:
        '''
        creates connection to given database
        '''
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    def generate_database(self) -> None:
        '''
        creates table with given data, using given sql scheme
        '''
        conn = self.get_db_connection()
        with open(self.db_schema_path) as f:
            conn.executescript(f.read())
        cur = conn.cursor()
        for row in self.table_data:
            cur.execute(f'INSERT INTO {self.table_name} (id, ip, model, intercom_password, firmware, add_device) VALUES (?, ?, ?, ?, ?, ?)',
                        (row)
                        )
        conn.commit()
        conn.close()

    def get_device(self) -> list:
        '''
        returns data saved in database table
        '''
        conn = self.get_db_connection()
        data = conn.execute(f'SELECT * FROM {self.table_name}').fetchall()
        conn.close()
        return data
