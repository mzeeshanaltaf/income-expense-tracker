import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from database import *
import calendar
from datetime import datetime
import time


# -------SETTINGS --------------
incomes = ["Salary", "Social Media", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]
currency = "USD"
page_title = "Budget Insight"
page_icon = ":money_with_wings:"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")
st.title(page_title + page_icon)
st.write(":blue[***Visualize Your Financial Journey***]")
st.write(f"{page_title} is a financial management app designed to help you keep track of your income and "
         "expenses with ease. Input your monthly earnings and expenditures, store them securely in the database, "
         "and gain valuable insights through intuitive visualizations. ")

# -----------DROP DOWN VALUES FOR SELECTING THE TIME PERIOD-------------------
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name)[1:]

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -- Navigation Menu ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization", "About"],
    icons=["pencil-fill", "bar-chart-fill", "app"],  # https://icons.getbootstrap.com
    orientation="horizontal",
)

# ------------INPUT & SAVE TIME PERIOD------------
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")

        st.divider()
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("Comment"):
            comment = st.text_area("Comments", placeholder="Enter a comment here ...", label_visibility="collapsed")
        st.divider()
        submitted = st.form_submit_button("Save Data")
        if submitted:
            with st.spinner('Processing...'):
                period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
                incomes = {income: st.session_state[income] for income in incomes}
                expenses = {expense: st.session_state[expense] for expense in expenses}
                period_data = dict(Period=period, Incomes=incomes, Expenses=expenses, Comments=comment)
                all_periods = get_all_periods()
                if period in all_periods:
                    st.info(f'Income and Expense details for {st.session_state["month"]} {st.session_state["year"]}  '
                            f'already exists.')
                else:
                    insert_period(period_data)
                    st.success("Data Saved!")

# ----PLOT PERIOD----
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("save_periods"):
        with st.spinner('Processing ...'):
            period = st.selectbox("Select Period", get_all_periods())
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            period_data = get_period(period)
            comment = period_data.get("Comments")
            expenses = period_data.get("Expenses")
            incomes = period_data.get("Incomes")

            # Create metrics
            total_income = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remaining_budget = total_income - total_expenses
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expenses", f"{total_expenses} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comment: {comment}")

            # Create sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            # Plot the chart
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)

# ----- SETUP ABOUT MENU ------
if selected == "About":
    with st.expander("About this App"):
        st.markdown(''' Budget Insight is a financial management app designed to help you keep track of your income and 
        expenses with ease. It has following functionality:

    - Input your income and expenses for each month with ease
    - Safe and secure storage in cloud db 
    - Intuitive visualization with insightful sankey chart will help you to understand your financial habits

        ''')

    with st.expander("Which database is used for storing data?"):
        st.markdown(''' MongoDB Cloud is used to store income and expense data securely.
        ''')

    with st.expander("Where to get the source code of this app?"):
        st.markdown(''' Source code is available at:
    -  https://github.com/mzeeshanaltaf/income-expense-tracker
        ''')
    with st.expander("Whom to contact regarding this app?"):
        st.markdown(''' Contact [Zeeshan Altaf](zeeshan.altaf@gmail.com)
        ''')