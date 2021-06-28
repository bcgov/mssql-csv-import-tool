import src.database as database
import src.dataframe as dataframe
import src.file_operations as file_operations


def clean_and_verify_csv() -> list:
    return [
        {"try": file_operations.set_log_level, "fail": []},
        {"try": database.set_environment_variables, "fail": []},
        {"try": database.prompt_for_database_password_if_not_set, "fail": []},
        {"try": database.get_database_connection_string, "fail": []},
        {"try": database.get_database_connection, "fail": []},
        {"try": database.get_destination_table_schema, "fail": []},
        {"try": database.get_destination_primary_keys, "fail": []},

        {"try": file_operations.determine_destination_filename, "fail": []},
        {"try": file_operations.delete_target_if_exists, "fail": []},
        {"try": dataframe.process_csv_in_chunks, "fail": []},

        {"try": database.create_temporary_table, "fail": []},
        {"try": database.bulk_import_from_text_file, "fail": []},
        {"try": database.merge_temporary_table_into_destination, "fail": []},
        {"try": file_operations.delete_target_if_exists, "fail": []},
    ]


def process_dataframe() -> list:
    return [
        {"try": dataframe.uppercase_column_names, "fail": []},
        {"try": dataframe.is_first_dataframe, "fail": [
            {"try": dataframe.trim_string_values, "fail": []},
            {"try": dataframe.convert_dates, "fail": []},
            {"try": dataframe.format_numeric_values, "fail": []},
            {"try": dataframe.write_dataframe_to_file, "fail": []},
        ]},
        {"try": dataframe.check_all_csv_columns_have_matching_db_fields, "fail": []},
        {"try": dataframe.create_header_record, "fail": []},
        {"try": dataframe.get_list_of_date_columns, "fail": []},
        {"try": dataframe.check_no_not_null_fields_missing, "fail": []},
        {"try": dataframe.trim_string_values, "fail": []},
        {"try": dataframe.convert_dates, "fail": []},
        {"try": dataframe.format_numeric_values, "fail": []},
        {"try": dataframe.write_dataframe_to_file, "fail": []},
    ]


