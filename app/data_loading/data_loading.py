import pandas as pd
import logging
from pathlib import Path
import time
# import numpy as np
import os
from typing import Union, Optional, Tuple, List, Dict
from pandas import DataFrame
import pickle
# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
# from urllib.parse import quote
from utils import read_yaml, get_pickle_dict_file
import requests
from urllib.parse import urlparse


# from utils_streamlit import streamlit_error_stop
# from data_processing.business_loans.business_loans import business_loans_fn
# from pd_data_frame_checks import check_columns_existence, convert_columns_dict_type_allocation
# column_adjustments
# from utils_dataframe_calcs import new_calculated_column

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


def load_file_from_url(
    url: str,
    data_folder: Union[str, Path],
    file_name: str = '',
    max_retries: int = 5,
    retry_delay: int = 2,
) -> Path:
    """
    Downloads a file from a given URL and saves it to a specified directory with retry logic.

    Args:
        url (str): The URL from which to download the file.
        data_folder (Union[str, Path]): The directory path where the file will be saved.
        file_name (str, optional): The name of the file. If not provided, the name is extracted
        from the URL.
        max_retries (int, optional): Maximum number of retries if the download fails.
        retry_delay (int, optional): Delay in seconds between retries.

    Returns:
        Path: The path to the downloaded file.

    Raises:
        Exception: If the file cannot be downloaded after the specified number of retries.
    """
    if not file_name:
        file_name = extract_filename(url)

    file_path = Path(data_folder) / 'raw' / file_name

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses

            # Write the data to the file
            with open(file_path, 'wb') as f:
                f.write(response.content)

            logger.debug(f"File downloaded successfully! file_name: {file_path}")
            return file_path  # Success, return the path to the downloaded file
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} " +
                           "seconds...")
            time.sleep(retry_delay)
    # All attempts failed, raise an exception
    error_text = f"Failed to download the file after {max_retries} attempts."
    logger.error(error_text)
    raise Exception(error_text)


def read_xls_with_header(
        file_path: Path,
        dataset_yaml_dict: Dict
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reads an Excel file (.xls or .xlsx), separating extended header information from the actual
    data.

    This function handles Excel files where the initial rows serve as extended header information,
    followed by tabular data. The first row of headers within the data is treated as column names.
    Rows between the first row and the start of the data are converted into a reference DataFrame.
    The actual data is read into a separate DataFrame.

    Args:
        file_path (Path): The path to the Excel file.
        dataset_yaml_dict (Dict): Configuration specifying parameters such as:
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
        sheet_name=dataset_yaml_dict['sheet_name'],
        header=None,  # Read without using the first row as header
        skiprows=dataset_yaml_dict.get('skiprows', 0),  # Use 'skiprows' from dataset_yaml_dict if
        # provided
        engine=engine,
    )

    # Correctly find the start of data based on a unique identifier
    start_of_data_idx = sheet_df[sheet_df.iloc[:, 0] == dataset_yaml_dict[
        'table_header_id']].index[0]

    # Correctly process header descriptions
    header_df = sheet_df.iloc[:start_of_data_idx].dropna(subset=[0])  # Correct subset reference
    header_df = header_df.T  # Transpose
    header_df.columns = header_df.iloc[0]  # Set the first row as column headers
    header_df = header_df[1:].reset_index(drop=True)  # Drop the first row and reset index

    # Prepare the data DataFrame
    original_df = sheet_df.iloc[start_of_data_idx + 1:].reset_index(drop=True)
    original_df.columns = sheet_df.iloc[0].values
    original_df = original_df[1:]  # Skip the header row now used for column names
    original_df.rename(columns=dataset_yaml_dict.get('convert_headers', {}), inplace=True)

    return header_df, original_df


def clean_df(
    header_descriptions_df: DataFrame,
    original_df: DataFrame,
    date_column: str = 'Date',
    units_column: str = 'Units',
    col_name_id: str = 'Title',
) -> DataFrame:
    """
    Cleans and transforms an original DataFrame based on configurations defined in a header
    descriptions DataFrame.

    Parameters:
    - header_descriptions_df: DataFrame containing column units and titles.
    - original_df: DataFrame with the data to be cleaned.
    - date_column: Name of the column in original_df containing dates.
    - units_column: Name of the column in header_descriptions_df containing unit types.
    - col_name_id: Identifier for accessing columns in original_df to apply transformations based
    on unit types.

    Returns:
    - DataFrame: The cleaned and transformed DataFrame.
    """
    # Ensure a copy is made to avoid modifying the original DataFrame unexpectedly
    cleaned_df = original_df.copy()

    # Convert Date column to datetime
    cleaned_df[date_column] = pd.to_datetime(cleaned_df[date_column])

    # Order table by date and reset index
    cleaned_df.sort_values(by=date_column, inplace=True)
    cleaned_df.reset_index(drop=True, inplace=True)

    # Prepare for column transformations based on units
    transformations = {
        'Per cent': lambda x: x.astype(float) / 100,
        'Index 04-Jan-2011=100': lambda x: x.astype(float) / 100,
        '$m': lambda x: x.astype(float) * 1_000_000,
        'Number ': lambda x: x.astype(float),
    }

    # Apply transformations based on unit types
    for _, row in header_descriptions_df.iterrows():
        unit = row[units_column]
        col_name = row[col_name_id]  # Assuming this is meant to specify which column to transform

        if unit in transformations:
            cleaned_df[col_name] = transformations[unit](cleaned_df[col_name])
        else:
            print(f"No transformation defined for unit: {unit}")

    return cleaned_df


