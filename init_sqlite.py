# create a sqlite database
if __name__ == '__main__':
    import sqlite3
    import os
    # create a connection to the database
    conn = sqlite3.connect('.hth/localstate.db')

    # create a cursor object
    cur = conn.cursor()

    # create a table scenarios if it does not exist
    # id, name, description, created_at, updated_at
    cur.execute('''
    CREATE TABLE IF NOT EXISTS scenarios (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        annual_inflation_lower_bound REAL NOT NULL,
        annual_inflation_upper_bound REAL NOT NULL
    )
    ''')

    # create table expenses if it doesn't exist
    # id, scenario_id, name, description, amount, created_at, updated_at

    cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        scenario_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        recurring BOOLEAN NOT NULL,
        recurring_interval TEXT,
        amount REAL NOT NULL,
        apply_inflation BOOLEAN NOT NULL,
        FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
    )
    ''')

    # create table incomes if it doesn't exist
    # id, scenario_id, name, description, amount, created_at, updated_at

    cur.execute('''
    CREATE TABLE IF NOT EXISTS incomes (
        id INTEGER PRIMARY KEY,
        scenario_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        basis TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
    )
    ''')

    # create table assets if it doesn't exist
    # id, scenario_id, name, description, amount, created_at, updated_at

    cur.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY,
        scenario_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL,
        penalty REAL NOT NULL,
        FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
    )
    ''')

    # create table risks if it doesn't exist
    # id, scenario_id, name, description, amount, horizon
    cur.execute('''
    CREATE TABLE IF NOT EXISTS risks (
        id INTEGER PRIMARY KEY,
        scenario_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL,
        horizon INTEGER NOT NULL,
        FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
    )
    ''')

    # close the connection
    conn.close()