import pandas as pd

def compare_differences(csv_file1, csv_file2, uid_col_str, output_file_name, delete_null_rows=False, delete_null_cols=False):
    
    ansi = {
        "red": '\033[31m', # red
        "red_b": '\033[1m\033[31m', # red and bold
        "grn": '\033[32m', # green
        "grn_b": '\033[1m\033[32m', # green and bold
        "ylw": '\033[33m', # brown/yellow
        "end": '\033[0m' # terminate coloring
        }

    print(f'{ansi["ylw"]}' + f'\nComparing two CSV Files:\n‣ {csv_file1}\n‣ {csv_file2}\n ⭑ Preserving the "{uid_col_str}" column.\n' + f'{ansi["end"]}')
    df1 = pd.read_csv(csv_file1, low_memory=False)
    df2 = pd.read_csv(csv_file2, low_memory=False)

    # Get column number of uid_col_str
    print(f'{ansi["ylw"]}' + f'Retrieving the column number of "{uid_col_str}".' + f'{ansi["end"]}')
    uid_col_num = df1.columns.get_loc(uid_col_str)
    print(f'{ansi["grn"]}' + f'✔ Retrieved. "{uid_col_str}" is in column no. {uid_col_num}.\n' + f'{ansi["end"]}')

    
    # sort by 'uid_col_str'
    print(f'{ansi["ylw"]}' + f'Aligning rows of the dataframes by "{uid_col_str}" by sorting in ascending order.' + f'{ansi["end"]}')
    df1 = df1.sort_values(by=[uid_col_str], axis=0, ascending=True, ignore_index=True)
    df2 = df2.sort_values(by=[uid_col_str], axis=0, ascending=True, ignore_index=True)
    print(f'{ansi["grn"]}' + f'✔ Successfully sorted by "{uid_col_str}".\n' f'{ansi["end"]}')

    # Copy the column 'uid_col_str'
    df1_uid_cols_data = df1[uid_col_str].copy()

    # Drop the 'uid_col_str' column from the current data frames before comparing.
    df1.drop(uid_col_str, axis=1, inplace=True)
    df2.drop(uid_col_str, axis=1, inplace=True)

    # Find the differences between the two dataframes. Fill any NaN values with '.'
    try:
      print(f'{ansi["ylw"]}' + 'Comparing differences between both dataframes.' + f'{ansi["end"]}')
      difference = df1[df1!=df2]
      # Add the 'uid_col_str' column back to the dataframe.
      difference.insert(uid_col_num, uid_col_str, df1_uid_cols_data)
      print(f'{ansi["grn"]}' + '✔ Comparison completed. New dataframe positing differences created.\n' + f'{ansi["end"]}')
    except ValueError as err:
      print(f'{ansi["red_b"]}' + f'\n ValueError: {err}.' + f'{ansi["end"]}\n')
      return None
      
    # Drop any row that has less than 2 non-null values, or all `NaN` values
    if(delete_null_rows is True):
      print(f'{ansi["ylw"]}' + f'Dropping any rows that only contain the "{uid_col_str}" as a non-null value.' + f'{ansi["end"]}')
      difference = difference.dropna(thresh=2)
      print(f'{ansi["grn"]}' + '✔ Successfully dropped target rows.\n' + f'{ansi["end"]}')
    elif(delete_null_rows is False):
      print(f'{ansi["grn"]}' + 'Option to delete rows with all null values set to False. Set to True to delete these rows. \n' + f'{ansi["end"]}')
    
    # Dropping any columns with all NaN values
    if(delete_null_cols is True):
      print(f'{ansi["ylw"]}' + f'Dropping any columns that contain all null values.' + f'{ansi["end"]}')
      difference = difference.dropna(axis=1, how='all')
      print(f'{ansi["grn"]}' + '✔ Successfully dropped target columns.\n' + f'{ansi["end"]}')
    elif(delete_null_cols is False):
      print(f'{ansi["grn"]}' + 'Option to delete columns with all null values set to False. Set to True to delete these columns. \n' + f'{ansi["end"]}')
    
    
    # Fill any remaining 'NaN' cells with '.'
    difference = difference.fillna(value='.')

    # Set options so it doesn't truncate
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    
    # Export to a CSV file. Do not print the row numbers. Use df1's column headers.
    print(f'{ansi["ylw"]}' + f'Exporting final output file to {output_file_name}.csv.' + f'{ansi["end"]}')
    difference.to_csv(f'{output_file_name}.csv', index=False)
    print(f'{ansi["grn"]}' + f'✔ The program has successfully exported "{output_file_name}.csv"\n' + f'{ansi["end"]}')
    print(f'{ansi["grn_b"]}' + 'The comparison program has completed.\n' + f'{ansi["end"]}')
    

compare_differences(
    # First file name to compare. Can include just file name if in local folder. Else, provide path to file.
    'Daily_Diamond_Price_Input_20230302_013126.csv',
    # Second file name to compare. Can include just file name if in local folder. Else, provide path to file.
    'Daily_Diamond_Price_Output_20230302_013126.csv',
    # UUID Column to protect
    'Stock Number',
    # File Name
    '2023-03-02-differences-sheet',
    # Options
    # Delete all-null rows: True to delete all rows that contain all null values. False to keep all rows. False is default.
    True,
    # Delete all-null columns: True to delete all columns that contain all null values. False to keep all columns. False is default.
    True
)