import pandas as pd
import logging
from pathlib import Path
import numpy as np
import os
from typing import Union, Optional, Tuple, Dict
## from datetime import datetime, timedelta
## from dateutil.relativedelta import relativedelta
## from urllib.parse import quote
import requests
from urllib.parse import urlparse


from utils_streamlit import streamlit_error_stop
## from data_processing.business_loans.business_loans import business_loans_fn
## from pd_data_frame_checks import check_columns_existence, convert_columns_dict_type_allocation, column_adjustments
## from utils_dataframe_calcs import new_calculated_column

logger = logging.getLogger(__name__)

def extract_filename(url: str) -> Optional[str]:
    """
    Extracts the filename from a given URL.

    This function parses the URL to extract the path component, then isolates
    the filename by taking the last segment after splitting the path by '/'. It
    also handles cases where the URL may include query parameters or fragments
    that are not part of the filename, removing them accordingly.

    Args:
        url (str): The URL from which to extract the filename.

    Returns:
        Optional[str]: The extracted filename, or None if no filename is found.
    """
    # Parse the URL to extract its components
    parsed_url = urlparse(url)
    
    # Extract the path component and then take the last part after splitting by '/'
    path = parsed_url.path
    filename = path.split('/')[-1]
    
    # Handle URLs with parameters or fragments that are not part of the filename
    filename = filename.split('?')[0].split('#')[0]

    # Return None if the filename is empty, indicating no actual file was specified in the URL
    return filename if filename else None

