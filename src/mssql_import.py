import src.helper as helper
import src.business as business
import argparse
from src.config import Config


def main():
    parser = argparse.ArgumentParser(description='Clean and verify CSV files before running stored procedures')
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
    args = parser.parse_args()

    helper.middle_logic(business.clean_and_verify_csv(),
                        config=Config,
                        destination_table=args.table,
                        is_dry_run=args.dry_run,
                        environment=args.environment,
                        filename=args.filename)


if __name__ == '__main__':
    main()


