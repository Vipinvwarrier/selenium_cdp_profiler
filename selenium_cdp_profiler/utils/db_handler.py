from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from selenium_cdp_profiler.configs.interface_configurations import Configurations


class DataBaseHandler(Configurations):

    def __init__(self):
        self.execution_id = None
        self.sql_engine = self.create_engine()
        self.fetch_execution_id()

    def create_engine(self):
        connection_url = self.get_connection_string()
        return create_engine(connection_url, echo=True)
    
    def get_execution_id(self):
        return self.execution_id

    def get_create_engine(self):
        return self.sql_engine


    def fetch_execution_id(self):
        query_string = f'SELECT TOP 1 execution_id FROM {self.master_table} ORDER BY execution_id DESC;'
        result = self.execute_db_cmd(query_string)
        self.execution_id = result[0]['execution_id'] if result and isinstance(result, list) else result

    def execute_db_cmd(self, query_string, params=None):
        with self.sql_engine.connect() as connection:
            try:
                query = text(query_string)
                connection.execute(query)
                connection.commit()
            except SQLAlchemyError as e:
                print("Error occurred during execution:", str(e))
                connection.rollback()

    def write_to_network_table(self, table_name, data):
        with self.sql_engine.connect() as connection:
            execution_id = self.execution_id
            try:
                for row in data:
                    query = text(f"INSERT INTO {self.network_table} (execution_id, API, [CALL], [TIME], STATUS, RESPONSE, TYPE) "
                                 "VALUES (:execution_id, :api, :call_time, :time_taken, :status, :response, :data_type)")

                    connection.execute(query, {
                        'execution_id': execution_id,
                        'api': row['API'],
                        'call_time': row['CALL'],
                        'time_taken': row['TIME'],
                        'status': row['STATUS'],
                        'response': str(row.get('RESPONSE', '')).replace("'", "''"),
                        'data_type': row['TYPE']
                    })
                connection.commit()
            except SQLAlchemyError as e:
                print("Error occurred during execution:", str(e))
                connection.rollback()

    def write_console_errors_to_db(self, console_errors):
        with self.sql_engine.connect() as connection:
            for error in console_errors:
                execution_id = self.execution_id
                page_title = error['page_title']
                error_message = error['error_message'].replace("'", "''")

                query = text(f"INSERT INTO {self.console_table} (execution_id, page_title, error_message) "
                    "VALUES (:execution_id, :page_title, :error_message)")

                params = {
                    'execution_id': execution_id,
                    'page_title': page_title,
                    'error_message': error_message
                }
                try:
                    connection.execute(query, params)
                    connection.commit()
                except SQLAlchemyError as e:
                    print("Error occurred during execution:", str(e))
                    connection.rollback()

