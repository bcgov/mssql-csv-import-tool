import logging
import requests
import pyodbc
import json
import src.helper as helper
import src.business as business


def geocode_each_record_write_to_db_in_chunks(**args) -> tuple:
    results = args.get('results')
    args['validated_records'] = list()
    args['number_records_written_to_db'] = 0
    while len(results) > 0:
        row = results.pop()
        logging.debug("----------------------------------------------------")
        args['row'] = row
        args = helper.middle_logic(business.geocode_each_record(), **args)
        results = args.get('results')
    logging.info('no more records in the database')
    return True, args


def get_tas_records_without_geolocation_data(**args) -> tuple:
    """
    Connect to the database and retrieve 200 records that require geocoding.
    """
    config = args.get('config')
    logging.info('getting {} database records from tas.accidents for geocoding'.format(config.CHUNK_SIZE))
    cursor = args.get('cursor')

    sql = "SELECT TOP {} a.acc_no, a.standard_city_name, a.block_number, ".format(config.CHUNK_SIZE) + \
        " a.street_travelled_on, a.st_travelled_on_type, a.st_travelled_on_direction, " + \
        " a.cross_street, a.cross_street_type, a.cross_street_direction" + \
        " FROM tas.accidents a" + \
        " LEFT JOIN gis.geolocations g ON a.acc_no = g.business_id" + \
        " WHERE g.business_id is NULL AND a.standard_city_name IS NOT NULL AND a.street_travelled_on IS NOT NULL;"

    try:
        records = cursor.execute(sql).fetchall()
        columns = [column[0] for column in cursor.description]
    except pyodbc.DatabaseError as error:
        error_string = str(error)
        logging.warning("Read from db failed: " + error_string)
        logging.warning(error_string)
        return False, dict({error_string: str(error)})

    results = list()
    for row in records:
        results.append(dict(zip(columns, row)))
    args['results'] = results
    return True, args


def database_write_threshold_not_reached(**args) -> tuple:
    validated_records = args.get('validated_records')
    results = args.get('results')
    logging.debug('+++++++++++++ number of validated records created: ' + str(len(validated_records)))
    return len(results) > 0, args


def create_data_bc_payload(**args) -> tuple:
    row = args.get('row')
    if row['block_number']:
        address_string = "{} {} {} {} BC".format(
            row.get('block_number'),
            _xstr(row.get('street_travelled_on')),
            _xstr(row.get('st_travelled_on_type')),
            row.get('standard_city_name')
        )
    elif row['cross_street']:
        address_string = "{} {} AND {} {} {} BC".format(
            row.get('street_travelled_on'),
            _xstr(row.get('st_travelled_on_type')),
            _xstr(row.get('cross_street')),
            _xstr(row.get('cross_street_type')),
            row.get('standard_city_name')
        )
    else:
        address_string = "{} {} {} BC".format(
            row.get('street_travelled_on'),
            _xstr(row.get('st_travelled_on_type')),
            row.get('standard_city_name')
        )
    args['address_string'] = {"addressString": address_string}
    return True, args


def callout_to_databc(**args) -> tuple:
    config = args.get('config')
    address_dict = args.get('address_string')
    try:
        # create query string and execute request
        # request's "params" url encodes the address string
        headers = {'apikey': config.DATA_BC_API_KEY}
        params = address_dict
        response = requests.get(config.DATA_BC_API_URL,
                                params=params,
                                headers=headers,
                                timeout=5)
    except requests.exceptions.ReadTimeout as error:
        row = args.get('row')
        key_id = row.get('acc_no')
        logging.warning(address_dict.get('addressString'))
        logging.warning('DataBC took too long to resolve acc_no: {}'.format(key_id))
        return False, args
    except requests.exceptions.ConnectionError as error:
        logging.warning('no response from the DataBC API')
        return False, args
    if response.status_code == 200:
        args['data_bc_response'] = response.json()
        logging.debug(json.dumps(response.json()))
        return True, args
    error = 'DataBC did not return a successful response'
    args['error_string'] = error
    logging.info(error)
    return False, args


