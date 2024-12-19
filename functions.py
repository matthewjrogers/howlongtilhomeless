import streamlit as st
from models import Scenario, Expense, Income, Asset, Risk, session

def add_expense_form():
    st.write('Add Expense')
    name = st.text_input('Name')
    desc = st.text_area('Description')
    recurring = st.checkbox('Recurring')
    if recurring:
        recurring_interval = st.selectbox('Recurring Interval', ['daily', 'weekly', 'monthly', 'yearly'])
    amount = st.number_input('Amount')
    apply_inflation = st.checkbox('Apply Inflation')
    if st.button('Save'):
        new_expense = Expense(
            scenario_id=st.session_state.active_scenario_id,
            name=name,
            description=desc,
            recurring=recurring,
            recurring_interval=recurring_interval,
            amount=amount,
            apply_inflation=apply_inflation
        )
        session.add(new_expense)
        session.commit()
        st.session_state.show_expense_form = False
        calculate_expenses
        st.rerun(scope='fragment')

def render_expenses():
    if 'active_scenario_id' in st.session_state:
        expenses = session.query(Expense).filter_by(scenario_id=st.session_state.active_scenario_id).all()
        exp_col1, exp_col2, exp_col3, exp_col4 = st.columns(4)
        for i, expense in enumerate(expenses):
            with exp_col1:
                st.write(f'{expense.name}')
            with exp_col2:
                st.write(f'${expense.amount:,.2f} / {expense.recurring_interval if expense.recurring else "One-time"}')
            with exp_col3:
                st.write(f'{expense.description}')
            with exp_col4:
                if st.button('Delete', key=f'delete_{i}'):
                    session.delete(expense)
                    session.commit()
                    calculate_expenses()
                    st.rerun(scope='fragment')

def add_income_form():
    st.write('Add Income')
    name = st.text_input('Name')
    desc = st.text_area('Description')
    basis = st.selectbox('Basis', ['daily', 'weekly', 'monthly', 'yearly'])
    amount = st.number_input('Amount')
    if st.button('Save'):
        new_income = Income(
            scenario_id=st.session_state.active_scenario_id,
            name=name,
            description=desc,
            basis=basis,
            amount=amount
        )
        session.add(new_income)
        session.commit()
        st.session_state.show_income_form = False
        calculate_incomes()
        st.rerun(scope='fragment')

def render_incomes():
    if 'active_scenario_id' in st.session_state:
        incomes = session.query(Income).filter_by(scenario_id=st.session_state.active_scenario_id).all()
        inc_col1, inc_col2, inc_col3, inc_col4 = st.columns(4)
        for i, income in enumerate(incomes):
            with inc_col1:
                st.write(f'{income.name}')
            with inc_col2:
                st.write(f'${income.amount:,.2f} / {income.basis}')
            with inc_col3:
                st.write(f'{income.description}')
            with inc_col4:
                if st.button('Delete', key=f'delete_income_{i}'):
                    session.delete(income)
                    session.commit()
                    calculate_incomes()
                    st.rerun(scope='fragment')

def calculate_incomes():
    incomes = session.query(Income).filter_by(scenario_id=st.session_state.active_scenario_id).all()
    total_monthly_income = 0
    for income in incomes:
        if income.basis == 'daily':
            monthly_income = (income.amount * 365) / 12
        elif income.basis == 'weekly':
            monthly_income = (income.amount * 52) / 12
        elif income.basis == 'monthly':
            monthly_income = income.amount
        elif income.basis == 'yearly':
            monthly_income = income.amount / 12
        total_monthly_income += monthly_income
    st.session_state.total_monthly_income = total_monthly_income

def calculate_expenses():
    total_expenses_lb = 0
    total_expenses_ub = 0
    expenses = session.query(Expense).filter_by(scenario_id=st.session_state.active_scenario_id).all()
    for expense in expenses:
        if expense.recurring:
            if expense.recurring_interval == 'daily':
                monthly_expense = (expense.amount * 365) / 12
            elif expense.recurring_interval == 'weekly':
                monthly_expense = (expense.amount * 52) / 12
            elif expense.recurring_interval == 'monthly':
                monthly_expense = expense.amount
            elif expense.recurring_interval == 'yearly':
                monthly_expense = expense.amount / 12
        else:
            monthly_expense = expense.amount
        if expense.apply_inflation:
            monthly_expense_ub = monthly_expense * (1 + (session.query(Scenario).get(st.session_state.active_scenario_id).annual_inflation_upper_bound / 12))
            monthly_expense_lb = monthly_expense * (1 + (session.query(Scenario).get(st.session_state.active_scenario_id).annual_inflation_lower_bound / 12))
        total_expenses_lb += monthly_expense_lb
        total_expenses_ub += monthly_expense_ub
    st.session_state.total_expenses_lb = total_expenses_lb
    st.session_state.total_expenses_ub = total_expenses_ub

def calculate_assets():
    total_assets = 0
    assets = session.query(Asset).filter_by(scenario_id=st.session_state.active_scenario_id).all()
    for asset in assets:
        total_assets += asset.amount
    st.session_state.total_assets = total_assets

def master_update():
    calculate_incomes()
    calculate_expenses()
    calculate_assets()
    if st.session_state.total_assets:
        st.session_state.pct_asset_change = ((st.session_state.total_assets - (st.session_state.total_expenses_lb + st.session_state.total_expenses_ub)/2 + st.session_state.total_monthly_income) / st.session_state.total_assets) -1
    else:
        st.session_state.pct_asset_change = 0
