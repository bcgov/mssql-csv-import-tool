import src.database as database
import src.dataframe as dataframe
import src.file_operations as file_operations
import src.import_types as import_types


def clean_and_verify_csv() -> list:
    return [
        {"try": file_operations.set_log_level, "fail": []},
        {"try": import_types.get_import_file_attributes, "fail": []},
        {"try": database.set_environment_variables, "fail": []},
        {"try": database.prompt_for_database_password_if_not_set, "fail": []},
        {"try": database.get_database_connection_string, "fail": []},
        {"try": database.get_database_connection, "fail": []},
        {"try": database.get_destination_table_schema, "fail": []},
        {"try": database.get_destination_primary_keys, "fail": []},

        {"try": file_operations.determine_destination_filename, "fail": []},
        {"try": file_operations.delete_target, "fail": []},
        {"try": file_operations.count_rows_in_import_file, "fail": []},
        {"try": dataframe.process_csv_in_chunks, "fail": []},

        {"try": database.create_temporary_table, "fail": []},
        {"try": file_operations.wait_for_file_to_finish_writing, "fail": []},
        {"try": database.bulk_import_from_text_file, "fail": []},
        {"try": database.count_temporary_table_records, "fail": []},
        {"try": database.merge_temporary_table_into_destination, "fail": []},
        {"try": file_operations.delete_target_if_not_verbose, "fail": []},
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
        {"try": dataframe.check_date_format_set_if_date_fields_present, "fail": []},
        {"try": dataframe.check_no_not_null_fields_missing, "fail": []},
        {"try": dataframe.trim_string_values, "fail": []},
        {"try": dataframe.convert_dates, "fail": []},
        {"try": dataframe.format_numeric_values, "fail": []},
        {"try": dataframe.write_dataframe_to_file, "fail": []},
    ]


