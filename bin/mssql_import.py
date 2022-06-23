import src.helper as helper
import src.business as business
import pkg_resources
from src.config import Config
import argparse

VERSION = pkg_resources.require('mssql-csv-import-tool')[0].version


def main():
    parser = argparse.ArgumentParser(description="Import data to RSBC's Operational Data Warehouse ")
    parser.add_argument('-f', '--filename',
                        help='path and filename of the file for import')
    parser.add_argument('-d', '--destination',
                        choices=list(Config.IMPORT_TYPES.keys()),
                        help='Destination database schema and table name')
    parser.add_argument('-e', '--environment',
                        choices=['TEST', 'PROD'],
                        default='TEST',
                        help='destination database environment')
    parser.add_argument('--dry_run',
                        action='store_true',
                        help=" don't save the changes to the database")
    parser.add_argument('--debug',
                        action='store_true',
                        help=" show detailed output for debugging")
    args = parser.parse_args()

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=args.debug,
                        config=Config,
                        type=args.destination,
                        is_dry_run=args.dry_run,
                        environment=args.environment,
                        filename=args.filename)


if __name__ == '__main__':
    main()


