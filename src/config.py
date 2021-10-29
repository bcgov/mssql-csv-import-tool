import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:

    TEST_DB_HOST                        = os.getenv('TEST_DB_HOST')
    TEST_DB_NAME                        = os.getenv('TEST_DB_NAME')
    TEST_DB_USERNAME                    = os.getenv('TEST_DB_USERNAME')
    TEST_DB_PASSWORD                    = os.getenv('TEST_DB_PASSWORD')

    # Path of destination Windows share from local perspective
    TEST_SHARE_LOCAL                    = os.getenv('TEST_SHARE_LOCAL')
    # Path of destination Windows share from database server perspective
    TEST_SHARE_DB                       = os.getenv('TEST_SHARE_DB')

    # BI PRODUCTION DATABASE
    PROD_DB_HOST                        = os.getenv('PROD_DB_HOST')
    PROD_DB_NAME                        = os.getenv('PROD_DB_NAME')
    PROD_DB_USERNAME                    = os.getenv('PROD_DB_USERNAME')
    PROD_DB_PASSWORD                    = os.getenv('PROD_DB_PASSWORD')

    # Path of destination Windows share from local perspective
    PROD_SHARE_LOCAL                    = os.getenv('PROD_SHARE_LOCAL')
    # Path of destination Windows share from database server perspective
    PROD_SHARE_DB                       = os.getenv('PROD_SHARE_DB')

    # THE ODBC DRIVER MUST BE INSTALLED IN THE CONTAINER
    ODBC_DRIVER                         = 'ODBC Driver 17 for SQL Server'

    # Pandas options
    CHUNK_SIZE                          = 5000
    TEMPORARY_TABLE_NAME                = '#temporary_data'

    # Number of seconds to wait before bulk importing the temporary file
    BULK_IMPORT_WAIT                     = int(os.getenv('BULK_IMPORT_WAIT', '10'))
