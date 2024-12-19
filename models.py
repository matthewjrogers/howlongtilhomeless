# make sqlalchemy models for tables
# filepath: /Users/f006p17/Desktop/localstate/models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    annual_inflation_lower_bound = Column(Float, nullable=False)
    annual_inflation_upper_bound = Column(Float, nullable=False)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    recurring = Column(Boolean, nullable=False)
    recurring_interval = Column(String)
    amount = Column(Float, nullable=False)
    apply_inflation = Column(Boolean, nullable=False)
    scenario = relationship('Scenario', back_populates='expenses')

class Income(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    basis = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    scenario = relationship('Scenario', back_populates='incomes')

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    amount = Column(Float, nullable=False)
    penalty = Column(Float, nullable=False)
    scenario = relationship('Scenario', back_populates='assets')

class Risk(Base):
    __tablename__ = 'risks'
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    amount = Column(Float, nullable=False)
    horizon = Column(Integer, nullable=False)
    scenario = relationship('Scenario', back_populates='risks')

Scenario.expenses = relationship('Expense', order_by=Expense.id, back_populates='scenario')
Scenario.incomes = relationship('Income', order_by=Income.id, back_populates='scenario')
Scenario.assets = relationship('Asset', order_by=Asset.id, back_populates='scenario')
Scenario.risks = relationship('Risk', order_by=Risk.id, back_populates='scenario')

# Create an engine and a session
engine = create_engine('sqlite:///./.hth/localstate.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
