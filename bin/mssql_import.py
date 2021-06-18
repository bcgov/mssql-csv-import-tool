import src.helper as helper
import src.business as business
import argparse
from src.config import Config


def main():
    d = 'Clean and verify CSV file, bulk import to temporary table and then, '
    d += 'merge temporary table with destination table.'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('-f', '--filename', required=True, help='path and filename of the CSV file for import')
    parser.add_argument('-t', '--table',
                        required=True,
                        help='destination schema and table name')
    parser.add_argument('-e', '--environment',
                        choices=['TEST', 'PROD'],
                        default='TEST',
                        help='destination database environment')
    parser.add_argument('-d', '--dry_run', action='store_true',
                        help="run through import process but don't commit the changes")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase the verbosity of log output")
    args = parser.parse_args()

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=args.verbose,
                        config=Config,
                        destination_table=args.table,
                        is_dry_run=args.dry_run,
                        environment=args.environment,
                        filename=args.filename)


if __name__ == '__main__':
    main()


