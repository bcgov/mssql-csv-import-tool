from src.config import Config


def get_import_file_attributes(**args) -> tuple:
    import_type = args.get('type')
    if import_type not in Config.IMPORT_TYPES:
        return False, args
    args['destination_table'] = Config.IMPORT_TYPES[import_type]['table']
    args['has_header_record'] = Config.IMPORT_TYPES[import_type]['has_header_record']
    args['columns'] = Config.IMPORT_TYPES[import_type]['columns']
    args['delimiter'] = Config.IMPORT_TYPES[import_type]['delimiter']
    args['day_first'] = Config.IMPORT_TYPES[import_type]['table']
    return True, args
