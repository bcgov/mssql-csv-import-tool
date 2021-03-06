import logging
import os
import csv
import pandas as pd
import src.helper as helper
import src.business as business


def process_csv_in_chunks(**args) -> tuple:
    filename = args.get('filename')
    config = args.get('config')
    delimiter = args.get('delimiter')
    args['rows_written'] = 0
    with pd.read_csv(filename,
                     delimiter=delimiter,
                     header=int(not args.get('has_header_record')),
                     names=args.get('columns'),
                     dtype=object,
                     na_values='',
                     na_filter=False,
                     engine='c',
                     chunksize=config.CHUNK_SIZE) as reader:
        for indx, data_frame in enumerate(reader):
            args['chunk_index'] = indx
            args['data_frame'] = data_frame
            args = helper.middle_logic(business.process_dataframe(), **args)
            if args.get('critical_error'):
                return False, args
        # DEBUG data_frame.info()
    return True, args


def write_dataframe_to_file(**args) -> tuple:
    data_frame = args.get('data_frame')
    header_record = args.get('header_record')
    total_rows = args.get('total_rows', 1)
    chunk_index = args.get('chunk_index')
    is_initial_write = chunk_index == 0
    destination_filename = args.get('destination_filename')
    filepath_list = os.path.split(destination_filename)
    logging.debug('count of records in dataframe: ' + str(data_frame.shape[0]))
    logging.debug('is initial write to {}: {}'.format(destination_filename, bool(is_initial_write)))
    with open(destination_filename, "a") as openfile:
        data_frame.to_csv(openfile,
                          index=False,
                          mode='a',
                          sep='|',
                          date_format='%Y%m%d',
                          header=is_initial_write,
                          line_terminator='\n',
                          columns=header_record,
                          quoting=csv.QUOTE_NONE)
    rows_written = args.get('rows_written') + data_frame[data_frame.columns[0]].count()
    logging.debug('{} rows written to {} '.format(
        str(rows_written),
        filepath_list[1]))
    print('Progress: {}/{}'.format(rows_written, total_rows))
    args['rows_written'] = rows_written
    return True, args


def trim_string_values(**args) -> tuple:
    data_frame = args.get('data_frame')
    df_obj = data_frame.select_dtypes(['object'])
    data_frame[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    return True, args


def is_first_dataframe(**args) -> tuple:
    chunk_index = args.get('chunk_index')
    return chunk_index == 0, args


def create_header_record(**args) -> tuple:
    missing_columns = args.get('missing_columns')
    data_frame = args.get('data_frame')
    if len(data_frame.columns) > 0:
        header = [column for column in data_frame.columns if column not in missing_columns]
        logging.debug("columns to be imported: " + str(header))
        args['header_record'] = header
        return True, args
    logging.critical("No columns in the data_frame")
    return False, args


def get_list_of_date_columns(**args) -> tuple:
    header_record = args.get('header_record')
    destination_schema = args.get('destination_schema')
    result = list()
    for column in header_record:
        if destination_schema[column]['DATA_TYPE'] == 'date':
            result.append(column)
    args['date_columns'] = result
    return True, args


def check_date_format_set_if_date_fields_present(**args) -> tuple:
    date_columns = args.get('date_columns')
    day_first = args.get('day_first')
    if len(date_columns) > 0 and day_first is None:
        logging.critical('date format not set')
        args['critical_error'] = True
        return False, args
    return True, args


def format_numeric_values(**args) -> tuple:
    data_frame = args.get('data_frame')
    header_record = args.get('header_record')
    destination_schema = args.get('destination_schema')
    for column_name in header_record:
        if destination_schema[column_name]['DATA_TYPE'] == 'numeric':
            data_frame[column_name] = pd.to_numeric(data_frame[column_name])
    # TODO https://stackoverflow.com/a/62546734/14205069 for better solution
    return True, args


def convert_dates(**args) -> tuple:
    data_frame = args.get('data_frame')
    header_record = args.get('header_record')
    destination_schema = args.get('destination_schema')
    day_first = args.get('day_first')
    for column_name in header_record:
        if destination_schema[column_name]['DATA_TYPE'][0:4] == 'date':
            try:
                data_frame[column_name] = pd.to_datetime(data_frame[column_name], dayfirst=day_first)
            except pd.errors.OutOfBoundsDatetime as error:
                logging.warning(error)
                logging.warning('the error above has prevented the date or datetime values')
                logging.warning('from being converted correctly.  Fix the error and retry')
                args['critical_error'] = True
                return False, args
    return True, args


def check_all_csv_columns_have_matching_db_fields(**args) -> tuple:
    data_frame = args.get('data_frame')
    destination_schema = args.get('destination_schema')
    destination_table = args.get('destination_table')
    missing_columns = list()
    missing_columns_text = list()

    for i, column_name in enumerate(data_frame.columns):
        if column_name not in destination_schema:
            missing_columns.append(column_name)
            missing_columns_text.append('{} (col {})'.format(column_name, i + 1))
    if len(missing_columns) > 0:
        logging.warning('the following columns in the CSV file WILL NOT BE IMPORTED. '
                        'They cannot be found in the DB table "{}": {}'.format(
                                                                                destination_table,
                                                                                ", ".join(missing_columns_text)))
    args['missing_columns'] = missing_columns
    return True, args


def check_no_not_null_fields_missing(**args) -> tuple:
    header_record = args.get('header_record')
    destination_schema = args.get('destination_schema')
    for column in destination_schema:
        logging.debug(str(destination_schema[column]))
        if destination_schema[column]['IS_NULLABLE'] == 'NO':
            if column not in header_record:
                logging.debug("header_record: " + str(header_record))
                logging.critical("Database column '{}' cannot be NULL "
                                 "but it's not included in the CSV file".format(column))
                args['critical_error'] = True
                return False, args
    return True, args


def uppercase_column_names(**args) -> tuple:
    data_frame = args.get('data_frame')
    data_frame.columns = map(str.upper, data_frame.columns)
    return True, args
