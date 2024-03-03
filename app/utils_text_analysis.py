def percentage_analysis(
        df,
        date_col,
        y_column,
        month,
        months_dict,
):
    txt_dict = {}
    start_rate = df[y_column].iloc[0]
    end_rate = df[y_column].iloc[-1]

    txt_dict['start_to_end'] = (
        f"Over the past {months_dict[int(month)]} the {y_column} has moved from " +
        f"{'{:.2%}'.format(start_rate)} to {'{:.2%}'.format(end_rate)}"
    )
     
    return txt_dict['start_to_end']


def text_analysis(
        df,
        date_col,
        y_column,
        month,
        months_dict,
        analysis_type,
):
    
    if analysis_type == 'percentage':
        return percentage_analysis(
            df=df,
            date_col=date_col,
            y_column=y_column,
            month=month,
            months_dict=months_dict,
        )