def read_file_as_df(
        file_path,
        dataset_yaml_dict,
):
    # Read in data from file
    if dataset_yaml_dict['file_reader'] == 'read_xls_with_header':
        header_descriptions_df, original_df = read_xls_with_header(
            file_path,
            dataset_yaml_dict,
        )

    # Clean the data
    cleaned_df = clean_df(
        header_descriptions_df=header_descriptions_df,
        original_df=original_df,
        date_column=dataset_yaml_dict['date_column'],
        units_column=dataset_yaml_dict['units_column'],
        col_name_id=dataset_yaml_dict['col_name_id'],
    )

    return header_descriptions_df, cleaned_df


def check_columns_existence(
        df: DataFrame,
        target_columns: Union[List[str], str]
) -> bool:
    """
    Verifies if specified columns exist in a DataFrame.

    This function checks if each column listed in target_columns is present in the DataFrame's
    columns.
    If a column is missing, a warning is logged. The function returns a boolean indicating whether
    all
    target columns exist in the DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame to check for column existence.
    - target_columns (Union[List[str], str]): A list of strings representing the names of the
    columns
      to check for existence. A single column name can also be passed as a string.

    Returns:
    - bool: True if all target columns exist in the DataFrame, False otherwise.
    """
    # Ensure target_columns is a list even if a single column name is provided
    if isinstance(target_columns, str):
        target_columns = [target_columns]

    missing_columns = [column for column in target_columns if column not in df.columns]

    # Log warnings for missing columns
    for column in missing_columns:
        logger.warning(f"'{column}' is an expected column but does not exist in the DataFrame.")

    # Return False if any columns are missing, True otherwise
    return not missing_columns


def df_data_quality_checks(
        df,
        dataset_yaml_dict
):
    # Check expected columns exist
    check_columns_existence(
         df=df,
         target_columns=dataset_yaml_dict['expected_columns']
    )


def dataset_dict(
        dataset_yaml_dict,
        data_folder,
):
    """
    Create the dictionary for the dataset defined in the yaml provided
    """
    logger.debug('Executing: dataset_dict')
    create_dataset_dict = {}

    # File url and return the file path
    if 'file_url' in dataset_yaml_dict.keys():
        # Download file from url if required
        # Load file from URL
        create_dataset_dict['file_path'] = load_file_from_url(
            url=dataset_yaml_dict['file_url'],
            data_folder=data_folder,
        )

    # Generate df from file
    (
        create_dataset_dict['header_descriptions_df'],
        create_dataset_dict['cleaned_df'],
    ) = read_file_as_df(
        file_path=create_dataset_dict['file_path'],
        dataset_yaml_dict=dataset_yaml_dict,
    )

    # Perform DQ checks
    df_data_quality_checks(
        df=create_dataset_dict['cleaned_df'],
        dataset_yaml_dict=dataset_yaml_dict,
    )

    logger.debug('Executed: dataset_dict')
    return create_dataset_dict


def data_loader(
        dataset_yamls_folder,
        dataset_yaml_name_list,
        data_folder,
):
    logger.info("Executing: data_loader")

    # Set the data_dict file path location
    data_dict_pickle_file_path = os.path.join(data_folder, 'processed/data_dict.pkl')
    logger.debug(f"data_dict_pickle_file_path:{data_dict_pickle_file_path}")
    # TO DO: If loading takes too long, consider spliting into separate dictionaries and loading
    # each individually.

    # Get the existing data_dict
    data_dict = get_pickle_dict_file(data_dict_pickle_file_path)
    logger.debug(f"data_dict from get_pickle_dict_file read in. Keys: {data_dict.keys()}")

    # Loop through all of the dataset yamls required
    logger.debug(f"dataset_yaml_list:{dataset_yaml_name_list}")
    for dataset_yaml_name in dataset_yaml_name_list:
        logger.debug(f"dataset_yaml_name:{dataset_yaml_name}")

        # Get the name of the dataset
        dataset = dataset_yaml_name[:dataset_yaml_name.rfind('.')]
        logger.debug(f"dataset:{dataset}")
        dataset_yaml_dict = read_yaml(os.path.join(dataset_yamls_folder, dataset_yaml_name))
        logger.debug(f"dataset_yaml_dict:{dataset_yaml_dict}")

        # If data doesnt exists, download it
        if dataset not in data_dict.keys():
            data_dict[dataset] = dataset_dict(
                dataset_yaml_dict=dataset_yaml_dict,
                data_folder=data_folder,
            )

    # Save data_dict to a pickle file for future useage
    with open(data_dict_pickle_file_path, 'wb') as file:
        pickle.dump(data_dict, file)

    logger.info("Executed: data_loader")
    return data_dict
