from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
from typing import Any
load_dotenv()

DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_NAME = 'circles_local_database_python/cursor.py'
DEVELOPER_EMAIL = 'valeria.e@circ.zone and idan.a@circ.zone'
obj = {
    'component_id': DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=obj)


class Cursor():

    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def execute(self, sql_statement, sql_parameters=None) -> None:
        obj = {
            "sql_statement": sql_statement,
            "sql_parameters": str(sql_parameters)
        }
        logger.start(object=obj)
        if sql_parameters:
            quoted_parameters = [
                "'" + str(param) + "'" for param in sql_parameters]
            formatted_sql = sql_statement % tuple(quoted_parameters)
            sql_parameters_str = ", ".join(quoted_parameters)
        else:
            formatted_sql = sql_statement
            sql_parameters_str = "None"
        EXECUTE_METHOD_NAME = 'database-without-orm-local-python-package cursor.py execute()'
        logger.info(EXECUTE_METHOD_NAME, object={
            "full_sql_query": formatted_sql,
            "sql_parameters": sql_parameters_str,
            "sql_statement": sql_statement
        })
        self.cursor.execute(sql_statement, sql_parameters)
        logger.end(EXECUTE_METHOD_NAME)

    def fetchall(self) -> Any:
        logger.start()
        result = self.cursor.fetchall()
        logger.end("End of fetchall", object={'result': str(result)})
        return result

    def fetchone(self) -> Any:
        logger.start()
        result = self.cursor.fetchone()
        logger.end()
        return result

    def description(self) -> Any:
        logger.start()
        result = self.cursor.description
        logger.end(object={"result": str(result)})
        return result

    def lastrowid(self) -> int:
        logger.start()
        result = self.cursor.lastrowid
        logger.end(object={"result": str(result)})
        return result

    def close(self) -> None:
        logger.start()
        self.cursor.close()
        logger.end()
