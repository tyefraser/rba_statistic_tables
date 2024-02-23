import streamlit as st
import pandas as pd
import logging
import os
from pathlib import Path

from utils import read_yaml, absolute_path, create_directory
from utils_logging import setup_logging
from utils_logging import close_log_handlers
from data_loading import data_loader


# Setup logging
close_log_handlers()
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Start of Streamlit App.")

# Setup folder locations
yamls_folder = absolute_path('source_yamls')
data_folder = absolute_path('data')
create_directory(data_folder)
outputs_folder = absolute_path('outputs')
create_directory(outputs_folder)

# Select what data to look at
dataset_list = os.listdir('source_yamls')
selected_dataset = st.selectbox(
    'Data Set',
    dataset_list,
    index=dataset_list.index(dataset_list[0])
)
yaml_path = Path(yamls_folder) / selected_dataset
source_yaml=read_yaml(yaml_path) # TO DO: return source_yaml after checks etc.

# Load data
file_path, header_descriptions_df, cleaned_df =data_loader(
    source_yaml=source_yaml,
    data_folder=data_folder,
)

st.write(f'selected_dataset:{selected_dataset}')

close_log_handlers()