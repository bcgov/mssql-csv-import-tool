import src.helper as helper
import src.business as business
import argparse
import pkg_resources
from src.config import Config

VERSION = pkg_resources.require('mssql-csv-import-tool')[0].version

def main():
    d = 'Clean and verify CSV file, import to a temporary table and '
    d += 'merge the temporary table with destination table. Version: {}'.format(VERSION)
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('-f', '--filename', required=True, help='path and filename of the CSV file for import')
    parser.add_argument('--type',
                        choices=list(Config.IMPORT_TYPES.keys()),
                        required=True,
                        help='import type')
    parser.add_argument('--environment',
                        choices=['TEST', 'PROD'],
                        default='TEST',
                        help='destination database environment')
    parser.add_argument('-n', '--dry_run', action='store_true',
                        help="run through import process but don't commit the changes")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase the verbosity of log output")
    args = parser.parse_args()

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=args.verbose,
                        config=Config,
                        type=args.type,
                        is_dry_run=args.dry_run,
                        environment=args.environment,
                        filename=args.filename)


if __name__ == '__main__':
    main()


