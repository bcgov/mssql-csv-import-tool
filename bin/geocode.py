import logging
import argparse
import src.business as business
import src.helper as helper
from src.config import GeocodeTAS


def main():
    parser = argparse.ArgumentParser(description='Lookup Geocode tas.accident data in Open Data Warehouse')
    parser.add_argument('-e', '--environment', choices=['TEST', 'PROD'], default='TEST',
                        help='destination database environment')
    args = parser.parse_args()

    logging.info(args.environment)

    return helper.middle_logic(business.geocode_tas_accidents(),
                               config=GeocodeTAS,
                               environment=args.environment)


if __name__ == "__main__":
    main()





