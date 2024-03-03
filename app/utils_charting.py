import plotly_express as px


def single_line_chart(
        # Line chart
        data_frame=None,
        x=None,
        y=None,
        line_group=None,
        color=None,
        line_dash=None,
        symbol=None,
        hover_name=None,
        hover_data=None,
        custom_data=None,
        text=None,
        facet_row=None,
        facet_col=None,
        facet_col_wrap=0,
        facet_row_spacing=None,
        facet_col_spacing=None,
        error_x=None,
        error_x_minus=None,
        error_y=None,
        error_y_minus=None,
        animation_frame=None,
        animation_group=None,
        category_orders=None,
        labels=None,
        orientation=None,
        color_discrete_sequence=None,
        color_discrete_map=None,
        line_dash_sequence=None,
        line_dash_map=None,
        symbol_sequence=None,
        symbol_map=None,
        markers=False,
        log_x=False,
        log_y=False,
        range_x=None,
        range_y=None,
        line_shape=None,
        render_mode='auto',
        title=None,
        template=None,
        width=None,
        height=None,

        # Design
        y_tickformat=None,

):
    # Generate Line Chart
    fig = px.line(
        data_frame=data_frame,
        x=x,
        y=y,
        line_group=line_group,
        color=color,
        line_dash=line_dash,
        symbol=symbol,
        hover_name=hover_name,
        hover_data=hover_data,
        custom_data=custom_data,
        text=text,
        facet_row=facet_row,
        facet_col=facet_col,
        facet_col_wrap=facet_col_wrap,
        facet_row_spacing=facet_row_spacing,
        facet_col_spacing=facet_col_spacing,
        error_x=error_x,
        error_x_minus=error_x_minus,
        error_y=error_y,
        error_y_minus=error_y_minus,
        animation_frame=animation_frame,
        animation_group=animation_group,
        category_orders=category_orders,
        labels=labels,
        orientation=orientation,
        color_discrete_sequence=color_discrete_sequence,
        color_discrete_map=color_discrete_map,
        line_dash_sequence=line_dash_sequence,
        line_dash_map=line_dash_map,
        symbol_sequence=symbol_sequence,
        symbol_map=symbol_map,
        markers=markers,
        log_x=log_x,
        log_y=log_y,
        range_x=range_x,
        range_y=range_y,
        line_shape=line_shape,
        render_mode=render_mode,
        title=title,
        template=template,
        width=width,
        height=height,
    )

    # Title
    fig.update_layout(
        title={
            'text': title,
            'font': {
                'family': "Arial, sans-serif",
                'size': 24,
                # 'color': "#1E3A2F"  # Dark green
            },
            'x': 0.5,
            'y': 0.9,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    # Background
    # fig.update_layout(
    #     plot_bgcolor='#FFFFFF',
    #     paper_bgcolor='#FFFFFF',
    # )

    # X axis
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        # gridcolor='black',
        # tickcolor='black',
        # tickfont=dict(color='black'),
    )

    # Y axis
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        # gridcolor='black',
        # tickcolor='black',
        # tickfont=dict(color='black'),
        tickformat=y_tickformat,
    )

    # Legend
    fig.update_layout(
        legend=dict(
            title='Legend',
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="right",
            x=1
        ),
    )

    return fig
