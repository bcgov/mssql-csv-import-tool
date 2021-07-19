import pytest
import src.helper as helper
import src.business as business
import src.database as database
from src.config import Config


@pytest.fixture()
def some_fixture(monkeypatch, tmpdir):
    monkeypatch.setattr(database, "get_database_connection", lambda **args: (True, args))
    monkeypatch.setattr(database, "get_destination_table_schema", lambda **args: (True, args))
    monkeypatch.setattr(database, "get_destination_primary_keys", lambda **args: (True, args))
    # These tests are interested only in the '_clean' CSV file created.
    # Returning 'False' from create_temporary_table() below causes script to stop early.
    monkeypatch.setattr(database, "create_temporary_table", lambda **args: (False, args))

    filename = "test.csv"
    temp_directory = tmpdir.mkdir('subdirectory')
    input_file = temp_directory.join(filename)

    class TestConfig(Config):
        TEST_SHARE_LOCAL = str(temp_directory) + '/'

    return input_file, TestConfig


def test_two_column_input_file_creates_two_column_clean_file(some_fixture, tmpdir):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write("COL_1,COL_2\nvalue1,value2")

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        assert clean_text == "COL_1|COL_2\nvalue1|value2\n"


def test_input_file_with_lowercase_header_correctly_identifies_column_names(some_fixture, tmpdir):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write("col_1,col_2\nvalue1,value2")

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        assert clean_text == "COL_1|COL_2\nvalue1|value2\n"


def test_input_file_with_delimiter_wrapped_in_quotes_is_correctly_converted(some_fixture, tmpdir):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '10',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '10',
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write('COL_1,COL_2\n"value1","value2,3"')

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        assert clean_text == "COL_1|COL_2\nvalue1|value2,3\n"


def test_input_file_with_ambiguous_date_format_correctly_converts_date(some_fixture, tmpdir):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "date",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write('COL_1,COL_2\n"value1","03/01/21"')

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file,
                        day_first=True)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        assert clean_text == "COL_1|COL_2\nvalue1|2021-01-03\n"


def test_error_shown_if_file_includes_a_date_column_but_date_format_not_declared(some_fixture, tmpdir, caplog):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "date",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write('COL_1,COL_2\n"value1","03/01/21"')

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file,
                        day_first=None)  # <-- date format not set
    assert 'date format not set' in caplog.text


def test_database_must_return_uppercase_column_names(some_fixture, tmpdir, caplog):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "lowercase": {
            "COLUMN_NAME": "lowercase",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write('LOWERCASE,COL_2\n"value1","value2"')

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        assert clean_text == "COL_2\nvalue2\n"
    assert 'cannot be found in schema.table: LOWERCASE (col 1)' in caplog.text


def test_not_all_database_fields_need_to_be_imported(some_fixture, tmpdir):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        },
        "COL_3": {
            "COLUMN_NAME": "COL_3",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write('COL_1,COL_2\n"value1","value2"')

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        # Note: COL_3 is not not included in the import
        assert clean_text == "COL_1|COL_2\nvalue1|value2\n"


def test_when_import_file_includes_columns_without_a_db_match_a_warning_is_shown(some_fixture, tmpdir, caplog):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write('COL_1,MISSING_COLUMN\n"value1","value2"')

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        # Note: COL_3 is not not included in the import
        assert clean_text == "COL_1\nvalue1\n"
    assert 'cannot be found in schema.table: MISSING_COLUMN (col 2)' in caplog.text


def test_source_file_can_be_delimited_by_pipes_instead_of_commas(some_fixture, tmpdir):
    input_file, config = some_fixture
    database_returns_this_schema = {
        "COL_1": {
            "COLUMN_NAME": "COL_1",
            "DATA_TYPE": "varchar",
            "CHARACTER_MAXIMUM_LENGTH": '7',
            "IS_NULLABLE": ""
        },
        "COL_2": {
            "COLUMN_NAME": "COL_2",
            "DATA_TYPE": "date",
            "CHARACTER_MAXIMUM_LENGTH": None,
            "IS_NULLABLE": ""
        }
    }
    with open(input_file, 'w') as file:
        file.write("col_1|col_2\nvalue1|2021-04-03")

    helper.middle_logic(business.clean_and_verify_csv(),
                        is_verbose=False,
                        delimiter="|",
                        destination_schema=database_returns_this_schema,
                        config=config,
                        destination_table='schema.table',
                        is_dry_run=True,
                        environment='TEST',
                        filename=input_file,
                        day_first=True)
    with open(str(input_file) + '_clean', 'r') as clean_file:
        clean_text = clean_file.read()
        assert clean_text == "COL_1|COL_2\nvalue1|2021-04-03\n"