def substitute_default_databc_response(**args) -> tuple:
    address_string = args.get('address_string')
    row = args.get('row')
    validated_records = args.get('validated_records')
    validated_records.append({
        "business_program": "TAS",
        "business_type": "accident",
        "business_id": row.get('acc_no'),
        "lat": "53.913051000000",
        "long": "-122.7452849",
        "databc_lat": "53.913051000000",
        "databc_long": "-122.7452849",
        "databc_precision": "PROVINCE",
        "[precision]": "PROVINCE",
        "requested_address": address_string.get('addressString'),
        "submitted_address": address_string.get('addressString'),
        "databc_score": "1",
        "full_address": "BC",
        "faults": '[]',
    })
    logging.warning("substituting default response from DataBC")
    logging.warning("----------------------------------------------------")
    args['validated_records'] = validated_records
    return True, args


def transform_response_from_databc(**args) -> tuple:
    data_bc_response = args.get('data_bc_response')
    address_string = args.get('address_string')
    row = args.get('row')
    logging.debug(json.dumps(data_bc_response))
    validated_records = args.get('validated_records')
    try:
        coordinates = data_bc_response['features'][0]['geometry']['coordinates']
        validated_records.append({
            "business_program": "TAS",
            "business_type": "accident",
            "business_id": row.get('acc_no'),
            "lat": coordinates[1],
            "long": coordinates[0],
            "databc_lat": coordinates[1],
            "databc_long": coordinates[0],
            "databc_precision": data_bc_response['features'][0]['properties']['matchPrecision'],
            "[precision]": data_bc_response['features'][0]['properties']['matchPrecision'],
            "requested_address": address_string.get('addressString'),
            "submitted_address": address_string.get('addressString'),
            "databc_score": data_bc_response['features'][0]['properties']['score'],
            "full_address": data_bc_response['features'][0]['properties']['fullAddress'],
            "faults": json.dumps(data_bc_response['features'][0]['properties']['faults']),
        })
        logging.debug("faults: {}".format(json.dumps(data_bc_response['features'][0]['properties']['faults'])))
    except AttributeError as error:
        error_string = 'response from DataBC did not match expected format'
        args['error_string'] = error_string
        logging.info(error_string)
        return False, args
    args['validated_records'] = validated_records
    return True, args


def write_geolocation_to_database(**args) -> tuple:
    validated_records = args.get('validated_records')
    config = args.get('config')
    logging.info("========== write to {} ==========".format(config.GEOLOCATION_TABLE_NAME))
    cursor = args.get('cursor')
    number_records_written_to_db = args.get('number_records_written_to_db')
    connection = args.get('connection')
    if len(validated_records) > 0:
        sql = "INSERT INTO {} ({}) VALUES ({})".format(
            config.GEOLOCATION_TABLE_NAME,
            _record_keys(validated_records),
            _record_keys(validated_records, True))
        logging.debug("sql " + sql)
        try:
            cursor.fast_executemany = True
            cursor.executemany(sql, _record_values(validated_records))
        except pyodbc.DatabaseError as e:
            connection.rollback()
            logging.critical('error writing to db ' + str(e))
            logging.critical(json.dumps(validated_records, indent=4, default=str))
            return False, args
        connection.commit()
        args['number_records_written_to_db'] = number_records_written_to_db + len(validated_records)
        args['validated_records'] = list()
    else:
        logging.info('no more DB records to write')
    logging.info('number of records written to {}: {}'.format(
        config.GEOLOCATION_TABLE_NAME, args.get('number_records_written_to_db')))
    return True, args


def _xstr(s):
    return '' if s is None else str(s)


def _record_keys(validated_records, is_placeholders=False) -> str:
    first_record = validated_records[0]
    if is_placeholders:
        return ",".join(["?" for x in first_record])
    else:
        return ",".join(first_record.keys())


def _record_values(validated_records) -> list:
    results = list()
    for row in validated_records:
        results.append(list(row.values()))
    logging.debug(json.dumps(results))
    return results

