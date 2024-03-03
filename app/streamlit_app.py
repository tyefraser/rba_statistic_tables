import streamlit as st
import logging

# from generate_text import text_generator
from utils import read_yaml, create_directory
from utils import app_item_absolute_path, repo_item_absolute_path
from utils_logging import setup_logging, close_log_handlers
from data_loading.data_loading import data_loader
# from app.charting.generate_charts import charts_generator
# from grouped_analysis.grouped_analysis import grouped_analysis
from single_column_charter import single_column_charting
from app_displays.interest_rates_and_yields_money_market_daily_f1 import (
    interest_rates_and_yields_money_market_daily_f1
)

# Apply Yaml app settings
st.set_page_config(layout="wide")

# Setup logging
close_log_handlers()
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Start of Streamlit App.")

st.title("Chartings")
st.markdown("This app lets you chart a number of key financial market indicators.")

# Setup folder locations
dataset_yamls_folder = app_item_absolute_path('data_loading/dataset_yamls')
data_folder = repo_item_absolute_path('data')
create_directory(data_folder)
outputs_folder = repo_item_absolute_path('outputs')
create_directory(outputs_folder)

# Read yaml for options to display
dataset_options_yaml = read_yaml(app_item_absolute_path('data_loading/dataset_options.yaml'))

# Select what data to look at
options_list = list(dataset_options_yaml.keys())
selected_dataset_yaml_list = st.selectbox(
    'Data Set',
    options_list,
    index=options_list.index(options_list[0])
)

# Download the required data
data_dict = data_loader(
    dataset_yamls_folder=dataset_yamls_folder,
    dataset_yaml_name_list=dataset_options_yaml[selected_dataset_yaml_list]['required_data'],
    data_folder=data_folder,
)
# st.write(data_dict)

# Analyse Data
single_col_charts_dict = single_column_charting(
        data_dict=data_dict,
        selected_dataset=selected_dataset_yaml_list
)


# Display the selected dataset
if selected_dataset_yaml_list == 'Interest Rates and Yields – Money Market – Daily – F1':
    interest_rates_and_yields_money_market_daily_f1(
        single_col_charts_dict=single_col_charts_dict
    )


close_log_handlers()
