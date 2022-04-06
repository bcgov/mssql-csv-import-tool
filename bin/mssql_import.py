import src.helper as helper
import src.business as business
import pkg_resources
from src.config import Config
from gooey import Gooey, GooeyParser

VERSION = pkg_resources.require('mssql-csv-import-tool')[0].version


@Gooey(
    show_restart_button=False,
    terminal_font_color='FFFFFF',
    progress_regex=r"^Progress: (\d+)/(\d+)$",
    progress_expr="x[0] / x[1] * 100",
    clear_before_run=True
    )
def main():
    parser = GooeyParser(description="Import data to RSBC's Operational Data Warehouse ")
    filename_group = parser.add_argument_group()
    filename_group.add_argument('--filename',
                        help='path and filename of the file for import',
                        widget='FileChooser')
    type_group = parser.add_argument_group()
    type_group.add_argument('--type',
                        choices=list(Config.IMPORT_TYPES.keys()),
                        help='Destination database schema and table name')
    environment_group = parser.add_argument_group()
    environment_group.add_argument('--environment',
                        choices=['TEST', 'PROD'],
                        default='TEST',
                        help='destination database environment')
    optional_group = parser.add_argument_group(
        "Optional",
        "Typically for debugging purposes"
    )
    optional_group.add_argument('--dry_run',
                        action='store_true',
                        help=" don't save the changes to the database")
    optional_group.add_argument('--debug',
                        action='store_true',
                        help=" show detailed output for debugging")
    args = parser.parse_args()

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=args.debug,
                        config=Config,
                        type=args.type,
                        is_dry_run=args.dry_run,
                        environment=args.environment,
                        filename=args.filename)


if __name__ == '__main__':
    main()


