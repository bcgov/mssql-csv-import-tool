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

This tool is used to import text files into RoadSafety BC Business Intelligence (BI) database.

## Prerequisites
Install `python3` from https://www.python.org/downloads/windows/

Install `git`: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

## Installation
From Windows command prompt:

`pip install git+https://github.com/bcgov/mssql-csv-import-tool.git`

`pip install git+https://github.com/bcgov/mssql-csv-import-tool.git --upgrade`


## Usage

usage: mssql-import

optional arguments:

  -h, --help            show this help message and exit

  -f, --filename FILENAME   path and filename of the file for import

  -d, --destination     Destination database schema and table name (see options below)

  -e, --environment {TEST,PROD}
                        destination database environment

  --dry_run             don't save the changes to the database

  --debug               show detailed output for debugging

destination options:
- DFCMS.document_images
- DFCMS.case_test_consultations
- DFCMS.cases
- GIS.geolocations
- ISC.tickets 
- ICBC.contraventions
- TAS.accidents
- TAS.entities
- TAS.victims
- VIPS.prohibitions
- VIPS.impoundments
- VIPS.licences


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
