# hello world streamlit application
import streamlit as st
from models import Scenario, Expense, Income, Asset, Risk, session
import plotly.express as px
from functions import add_expense_form, render_expenses, add_income_form, render_incomes, master_update

all_scenarios = session.query(Scenario).all()

st.title('How Long Till Homeless?')
st.write('Estimate how long you can survive in the event of income loss with assumptions for rising costs.')

@st.dialog("New Scenario")
def add_scenario():
    st.write('Add Scenario')
    name = st.text_input('Name')
    desc = st.text_area('Description')
    inflation_lb = st.number_input('Annual Inflation Lower Bound')
    inflation_ub = st.number_input('Annual Inflation Upper Bound')
    if st.button('Save'):
        new_scenario = Scenario(
            name=name,
            description=desc,
            annual_inflation_lower_bound=inflation_lb,
            annual_inflation_upper_bound=inflation_ub
        )
        session.add(new_scenario)
        session.commit()
        st.rerun()


@st.dialog("Manage Expenses")
@st.fragment
def manage_expenses():
    if st.button('Add Expense'):
        st.session_state.show_expense_form = True

    if 'show_expense_form' in st.session_state and st.session_state.show_expense_form:
        add_expense_form()
    
    render_expenses()


@st.dialog("Manage Incomes")
@st.fragment
def manage_incomes():
    if st.button('Add Income'):
        st.session_state.show_income_form = True

    if 'show_income_form' in st.session_state and st.session_state.show_income_form:
        add_income_form()
    
    render_incomes()


@st.dialog("Add Asset")
def add_asset():
    if 'active_scenario_id' not in st.session_state:
        st.error('Please select a scenario first')
        return
    
    st.write('Add Asset')
    name = st.text_input('Name')
    desc = st.text_area('Description')
    amount = st.number_input('Amount')
    penalty = st.number_input('Penalty')
    if st.button('Save'):
        new_asset = Asset(
            scenario_id=st.session_state.active_scenario_id,
            name=name,
            description=desc,
            amount=amount,
            penalty=penalty
        )
        session.add(new_asset)
        session.commit()
        st.rerun()

# Arrange buttons inline using st.columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('New Scenario'):
        add_scenario()

with col2:
    if st.button('Manage Expenses'):
        manage_expenses()

with col3:
    if st.button('Manage Incomes'):
        manage_incomes()

with col4:
    if st.button('Add Asset'):
        add_asset()

scenario_dict = {s.name: s.id for s in all_scenarios}
selected_scenario_name = st.selectbox('Select Scenario', list(scenario_dict.keys()))
@st.fragment(run_every="1s")
def render_output():
    st.session_state.active_scenario_id = scenario_dict[selected_scenario_name]
    master_update()

    # Display the summary
    report_col1, report_col2 = st.columns([1, 3])
    with report_col1:
        st.metric("Total Monthly Income", value = f'${st.session_state.total_monthly_income:,.2f}')
        st.metric("Total Monthly Expenses (LB)", value = f'${st.session_state.total_expenses_lb:,.2f}')
        st.metric("Total Monthly Expenses (UB)", value = f'${st.session_state.total_expenses_ub:,.2f}')
        st.metric("Total Assets", value = f'${st.session_state.total_assets:.2f}', delta = f'{st.session_state.pct_asset_change:.2%} monthly')

    with report_col2:
        # Calculate monthly change to assets over the course of 1 year
        monthly_changes = []
        current_assets = st.session_state.total_assets
        for month in range(12):
            current_assets += st.session_state.total_monthly_income - st.session_state.total_expenses_ub
            monthly_changes.append(current_assets)

        # Plot the chart using Plotly Express
        fig = px.line(x=range(1, 13), y=monthly_changes, title='Monthly Change to Assets Over 1 Year')
        fig.update_xaxes(title_text='Months from Present')
        fig.update_yaxes(title_text='Assets ($)')
        fig.update_traces(hovertemplate='Month: %{x}<br>Assets: $%{y:,.2f}')
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig.update_xaxes(tickvals=[3, 6, 9, 12])
        st.plotly_chart(fig)
if selected_scenario_name:
    render_output()
    # st.session_state.active_scenario_id = scenario_dict[selected_scenario_name]
    # master_update()

    # # Display the summary
    # report_col1, report_col2 = st.columns([1, 3])
    # with report_col1:
    #     st.metric("Total Monthly Income", value = f'${st.session_state.total_monthly_income:,.2f}')
    #     st.metric("Total Monthly Expenses (LB)", value = f'${st.session_state.total_expenses_lb:,.2f}')
    #     st.metric("Total Monthly Expenses (UB)", value = f'${st.session_state.total_expenses_ub:,.2f}')
    #     st.metric("Total Assets", value = f'${st.session_state.total_assets:.2f}', delta = f'{st.session_state.pct_asset_change:.2%} monthly')

    # with report_col2:
    #     # Calculate monthly change to assets over the course of 1 year
    #     monthly_changes = []
    #     current_assets = st.session_state.total_assets
    #     for month in range(12):
    #         current_assets += st.session_state.total_monthly_income - st.session_state.total_expenses_ub
    #         monthly_changes.append(current_assets)

    #     # Plot the chart using Plotly Express
    #     fig = px.line(x=range(1, 13), y=monthly_changes, title='Monthly Change to Assets Over 1 Year')
    #     fig.update_xaxes(title_text='Months from Present')
    #     fig.update_yaxes(title_text='Assets ($)')
    #     fig.update_traces(hovertemplate='Month: %{x}<br>Assets: $%{y:,.2f}')
    #     fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    #     fig.update_xaxes(tickvals=[3, 6, 9, 12])
    #     st.plotly_chart(fig)