import pandas as pd
import logging
## from datetime import datetime, timedelta
## from dateutil.relativedelta import relativedelta
## from urllib.parse import quote
import requests

from utils import read_yaml
from utils_streamlit import streamlit_error_stop
## from data_processing.business_loans.business_loans import business_loans_fn
## from pd_data_frame_checks import check_columns_existence, convert_columns_dict_type_allocation, column_adjustments
## from utils_dataframe_calcs import new_calculated_column

logger = logging.getLogger(__name__)

from urllib.parse import urlparse

def extract_filename(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract the path component and then take the last part after splitting by '/'
    path = parsed_url.path
    filename = path.split('/')[-1]
    
    # Some URLs may include parameters that are not part of the file name, so we remove them
    filename = filename.split('?')[0]

    return filename

def load_file_from_url():

    # Get the URL address
    url = 'https://www.rba.gov.au/statistics/tables/xls/f01d.xls?v=2024-02-19-18-18-28'

    # Extract the file name form the URL
    file_name = extract_filename(url)

    try:
        # Attempt to load URL xlsx
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception if there is an error

        # Write the date to the file
        with open(file_name, 'wb') as f:
            f.write(response.content)

        logger.debug(f"File downloaded successfully! file_name:{file_name}")
    except requests.exceptions.HTTPError as e:        
        # Display an error message and stop the app
        error_text = f"Failed to download the file due to an HTTP error: {e}"
        logger.info(error_text)
        streamlit_error_stop(error_text=error_text)

    except Exception as e:
        # Anotehr error occured
        error_text = f"An unexpected error occurred: {e}. Using alternative file."
        logger.info(error_text)
        streamlit_error_stop(error_text=error_text)
    
    return file_name
    

## def read_and_process_data(
##         config_dict,
##         file_name,
##         date_column,
## ):
##     # Read the Excel file into a DataFrame
##     df = pd.read_excel(
##         io=file_name,
##         sheet_name=config_dict['file_loading_details']['sheet_name'],
##         skiprows=config_dict['file_loading_details']['skiprows'],
##     )
## 
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
##     return df
## 
## 
## def data_loader():
##     logger.debug("Executing: data_loader")
## 
##     # Load file from URL
##     file_name=load_file_from_url()
##     
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
##     logger.debug("Executed: data_loader")
##     return df, file_name
## 