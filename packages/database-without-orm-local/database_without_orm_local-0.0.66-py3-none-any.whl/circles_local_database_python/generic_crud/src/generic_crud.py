from circles_local_database_python.connector import Connector
from typing import Any
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'circles_local_database_python')
sys.path.append(src_path)
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_NAME = 'circles_local_database_python\\generic_crud'
DEVELOPER_EMAIL = 'sahar.g@circ.zone'
obj = {
    'component_id': DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=obj)


class GenericCRUD:

    def __init__(self):
        pass

    def _serialize_datetime(result):
        result_serializable = []
        for row in result:
            row_serializable = list(row)
            for i, value in enumerate(row_serializable):
                if isinstance(value, datetime):
                    row_serializable[i] = value.strftime('%Y-%m-%d %H:%M:%S')
            result_serializable.append(tuple(row_serializable))
        return result_serializable

    @staticmethod
    def get_records_by_id(schema_name: str, table_name: str, id_column_name: str, id_column_value: int) -> Any:
        """
        This method gets the data from the database for the given id and table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param id: The id of the data
        :param id_col_name: The name of the id column in the table (default: id)
        :return: The data from the database
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'id': id_column_value,
            'id_col_name': id_column_name
        }
        logger.start(object=obj)
        try:
            # Connect to the database
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            raise Exception(message)

        try:
            # Use the table name
            cursor.execute(f"USE {schema_name}")
            if id_column_name == "":
                # If the id column name is empty, select all the data from the table
                cursor.execute(f"SELECT * FROM {table_name}")
            else:
                # Else, select the data from the table where the id column name is equal to the id
                cursor.execute(
                    f"SELECT * FROM {table_name} WHERE {id_column_name} = {id_column_value}")

            # Get the result
            temp_result = cursor.fetchall()
            result = GenericCRUD._serialize_datetime(temp_result)
            # Return the result
            logger.end(object={'result': result})
            return result
        except Exception as e:
            message = "error: failed to get data from the database"
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            raise Exception(message)

    @staticmethod
    def fetchall_by_where_condition(schema_name: str, table_name: str, where_condition: str = "") -> Any:
        """
        This method gets the data from the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param where_cond: The where condition for the query (default: ""), no need to add the WHERE keyword
        :return: The data from the database for the given table name and where condition
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'where_condition': where_condition
        }
        logger.start(object=obj)
        try:
            # Connect to the database
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            # If the connection fails, write an error message to the log
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            raise Exception(message)

        try:
            # Select the database
            cursor.execute(f"USE {schema_name}")
        except Exception as e:
            message = "error: failed to select the database"
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            raise Exception(message)
        try:

            if where_condition == "":  # If the where condition is empty, select all the data from the table
                cursor.execute(f"SELECT * FROM {table_name}")
            else:
                cursor.execute(
                    f"SELECT * FROM {table_name} WHERE {where_condition}")

            result = cursor.fetchall()
            result = GenericCRUD._serialize_datetime(result)

            logger.end(object={'result': str(result)})
            return result
        except Exception as e:
            # If the database query fails, write an error message to the log
            message = "error: failed to get data from the database"
            logger.exception(message, object=e)
            logger.end()
            raise Exception(message)

    @staticmethod
    def insert(schema_name: str, table_name: str, json_data) -> Any:
        """
        This method inserts the data into the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to insert into the database (default: None)
        :return: The message and the ids of the inserted data
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'json_data': json_data
        }
        logger.start(object=obj)
        try:
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            raise Exception(message + str(e))

        try:
            added_ids = []
            cursor.execute(f"USE {schema_name}")
            if not json_data:
                message = 'No data provided'
                logger.error(message)
                raise Exception(message)

            # Extract the data from the json
            keys = ','.join(json_data.keys())
            values = ['{}'.format(y) for y in json_data.values()]
            values = ','.join(values)
            query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
            cursor.execute(query)
            added_ids.append(cursor.lastrowid())
            connection.commit()
            logger.end(
                object={'message': 'Contacts added successfully', 'contacts ids': added_ids})
            return {'message': 'Contacts added successfully', 'contacts ids': added_ids}

        except Exception as e:
            message = "error: failed to insert data into the database "
            logger.exception(message, object=e)
            logger.end(object={'message': message})
            raise Exception(message + str(e))

    @staticmethod
    def update(schema_name: str, table_name: str, data_json, id_column_name: str, id_column_value: int) -> Any:
        """
        This method updates the data in the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to update in the database
        :param id_col_name: The name of the id column in the table (default: id)
        :return: The message and the ids of the updated data
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'id_column_name': id_column_name
        }

        logger.start(object=obj)
        try:
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            return {'message': message}

        try:
            updated_ids = []
            cursor.execute(f"USE {schema_name}")
            if not data_json:
                message = 'No data provided'
                logger.error(message)
                raise Exception(message)

            # Extract the data from the json
            set_clause = ', '.join(
                [f"{key} = '{value}'" for key, value in data_json.items()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column_name} = {id_column_value}"
            cursor.execute(query)
            updated_ids.append(cursor.lastrowid())
            connection.commit()
            obj = {'updated_ids': updated_ids}
            logger.end('updated successfully', object=obj)
            return {'message': 'Contacts updated successfully', 'contacts ids': updated_ids}
        except Exception as e:
            message = "error: failed to update data in the database"
            logger.exception(message, object=e)
            logger.end(message)
            raise Exception(message)

    @staticmethod
    def update_by_where_condition(schema_name: str, table_name: str, data_json, where_condition: str) -> Any:
        """
        This method updates the data in the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to update in the database
        :param where_condition: The where condition for the query (no need to add the WHERE keyword)
        :return: The message and the ids of the updated data
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'where_condition': where_condition
        }
        logger.start(object=obj)
        try:
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            raise Exception(message + str(e))

        try:
            updated_ids = []
            cursor.execute(f"USE {schema_name}")
            if not data_json:
                message = 'No data provided'
                logger.error(message)
                raise Exception(message)

            # Extract the data from the json
            set_clause = ', '.join(
                [f"{key} = '{value}'" for key, value in data_json.items()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_condition}"
            print(query)
            cursor.execute(query)
            updated_ids.append(cursor.lastrowid())
            connection.commit()
            obj = {'updated_ids': updated_ids}
            logger.end('updated successfully', object=obj)
            return {'message': 'Contacts updated successfully', 'contacts ids': updated_ids}
        except Exception as e:
            message = "error: failed to update data in the database"
            logger.exception(message, object=e)
            logger.end(message)
            raise Exception(message + str(e))

    @staticmethod
    def delete(schema_name: str, table_name: str, data_json, id_column_name: str, id_column_value: int) -> None:
        """
        This method deletes the data from the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param json_data: The data to delete from the database
        :param id_col_name: The name of the id column in the table (default: id)
        :return: The message and the ids of the deleted data
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'id_column_name': id_column_name
        }
        logger.start(object=obj)
        try:
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            logger.end(message)
            raise Exception(message + str(e))

        deleted_ids = []
        try:
            cursor.execute(f"USE {schema_name}")
            if not data_json:
                message = 'No data provided'
                logger.error(message)
                logger.end()
                raise Exception(message)

            query = f"UPDATE {table_name} SET end_timestamp = NOW() WHERE {id_column_name} = {id_column_value};"
            cursor.execute(query)
            deleted_ids.append(cursor.lastrowid())
            connection.commit()
            logger.end('Deleted successfully', object={
                       'contacts ids': deleted_ids})
            return {'message': 'Deleted successfully', 'contacts ids': deleted_ids}
        except Exception as e:
            message = "error: failed to delete data from the database"
            logger.exception(message, object=e)
            logger.end(message)
            raise Exception(message + str(e))

    @staticmethod
    def delete_by_where_condition(schema_name: str, table_name: str, where_condition: str) -> None:
        """
        This method deletes the data from the database for the given table name.
        :param db_name: The name of the database
        :param table_name: The name of the table
        :param where_condition: The where condition for the query (no need to add the WHERE keyword)
        :return: The message and the ids of the deleted data
        """
        obj = {
            'schema_name': schema_name,
            'table_name': table_name,
            'where_condition': where_condition
        }
        logger.start(object=obj)
        try:
            connection = Connector.connect(schema_name=schema_name)
            cursor = connection.cursor()
        except Exception as e:
            message = "error: connection to the database failed"
            logger.exception(message, object=e)
            logger.end(message)
            raise Exception(message + str(e))

        deleted_ids = []
        try:
            cursor.execute(f"USE {schema_name}")
            if not where_condition:
                message = 'No where condition provided'
                logger.error(message)
                logger.end()
                raise Exception(message)

            query = f"UPDATE {table_name} SET end_timestamp = NOW() WHERE {where_condition};"
            cursor.execute(query)
            deleted_ids.append(cursor.lastrowid())
            connection.commit()
            logger.end('Deleted successfully', object={
                       'contacts ids': deleted_ids})
            return {'message': 'Deleted successfully', 'contacts ids': deleted_ids}
        except Exception as e:
            message = "error: failed to delete data from the database"
            logger.exception(message, object=e)
            logger.end(message)
            raise Exception(message + str(e))
