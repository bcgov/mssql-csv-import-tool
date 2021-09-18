import os
import pyodbc
import logging
import json


def prompt_for_database_password_if_not_set(**args) -> tuple:
    db_host = args.get('db_host')
    environment = args.get('environment')
    if not args.get('db_password'):
        args['db_password'] = input("What's the database password for {} ({})".format(environment, db_host))
    return True, args


def set_environment_variables(**args) -> tuple:
    config = args.get('config')
    environment = args.get('environment')
    if environment == "PROD":
        args['db_host'] = config.PROD_DB_HOST
        args['db_name'] = config.PROD_DB_NAME
        args['db_username'] = config.PROD_DB_USERNAME
        args['db_password'] = config.PROD_DB_PASSWORD
        args['share_db'] = config.PROD_SHARE_DB
        args['share_local'] = config.PROD_SHARE_LOCAL
    else:
        args['db_host'] = config.TEST_DB_HOST
        args['db_name'] = config.TEST_DB_NAME
        args['db_username'] = config.TEST_DB_USERNAME
        args['db_password'] = config.TEST_DB_PASSWORD
        args['share_db'] = config.TEST_SHARE_DB
        args['share_local'] = config.TEST_SHARE_LOCAL
    return True, args


def get_database_connection_string(**args) -> tuple:
    config = args.get('config')
    connection_string = "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(
        config.ODBC_DRIVER,
        args.get('db_host'),
        args.get('db_name'),
        args.get('db_username'),
        args.get('db_password')
    )
    logging.debug(connection_string)
    args['connection_string'] = connection_string
    return True, args


def get_database_connection(**args) -> tuple:
    connection_string = args.get('connection_string')
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        args['connection'] = connection
        args['cursor'] = cursor
    except pyodbc.DatabaseError as error:
        logging.warning("Unable to connect")
        logging.warning(str(error))
        return False, args
    return True, args


def create_temporary_table(**args) -> tuple:
    config = args.get('config')
    header_record = args.get('header_record')
    destination_schema = args.get('destination_schema')
    cursor = args.get('cursor')
    connection = args.get('connection')
    sql = "CREATE TABLE {} ({})".format(
        config.TEMPORARY_TABLE_NAME,
        _create_table_columns(header_record, destination_schema))
    try:
        cursor.execute(sql)
    except pyodbc.DatabaseError as e:
        connection.rollback()
    connection.commit()
    logging.debug("SUCCESS: {}".format(sql))
    return True, args


def _create_table_columns(header_record, destination_schema) -> str:
    result = list()
    for column_name in header_record:
        column = destination_schema[column_name]
        if column['DATA_TYPE'] == 'varchar':
            result.append("{} VARCHAR({})".format(column_name, _varchar_length(column['CHARACTER_MAXIMUM_LENGTH'])))
        elif column['DATA_TYPE'] == 'numeric':
            result.append("{} NUMERIC({},{})".format(
                column_name,
                column['NUMERIC_PRECISION'],
                column['NUMERIC_SCALE']))
        elif column['DATA_TYPE'] == 'smallint':
            result.append("{} SMALLINT".format(column_name))
        elif column['DATA_TYPE'] == 'int':
            result.append("{} INT".format(column_name))
        elif column['DATA_TYPE'] == 'date':
            result.append("{} DATE".format(column_name))
        elif column['DATA_TYPE'] == 'datetime':
            result.append("{} DATETIME".format(column_name))
        elif column['DATA_TYPE'] == 'datetime2':
            result.append("{} DATETIME2".format(column_name))
        elif column['DATA_TYPE'] == 'time':
            result.append("{} TIME".format(column_name))
        else:
            logging.critical('data type not found: {}'.format(column))

    result_string = ", ".join(result)
    logging.debug(result_string)
    return result_string


def _varchar_length(max_length: int) -> str:
    """
    MS-SQL uses '-1' to indicate VARCHAR(MAX)
    This returns "MAX" when length is '-1'; otherwise length
    """
    if max_length < 0:
        return "MAX"
    return str(max_length)


def get_destination_table_schema(**args) -> tuple:
    destination_table = args.get('destination_table')
    destination = destination_table.split('.')
    schema = dict()
    cursor = args.get('cursor')
    columns = ['UPPER(COLUMN_NAME)', 'DATA_TYPE', 'CHARACTER_MAXIMUM_LENGTH',
               'NUMERIC_PRECISION', 'NUMERIC_SCALE', 'IS_NULLABLE']
    sql = "SELECT {} FROM {}.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}' AND TABLE_SCHEMA='{}';".format(
        ','.join(columns),
        args.get('db_name'),
        destination[1],
        destination[0])
    try:
        records = cursor.execute(sql).fetchall()
    except pyodbc.DatabaseError as e:
        logging.critical(str(e))
        return False, args
    if len(records) == 0:
        logging.critical('unable to find destination table: {}'.format(destination_table))
        return False, args
    for row in records:
        column_name = row[0]
        schema[column_name] = dict(zip(columns, row))
    logging.debug(sql)
    logging.debug("destination table schema: {}".format(json.dumps(schema)))
    args['destination_schema'] = schema
    return True, args


