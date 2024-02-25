from charting.utils_charting import tf_line_chart

def charts_generator(
        data_dict,
        tf_chart_design_dict,
        tf_line_chart_dict,
):
    charts_dict = {}

    charts_dict['babs_ncds_chart'] = tf_line_chart(
        data_frame = data_dict['rba_f01d']['cleaned_df'],
        x = tf_line_chart_dict['dale_column'],
        y = list(tf_line_chart_dict['lines_dict'].keys()),
        color_discrete_map=tf_line_chart_dict['lines_dict'],
        title=tf_line_chart_dict['title'],
        height=800,
        tf_title_dict=tf_chart_design_dict['title_dict'],
    )

    return charts_dict