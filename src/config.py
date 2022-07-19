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
    BULK_IMPORT_WAIT                     = int(os.getenv('BULK_IMPORT_WAIT', '3'))

    IMPORT_TYPES = dict({
        "ISC.tickets": {
            "table": "isc.violation_tickets",
            "has_header_record": True,
            "columns": [
                'VT_NUM',
                'VIOLATION_DATE',
                'VIOLATION_TIME_STAMP',
                'LICENCE_PLATE',
                'LOCATION_CODE',
                'VEHICLE_SPEED',
                'MVA_SECTION',
                'DUAL'
            ],
            "delimiter": ",",
            "day_first": False
        },
        "ICBC.contraventions": {
            "table": "icbc.contravention",
            "has_header_record": True,
            "columns": None,
            "delimiter": "|",
            "day_first": False
        },
        "DFCMS.document_images": {
            "table": "DFCMS.document_images",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": True
        },
        "DFCMS.case_test_consultations": {
            "table": "DFCMS.case_test_consultations",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "DFCMS.cases": {
            "table": "DFCMS.cases",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "TAS.accidents": {
            "table": "tas.accidents",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "TAS.entities": {
            "table": "tas.entities",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "TAS.victims": {
            "table": "tas.victims",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "VIPS.prohibitions": {
            "table": "vips.prohibitions",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "VIPS.impoundments": {
            "table": "vips.impoundments",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "VIPS.licences": {
            "table": "vips.licences",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        },
        "GIS.geolocations": {
            "table": "gis.geolocations",
            "has_header_record": True,
            "columns": None,
            "delimiter": ",",
            "day_first": None
        }
    })
