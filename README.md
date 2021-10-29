![Lifecycle:Experimental](https://img.shields.io/badge/Lifecycle-Experimental-339999)

## Background
MS-SQL's built-in bulk import tool cannot parse comma separated value (CSV) files when the values 
contain a comma even if the value is wrapped in quotes. For example, below is a two-column import file:

```text
Column1,Column2
"Some Text","Some, other text"
```

MS-SQL's bulk import tool counts the comma after the word "Some" as a delimiter which incorrectly increases
the number of columns in the first data row from two to three.

This tool helps correct and import CSV files to MS-SQL.

## Prerequisites
Install `python3` from https://www.python.org/downloads/windows/

Install `git`: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

## Installation
From Windows command prompt:

`pip install git+https://github.com/bcgov/mssql-csv-import-tool.git`

`pip install git+https://github.com/bcgov/mssql-csv-import-tool.git --upgrade`


## Usage

`mssql-import -f H:\some-large-data-file.csv --table schema.table-name --environment PROD`


```
mssql-import [-h] -f FILENAME -t TABLE [-e {TEST,PROD}] [-n] [-d] [-v] [--day_first] [--month_first]

Clean and verify CSV file, import to a temporary table and merge the temporary table with destination
table. If the source file includes dates the format must be declared with either --month_first or
--day_first (version: 0.28)

optional arguments:
  -h, --help            show this help message and exit

  -f FILENAME, --filename FILENAME
                        path and filename of the CSV file for import
                        
  -t TABLE, --table TABLE
                        destination schema and table name
                        
  -e {TEST,PROD}, --environment {TEST,PROD}
                        destination database environment as configured in the .env
                        file. Defaults to 'TEST'
                        
  -n, --dry_run         run through import process but don't commit the changes
  
  -d, --delimiter       the character used to separate fields in the source file. Defaults to -d ','
                        The other commonly used delimiter is a pipe: -d '|'
  
  -v --verbose          increase the verbosity of the log output
  
  --day_first           source date formatted with day before month: 31/03/2020 or 2020/31/03
  
  --month_first         source date formatted with month before day: 03/31/2020 or 2020/03/31

```


## Secrets
This command-line application uses the following environment variables
to determine the database name, database server, username etc. 

```
TEST_DB_HOST=
TEST_DB_NAME=
TEST_DB_USERNAME=
TEST_SHARE_LOCAL=H:\
TEST_SHARE_DB=\\SERVER\SHARE


PROD_DB_HOST=
PROD_DB_NAME=
PROD_DB_USERNAME=
PROD_SHARE_LOCAL=I:\
PROD_SHARE_DB=\\SERVER\SHARE

```

Save the
`.env` file in a directory located above where the executable is installed. 
Within Windows use `where mssql-import` to locate the executable.
