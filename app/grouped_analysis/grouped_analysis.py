from app.utils_charting import single_line_chart
from utils import get_nested_data
from utils_text_analysis import text_analysis
from utils import find_dates_or_earlier


def single_variable_analysis(
        data_dict,
        grouping_dict,
):
    # Initiate return dictionary
    singles_dict = {}

    # Loop through all single column data required
    for single_column_title, col_dict in grouping_dict['single_columns'].items():
        single_column_title_dict = {}

        # Get the details from the dictionary
        months_dict = grouping_dict['months']
        df = get_nested_data(data_dict, col_dict['df_keys']).copy()
        date_col = col_dict['date_col']
        y_column = col_dict['y_column']
        graphing_dict = col_dict['graphing_dict']

        # Clean df
        df_filtered = df[[date_col, y_column]]
        df_cleaned = df_filtered.dropna()

        # Determine time periods to analyse
        dates_dict = find_dates_or_earlier(
            series=df_cleaned['Date'],
            months=list(months_dict.keys()),
        )

        for month, date in dates_dict.items():
            if month != 'latest_date':  # Skip 'latest_date' key if present
                if date is not None:  # Ensure date is not None before filtering
                    filtered_df = df_cleaned[df_cleaned[date_col] <= date]

                    # Create dictionary for the month
                    single_column_title_dict[month] = {}

                    # Generate chart
                    single_column_title_dict[month]['fig'] = single_line_chart(
                        data_frame=filtered_df,
                        x=date_col,
                        y=y_column,
                        **graphing_dict
                    )

                    # Generate Text
                    single_column_title_dict[month]['text_dict'] = text_analysis(
                        df=filtered_df,
                        date_col=date_col,
                        y_column=y_column,
                        month=month,
                        months_dict=months_dict,
                        analysis_type=col_dict['analysis_type'],
                    )

                else:
                    print(f"No date found for {month}.")
        
        singles_dict[single_column_title] = single_column_title_dict

    return singles_dict


def grouped_analysis(
        data_dict,
        grouping_dict,
):
    grouped_analysis_dict = {}

    grouped_analysis_dict.update(single_variable_analysis(
        data_dict,
        grouping_dict,
    ))

    return grouped_analysis_dict