def get_destination_primary_keys(**args) -> tuple:
    destination_table = args.get('destination_table')
    destination = destination_table.split('.')
    primary_keys = list()
    cursor = args.get('cursor')
    sql = " SELECT Col.Column_Name FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS Tab, "
    sql += "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE Col "
    sql += "WHERE "
    sql += "Col.Constraint_Name = Tab.Constraint_Name "
    sql += "AND Col.Table_Name = Tab.Table_Name "
    sql += "AND Constraint_Type = 'PRIMARY KEY' "
    sql += "AND Col.Table_Name = '{}' ".format(destination[1])
    sql += "AND Col.CONSTRAINT_SCHEMA = '{}'".format(destination[0])

    try:
        records = cursor.execute(sql).fetchall()
    except pyodbc.DatabaseError as e:
        logging.critical(str(e))
        return False, args

    for row in records:
        primary_keys.append(row[0])
    if len(records) == 0:
        logging.critical('{} has no primary keys - aborting'.format(destination_table))
        return False, args
    logging.debug(sql)
    logging.debug("primary keys: " + str(primary_keys))
    args['primary_keys'] = primary_keys
    return True, args


def count_temporary_table_records(**args) -> tuple:
    config = args.get('config')
    cursor = args.get('cursor')
    sql = "SELECT count(*) FROM {}".format(config.TEMPORARY_TABLE_NAME)
    result = cursor.execute(sql).fetchall()
    logging.info("number of records imported to {}: {}".format(config.TEMPORARY_TABLE_NAME, result[0][0]))
    return True, args


def merge_temporary_table_into_destination(**args) -> tuple:
    header_record = args.get('header_record')
    primary_keys = args.get('primary_keys')
    filename = args.get('filename')
    destination_table = args.get('destination_table')
    is_dry_run = args.get('is_dry_run')
    config = args.get('config')
    cursor = args.get('cursor')
    connection = args.get('connection')
    sql = "MERGE {0} c USING {1} cu ON ({2}) ".format(
        destination_table,
        config.TEMPORARY_TABLE_NAME,
        _merge_on_primary_keys(primary_keys, 'cu', 'c'))
    sql += "WHEN MATCHED THEN UPDATE SET {} ".format(
        _comma_separated_string_of_matched_columns(header_record, "cu", "c"))
    sql += "WHEN NOT MATCHED BY TARGET THEN INSERT ({}) VALUES ({});".format(
        comma_separated_string_of_column_names(header_record),
        comma_separated_string_of_column_names(header_record, "cu.")
    )
    logging.debug("sql: " + sql)
    try:
        cursor.execute(sql)
    except pyodbc.OperationalError as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    except pyodbc.DataError as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    except pyodbc.IntegrityError as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    except pyodbc.ProgrammingError as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    except pyodbc.NotSupportedError as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    except pyodbc.DatabaseError as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    except pyodbc.Error as err:
        logging.warning(err)
        connection.rollback()
        logging.critical('rollback complete')
        return False, args
    if not is_dry_run:
        connection.commit()
        logging.info("SUCCESS: {} has been merged to into {}".format(filename, destination_table))
    else:
        logging.warning("DRY RUN OPTION SELECTED - NO CHANGES COMMITTED")
    return True, args


def close_database_connection(**args) -> tuple:
    cursor = args.get('cursor')
    connection = args.get('connection')
    cursor.close()
    connection.close()
    return True, args


def output_is_database(**args) -> tuple:
    return args.get('environment') in ['TEST', 'PROD'], args


def comma_separated_string_of_column_names(header_record, prefix='') -> str:
    result = list()
    for column in header_record:
        result.append(prefix + column)
    return ", ".join(result)


def _merge_on_primary_keys(primary_keys, prefix_a, prefix_b) -> str:
    result = list()
    for column in primary_keys:
        result.append("{1}.{0} = {2}.{0}".format(
            column,
            prefix_a,
            prefix_b
        ))
    return " AND ".join(result)


def _comma_separated_string_of_matched_columns(header_record, temporary: str, destination: str) -> str:
    result = list()
    for column in header_record:
        result.append("{1}.{0} = {2}.{0}".format(
            column,
            destination,
            temporary
        ))
    return ", ".join(result)


def bulk_import_from_text_file(**args) -> tuple:
    config = args.get('config')
    share_db_path = args.get('share_db')
    destination_filename = args.get('destination_filename')
    filepath_array = os.path.split(destination_filename)
    filename = share_db_path + filepath_array[1]
    cursor = args.get('cursor')
    connection = args.get('connection')
    sql = "BULK INSERT {} FROM '{}' WITH ".format(config.TEMPORARY_TABLE_NAME, filename)
    sql += "(FIRSTROW = 2, FIELDTERMINATOR ='|', ROWTERMINATOR =  '0x0a')"

    logging.debug("sql: " + sql)
    try:
        cursor.execute(sql)
    except pyodbc.DatabaseError as e:
        connection.rollback()
        logging.critical('error writing to db ' + str(e))
        return False, args
    connection.commit()
    logging.info("bulk import to {} complete".format(config.TEMPORARY_TABLE_NAME))
    return True, args

