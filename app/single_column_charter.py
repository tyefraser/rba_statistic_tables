import os
import logging
import pickle

from utils import read_yaml, get_pickle_dict_file, repo_absolute_path, get_nested_data
from utils import find_dates_or_earlier
from utils_charting import single_line_chart

logger = logging.getLogger(__name__)


def single_column_charter(
        data_dict,
        selected_dataset,
):
    # Initiate dict to return
    single_column_chart_dict = {}

    # Get months dict for use in analysis
    months_dict = read_yaml(os.path.join(
        repo_absolute_path(),
        'config',
        'settings.yaml'
    ))['months_dict']

    # Get single col charts yaml and dict
    single_col_charts_yaml_path = os.path.join(
        repo_absolute_path(),
        'config',
        'single_column_graphs_dated.yaml'
    )
    single_column_graphs_dated_dict = read_yaml(single_col_charts_yaml_path)[selected_dataset]

    # Loop through all of the dataframes required:
    for _, df_dict in single_column_graphs_dated_dict.items():
        # Get the details from the dictionary
        df = get_nested_data(data_dict, df_dict['keys']).copy()
        date_col = df_dict['date_col']

        # Loop through the columns to be graphed
        for col_title in df_dict.keys():
            if col_title not in ['keys', 'date_col']:
                single_column_chart_dict[col_title] = {}
                col_dict = df_dict[col_title]
                y_column = col_dict['y_column']
                graphing_dict = col_dict['graphing_dict']

                # Filter for only the folumns need
                df_filtered = df[[date_col, y_column]].copy()

                # remove any nas from data
                df_filtered_cleaned = df_filtered.dropna()

                # Determine time periods to analyse
                dates_dict = find_dates_or_earlier(
                    series=df_filtered_cleaned[date_col],
                    months=list(months_dict.keys()),
                )

                for month, date in dates_dict.items():
                    if month != 'latest_date':  # Skip 'latest_date' key if present
                        if date is not None:  # Ensure date is not None before filtering
                            df_filtered_cleaned_dated = df_filtered_cleaned[
                                df_filtered_cleaned[date_col] >= date]

                            # Generate chart
                            single_column_chart_dict[col_title][month] = single_line_chart(
                                data_frame=df_filtered_cleaned_dated,
                                x=date_col,
                                y=y_column,
                                **graphing_dict
                            )

    return single_column_chart_dict


def single_column_charting(
        data_dict,
        selected_dataset,
):
    logger.info("Executing: single_column_charting")

    # Read existing single_col_charts_dict
    single_col_charts_pickle_path = os.path.join(
        repo_absolute_path(),
        'data',
        'processed',
        'single_col_charts.pkl'
    )
    single_col_charts_dict = get_pickle_dict_file(
        pickle_dict_file_path=single_col_charts_pickle_path
    )

    # Add new charts if required
    if selected_dataset not in single_col_charts_dict.keys():
        # Create dictionary to add to
        single_col_charts_dict[selected_dataset] = single_column_charter(
            data_dict,
            selected_dataset,
        )

    # Save data_dict to a pickle file for future useage
    with open(single_col_charts_pickle_path, 'wb') as file:
        pickle.dump(single_col_charts_dict, file)

    return single_col_charts_dict
