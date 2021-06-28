from setuptools import setup, find_packages

setup(name='mssql-csv-import-tool',
      version='0.16',
      description='Command line tool to import CSV files to MS-SQL server',
      url='https://github.com/bcgov/mssql-csv-import-tool',
      author='Jonathan Longe',
      author_email='jonathan.longe@gov.bc.ca',
      license='MIT',
      packages=find_packages(include=['src', 'src.*', 'bin', 'bin.*']),
      setup_requires=['wheel'],
      install_requires=[
        'certifi==2021.5.30',
        'chardet==4.0.0',
        'greenlet==1.1.0',
        'idna==2.10',
        'numpy==1.20.3',
        'pandas==1.2.4',
        'pyodbc==4.0.30',
        'python-dateutil==2.8.1',
        'python-dotenv==0.17.1',
        'pytest==6.2.4',
        'pytz==2021.1',
        'requests==2.25.1',
        'six==1.16.0',
        'SQLAlchemy==1.4.17',
        'urllib3==1.26.5',
      ],
      entry_points={
        'console_scripts': ['mssql-import=bin.mssql_import:main']
      },
      zip_safe=False)
