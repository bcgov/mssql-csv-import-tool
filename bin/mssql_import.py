import src.helper as helper
import src.business as business
import argparse
from src.config import Config


def main():
    d = 'Clean and verify CSV file, import to a temporary table and '
    d += 'merge the temporary table with destination table. If the source file '
    d += 'includes dates the format must be declared with either --month_first or --day_first '
    d += '(version: 0.26)'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('-f', '--filename', required=True, help='path and filename of the CSV file for import')
    parser.add_argument('-t', '--table',
                        required=True,
                        help='destination schema and table name')
    parser.add_argument('-e', '--environment',
                        choices=['TEST', 'PROD'],
                        default='TEST',
                        help='destination database environment')
    parser.add_argument('-d', '--delimiter',
                        default=',',
                        help="source file column delimiter. defaults to: -d ','")
    parser.add_argument('-n', '--dry_run', action='store_true',
                        help="run through import process but don't commit the changes")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase the verbosity of log output")
    parser.add_argument('--day_first', dest='day_first', action='store_true',
                        help="source date formatted with day before month: 31/03/2020 or 2020-31-03")
    parser.add_argument('--month_first', dest='day_first', action='store_false',
                        help="source date formatted with month before day: 03/31/2020 or 2020-03-31")
    parser.set_defaults(day_first=None)
    args = parser.parse_args()

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=args.verbose,
                        delimiter=args.delimiter,
                        config=Config,
                        destination_table=args.table,
                        is_dry_run=args.dry_run,
                        environment=args.environment,
                        filename=args.filename,
                        day_first=args.day_first)


if __name__ == '__main__':
    main()


