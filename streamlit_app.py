import streamlit as st
import pandas as pd
import logging
import os
from pathlib import Path

from utils import read_yaml, absolute_path, create_directory
from utils_logging import setup_logging, close_log_handlers
from data_loading import data_loader
from generate_charts import charts_generator

# Apply Yaml app settings
st.set_page_config(layout="wide")

# Setup logging
close_log_handlers()
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Start of Streamlit App.")

# Function to read CSS and inject it into the Streamlit app
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load your CSS file
load_css('styles.css')

st.title("Chartings")
st.markdown(f"This app lets you chart a number of key financial market indicators.")


# Setup folder locations
dataset_yamls_folder = absolute_path('dataset_yamls')
data_folder = absolute_path('data')
create_directory(data_folder)
outputs_folder = absolute_path('outputs')
create_directory(outputs_folder)

# Read yaml for options to display
dataset_options_yaml = read_yaml('dataset_options.yaml')

# Select what data to look at
options_list = list(dataset_options_yaml.keys())
selected_dataset_yaml_list = st.selectbox(
    'Data Set',
    options_list,
    index=options_list.index(options_list[0])
)

# Download the required data
data_dict = data_loader(
    dataset_yamls_folder = dataset_yamls_folder,
    dataset_yaml_name_list = dataset_options_yaml[selected_dataset_yaml_list],
    data_folder = data_folder,
)
st.write(data_dict)

# Generate Charts
tf_line_chart_dict = {
    'title': 'Annualised Interest Rates for BABs/NCDs',
    'dale_column': 'Date',
    'lines_dict': {
        'EOD 1-month BABs/NCDs': '#43B7C2',
        'EOD 3-month BABs/NCDs': '#024B79',
        'EOD 6-month BABs/NCDs': '#FFAD48',
    },
}
tf_line_chart_dict

# Title
tf_chart_design_dict={
    'title_dict': {
        # Title should already be defined
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'color': '#1E3A2F',
            'size': 40,
            'family': "Avenir Next LT Pro Demi",
        }
    },
}

charts_dict = charts_generator(
    data_dict = data_dict,
    tf_chart_design_dict = tf_chart_design_dict,
    tf_line_chart_dict = tf_line_chart_dict,
)
st.plotly_chart(charts_dict['babs_ncds_chart'], use_container_width=True)

# Generate Text values
from generate_text import text_generator
text_generator(data_dict=data_dict)

# Load teh tabs

close_log_handlers()