def extract_filename(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract the path component and then take the last part after splitting by '/'
    path = parsed_url.path
    filename = path.split('/')[-1]
    
    # Some URLs may include parameters that are not part of the file name, so we remove them
    filename = filename.split('?')[0]

    return filename

def load_file_from_url(
        url: str,
        data_folder: Union[str, Path],
        file_name: str = ''
) -> Path:
    """
    Downloads a file from a given URL and saves it to a specified directory.

    Args:
        url (str): The URL from which to download the file.
        data_folder (Union[str, Path]): The directory path where the file will be saved.
        file_name (str, optional): The name of the file. If not provided, the name is extracted from the URL.

    Returns:
        Path: The path to the downloaded file.

    Raises:
        HTTPError: If the request to the URL fails with an HTTP error.
        Exception: For any unexpected errors during download.
    """
    # If no file name provided, extract one from the URL
    if not file_name:
        file_name = extract_filename(url)

    file_path = Path(data_folder) / file_name

    try:
        # Attempt to load URL content
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Write the data to the file
        with open(file_path, 'wb') as f:
            f.write(response.content)

        logger.debug(f"File downloaded successfully! file_name: {file_path}")
    except requests.exceptions.HTTPError as e:
        error_text = f"Failed to download the file due to an HTTP error: {e}"
        logger.error(error_text)
        raise e
    except Exception as e:
        error_text = f"An unexpected error occurred: {e}."
        logger.error(error_text)
        raise e

    return file_path

##def read_xls_with_header(
##        file_path,
##        source_yaml,
##) -> Path:
##    """
##    This will read in an xls file that has a number of rows as header information before the data starts.
##    The first header row will be taken as the actual header, the other header rows will be converted into a reference dataframe.
##    The actual data will be separated into another dataframe for used in the code.
##    """
##    # Load in the complete set of relevant data from the sheet
##    sheet_df = pd.read_excel(
##        io=file_path,
##        sheet_name=source_yaml['sheet_name'],
##        header=source_yaml['header'],
##        engine='xlrd',
##    )
##
##    # Determine where the start of the data is
##    mask = (sheet_df.iloc[:, 0] == source_yaml['table_header_id'])
##    starting_row = np.where(mask)[0][0]
##
##    # Get the headers part of the sheet_df
##    header_descriptions_df = sheet_df.iloc[1:starting_row, :] # get rows before the data starts
##    header_descriptions_df = header_descriptions_df[~header_descriptions_df.iloc[:, 0].isna()] # Remove na rows
##    header_descriptions_df = header_descriptions_df.transpose() # Transpose the DataFrame
##    header_descriptions_df.columns = header_descriptions_df.iloc[0]  # Set the first row as the column names
##    header_descriptions_df = header_descriptions_df[1:]  # Create a new DataFrame excluding the original first row
##    header_descriptions_df = header_descriptions_df.reset_index()
##    header_descriptions_df = header_descriptions_df.rename(columns={'index': 'Title'})
##    header_descriptions_df.columns.name = None
##
##    # Get the data component of the sheet_df
##    original_df = sheet_df.iloc[(starting_row+1):, :]
##    original_df.reset_index(inplace=True, drop=True)
##    for old_heading, new_heading in source_yaml['convert_headers'].items():
##        original_df.rename(columns={old_heading: new_heading}, inplace=True)
##
##    return header_descriptions_df, original_df

def read_xls_with_header(file_path: Path, source_yaml: Dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reads an Excel file (.xls or .xlsx), separating extended header information from the actual data.

    This function handles Excel files where the initial rows serve as extended header information, followed by
    tabular data. The first row of headers within the data is treated as column names. Rows between the first
    row and the start of the data are converted into a reference DataFrame. The actual data is read into a
    separate DataFrame.

    Args:
        file_path (Path): The path to the Excel file.
        source_yaml (Dict): Configuration specifying parameters such as:
                            - 'sheet_name': Name or index of the sheet to read.
                            - 'header': Row (0-indexed) to use as header.
                            - 'table_header_id': Identifier to locate the start of data.
                            - 'convert_headers': Dictionary mapping old column names to new ones.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing:
                                           - A DataFrame of header descriptions.
                                           - A DataFrame of the actual data.
    """

    # Determine engine based on file extension
    engine = 'openpyxl' if str(file_path).endswith('.xlsx') else 'xlrd'

    # Load the data set from the specified sheet without using the first row as header
    sheet_df = pd.read_excel(
        io=file_path,
        sheet_name=source_yaml['sheet_name'],
        header=None,  # Read without using the first row as header
        skiprows=source_yaml.get('skiprows', 0),  # Use 'skiprows' from source_yaml if provided
        engine=engine,
    )

    # Get headers to use
    headers = sheet_df.iloc[0]
    print(headers)

    # Correctly find the start of data based on a unique identifier
    start_of_data_idx = sheet_df[sheet_df.iloc[:, 0] == source_yaml['table_header_id']].index[0]

    # Correctly process header descriptions
    header_df = sheet_df.iloc[:start_of_data_idx].dropna(subset=[0])  # Correct subset reference
    header_df = header_df.T  # Transpose
    header_df.columns = header_df.iloc[0]  # Set the first row as column headers
    header_df = header_df[1:].reset_index(drop=True)  # Drop the first row and reset index

    # Prepare the data DataFrame
    data_df = sheet_df.iloc[start_of_data_idx + 1:].reset_index(drop=True)
    data_df.columns = sheet_df.iloc[0].values
    data_df = data_df[1:]  # Skip the header row now used for column names
    data_df.rename(columns=source_yaml.get('convert_headers', {}), inplace=True)

    return header_df, data_df


def read_file_as_df(
        # config_dict,
        file_path,
        yaml,
        # date_column,
):
    # Read in data from file
    if yaml['file_reader'] == 'read_xls_with_header':
        header_descriptions_df, original_df = read_xls_with_header(
            file_path,
            yaml,
        )

    # Read in the Series descriptors
    
    
    # Read the Excel file into a DataFrame
    # df = pd.read_excel(
    #     io=file_name,
    #     sheet_name=config_dict['file_loading_details']['sheet_name'],
    #     skiprows=config_dict['file_loading_details']['skiprows'],
    # )

##     # Sort by date column
##     df.sort_values(by=date_column, inplace=True)
## 
##     # Check expected columns exist
##     check_columns_existence(
##         df=df,
##         target_columns=config_dict['file_loading_details']['expected_columns_list']
##     )
## 
##     # Column Data Types
##     df=convert_columns_dict_type_allocation(
##         df=df.copy(),
##         col_types_dict=config_dict['column_typing_dict'],
##     )
## 
##     # Column Adjustments - convert to dollar amounts (not scalled)
##     df=column_adjustments(df, config_dict)
## 
##     df[date_column] = pd.to_datetime(df[date_column])
## 
    return header_descriptions_df, original_df
## 
## 
def data_loader(
        source_yaml,
        data_folder,
):
    logger.debug("Executing: data_loader")

    # Load file from URL
    file_name = load_file_from_url(
        url = source_yaml['url'],
        data_folder = data_folder,
    )

    # Read data as df
    # df = read_as_df()
    
## 
##     # Read config
##     config_dict = read_yaml(file_path = 'config.yaml')
##     date_column = 'Period'
## 
##     # Load data
##     file_name=load_url_xlsx()
## 
##     # Read and process data
##     df = read_and_process_data(
##         config_dict=config_dict,
##         file_name=file_name,
##         date_column=date_column,        
##     )
## 
##     # Create calculated columns
##     for new_column_name, calculations in config_dict['calculated_columns'].items():
##         df[new_column_name] = 0
##         for column_calculation in calculations:
##             calculation = column_calculation[0]
##             column = column_calculation[1]
##             df = new_calculated_column(
##                 df=df,
##                 new_column_name=new_column_name,
##                 calculation=calculation,
##                 column=column,
##             )
## 
    logger.debug("Executed: data_loader")
    return file_name
    ## return df, file_name
