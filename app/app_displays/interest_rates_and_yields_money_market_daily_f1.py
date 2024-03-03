import streamlit as st


def interest_rates_and_yields_money_market_daily_f1(
        single_col_charts_dict
):

    # Insert containers separated into tabs:
    list_of_charts_dicts = single_col_charts_dict[
        'Interest Rates and Yields – Money Market – Daily – F1']

    for title, charts_dict in list_of_charts_dicts.items():
        st.write(f'## {title}')

        # Dynamically create tabs based on the keys in charts_dict
        tab_keys = sorted(charts_dict.keys(), key=int)  # Ensure tabs are ordered numerically
        tabs = st.tabs([f"{int(key) // 12} years" if int(key) % 12 == 0 else f"{key} months" for key in tab_keys])

        for i, key in enumerate(tab_keys):
            with tabs[i]:
                st.plotly_chart(charts_dict[key], use_container_width=True)
    # # Charts within tabs
    # # Insert containers separated into tabs:
    # list_of_charts_dicts = single_col_charts_dict[
    #     'Interest Rates and Yields – Money Market – Daily – F1']
    # for title, charts_dict in list_of_charts_dicts.items():
# 
    #     st.write(f'## {title}')
    #     months_12, months_60, months_120 = st.tabs(["1 year", "5 years", "10 years"])
    #     # Tab 1 content
    #     with months_12:
    #         st.plotly_chart(charts_dict['12'], use_container_width=True)
    #     with months_60:
    #         st.plotly_chart(charts_dict['60'], use_container_width=True)
    #     with months_120:
    #         st.plotly_chart(charts_dict['120'], use_container_width=True)

    # text
    st.write('Text analysis to be displayed here.')
