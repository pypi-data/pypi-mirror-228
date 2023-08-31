import pandas as pd

def get_excel_data_from_column(file_path, sheet_name, target_column):
    # Load spreadsheet
    xl = pd.ExcelFile(file_path)
    # Check if the sheet exists in the Excel file
    if sheet_name in xl.sheet_names:
        # Load the specific sheet into a DataFrame
        df = xl.parse(sheet_name)
    else:
        print(f'Sheet {sheet_name} does not exist in the Excel file')
        return None
    # Check if target_column exists in dataframe columns
    if target_column in df.columns:
        # Return the data from the specific column as a list
        return df[target_column].values.tolist()
    else:
        print(f'Column {target_column} does not exist in the Excel file')
        return None


def get_excel_data_object(file_path, sheet_name):
    # Load spreadsheet
    xl = pd.ExcelFile(file_path)
    # Check if the sheet exists in the Excel file
    if sheet_name in xl.sheet_names:
        # Load the specific sheet into a DataFrame
        df = xl.parse(sheet_name)
    else:
        logger.info(f'Sheet {sheet_name} does not exist in the Excel file')
        return None
    # Create a dictionary where the key is the column name and the value is a list of the column values
    data_dict = df.to_dict('list')
    return data_dict


def extract_excel_data_from_row(filename, sheet_name, search_value):
    # Read the Excel file into a DataFrame skipping the first row (assuming it's a header)
    df = pd.read_excel(filename, sheet_name=sheet_name, skiprows=1)
    print(f"Searching for: {search_value}")
    # Loop through the dataframe to find the search_value
    for i, row in df.iterrows():
        for j, value in enumerate(row):
            if value == search_value:
                print(
                    f"Found {search_value} at row {i + 2}, column {j + 1}")  # +2 since we're skipping a row and pandas is 0-indexed
                # Extract all values to the right of the matched value in the same row
                data_to_right = row.iloc[j + 1:].tolist()
                return data_to_right

    print(f"{search_value} not found in the Excel sheet.")
    return None
