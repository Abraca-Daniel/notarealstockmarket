from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
import os
app = Flask(__name__)
app.debug = True

dasedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy (app)


class Company(db.Model):
    __tablename__ = 'Company'
    companyId = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), foreign_key=True)
    total_shares = db.Column(db.Integer())
    name = db.Column(db.String())
    
    def __init__(self, name, ticker):
        self.name = name
        self.ticker = ticker
        

class Stock(db.Model):
   __tablename__ = 'Stock'
   stockId = db.Column(db.Integer, primary_key=True)
   ticker = db.Column(db.String(10))
   price = db.Column(db.Float())
   date = db.Column(db.DateTime, default=func.now())

   def __init__(self, company, ticker, price, date):
      self.company = company
      self.ticker = ticker
      self.price = price
      self.date = date

   def __repr__(self):
      return f'{self.ticker} at {self.price}'

    
class Portfolio(db.Model):
    __tablename__ = 'Portfolio'
    portfolioId = db.Column(db.Integer, primary_key=True)
    cash_amount = db.Column(db.Float())
    stocks = db.Column(db.String())

    def __init__(self, user, cash_amount=0):
        self.user = user
        self.stocks = {}
        self.cash_amount = cash_amount

    def add_stock(self, stock, quantity):
        if stock.ticker not in self.stocks:
            self.stocks[stock.ticker] = quantity
        else:
            self.stocks[stock.ticker] += quantity

    def remove_stock(self, stock, quantity):
        if stock.ticker not in self.stocks or self.stocks[stock.ticker] < quantity:
            print("You don't have enough shares of this stock to sell.")
            return
        self.stocks[stock.ticker] -= quantity

    def view_portfolio(self):
        print("Portfolio:")
        for ticker, quantity in self.stocks.items():
            print(f"{ticker}: {quantity} shares")

    def view_balance(self):
        return self.cash_amount

    def deposit_cash(self, amount):
        self.cash_amount += amount

    def withdraw_cash(self, amount):
        if amount > self.cash_amount:
            print("Insufficient funds in wallet.")
            return False
        self.cash_amount -= amount
        return True
    
    def view_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)


class Transations(db.Model):
    __tablename__ = 'Transaction_Ledger'
    transactId = db.column(db.Iteger, primary_key=True)
    userId = db.column(db.Integer, foreign_key=True)
    stockId = db.column(db.Integer, foreign_key=True)
    isWalletTransact = db.column(db.boolean)
    portfolioId = db.column(db.Integer, foreign_key=True)
    cashValue = db.column(db.Integer)

    def __init__(self, user, ticker, price, date):
      self.user = user
      self.ticker = ticker
      self.price = price
      self.date = date


class User(db.Model):
   __tablename__ = 'User'
   userId = db.Column(db.Integer, primary_key=True)
   full_name = db.Column(db.String())
   username = db.Column(db.String(20))
   email = db.Column(db.String())
   password = db.Column(db.String())
   portfolio = db.Column(db.Integer, foreign_key=True)
   transaction_history = db.Column(db.String())
   
   def __init__(self, full_name, username, email, password):
      self.full_name = full_name
      self.username = username
      self.email = email
      self.password = password
      self.portfolio = Portfolio(self)
      self.transaction_history = []

   def buy_stock(self, stock, quantity):
        if stock.price * quantity > self.portfolio.view_balance():
            print("Not enough money available to buy this quantity of stock.")
            return
        self.portfolio.add_stock(stock, quantity)
        self.portfolio.withdraw_cash(stock.price * quantity)
        self.transaction_history.append(f"Bought {quantity} shares of {stock.company.name} at ${stock.price} per share")

   def sell_stock(self, stock, quantity):
        self.portfolio.remove_stock(stock, quantity)
        self.portfolio.deposit_cash(stock.price * quantity)
        self.transaction_history.append(f"Sold {quantity} shares of {stock.company.name} at ${stock.price} per share")

   def deposit_cash(self, amount):
        self.portfolio.deposit_cash(amount)
        self.transaction_history.append(f"Deposited ${amount} into cash account")

   def withdraw_cash(self, amount):
        if self.portfolio.withdraw_cash(amount):
            self.transaction_history.append(f"Withdrew ${amount} from cash account")

   def view_portfolio(self):
        self.portfolio.view_portfolio()

   def view_balance(self):
        self.portfolio.view_balance

   def view_transaction_history(self):
        self.portfolio.view_transaction_history()


class Accounts:
    def __init__(self):
        self.users = {}

    def create_account(self, full_name, username, email, password):
        if username in self.users:
            print('Username already exists. Pleases choose a different username.')
            return False
        self.users[username] = User(full_name, username, email, password)
        print('Acount created successfully. Thank you for joining NotARealStock.Exchange')
        return True
    
    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            print('Login successful')
            return self.user[username]
        else:
            print('Invalid username or password.')
            return None


class Administrator:
    def __init__(self):
        self.companies = []
        self.stocks = []

    def add_company(self, name, symbol):
        self.companies.append(Company(name, symbol))
        print(f"Company {name} added successfully.")

    def add_stock(self, company, ticker, volume, price):
        self.stocks.append(Stock(company, ticker, volume, price))
        print(f"Stock {ticker} added successfully.")

 #   def change_market_hours(self, start_time, end_time):
 #       print(f"Market hours changed to {start_time} - {end_time}")

 #   def change_market_schedule(self, weekdays, holidays):
 #       print(f"Market open on weekdays: {weekdays}")
 #       print(f"Market closed on holidays: {holidays}")


@app.route("/")
def hello_world():
   return render_template('index.html')

@app.route("/contact")
def contact():
   tickers = ['This is apple.',
           'This is microsoft',
           'This is google',
           'This is facebook',
           ]
   return render_template('contact.html', tickers=tickers)

@app.route("/trade")
def trade():
   return render_template('trade.html')

@app.route("/portfolio")
def portfolio():
   return render_template('portfolio.html')

@app.route("/transaction")
def transaction():
   stock = Stock.query.all()
   return render_template('transaction.html', stock=stock)

@app.route("/faq")
def faq():
   return render_template('faq.html')
