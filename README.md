## Prerequisites
Install Python 3 from https://www.python.org/downloads/windows/

## Installation

`python -m pip install git+https://github.com/bcgov/mssql-csv-import-tool.git`

`python -m pip install git+https://github.com/bcgov/mssql-csv-import-tool.git --upgrade`


## Usage

`mssql-import -f H:\some-large-data-file.csv --table schema.table-name --environment PROD`


```
mssql-import [-h] -f FILENAME -t TABLE [-e {TEST,PROD}] [-d]

Clean and verify CSV file, bulk import to temporary table and then, 
merge temporary table with destination table.

optional arguments:
  -h, --help            show this help message and exit

  -f FILENAME, --filename FILENAME
                        path and filename of the CSV file for import
                        
  -t TABLE, --table TABLE
                        destination schema and table name
                        
  -e {TEST,PROD}, --environment {TEST,PROD}
                        destination database environment as configured in the .env
                        file. Defaults to 'TEST'
                        
  -d, --dry_run         run through import process but don't commit the changes
  
  -v --verbose          increase the verbosity of the log output

```


## Secrets
This command-line application uses the following environment variables
to determine the database name, database server, username etc. 

```
TEST_DB_HOST=
TEST_DB_NAME=
TEST_DB_USERNAME=
TEST_SHARE_DB=\SERVER`SHARE

PROD_DB_HOST=
PROD_DB_NAME=
PROD_DB_USERNAME=
PROD_SHARE_DB=
```

Save the
`.env` file in a directory located above where the executable is installed. 
Within Windows use `where mssql-import` to locate the executable.
