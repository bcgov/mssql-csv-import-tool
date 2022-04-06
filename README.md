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

 - Unix: `mssql-import`
 - Windows: `mssql-import.exe`

The tool opens a Windows GUI as shown in the screenshot below.

[TODO - add screenshot here]


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
