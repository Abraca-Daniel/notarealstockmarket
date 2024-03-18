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


class Company:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        

class Stock(db.Model):
   __tablename__ = 'stocks'
   id = db.Column(db.Integer, primary_key=True)
   ticker = db.Column(db.String(10))
   price = db.Column(db.Float())
   date = db.Column(db.DateTime, default=func.now)

   def __init__(self, ticker, price, date):
      self.ticker = ticker
      self.price = price
      self.date = date

   def __repr__(self):
      return f'{self.ticker} at {self.price}'
   

class Wallet:
    def __init__(self, user, cash_amount=0):
        self.user = user
        self.cash_amount = cash_amount

    def deposit_cash(self, amount):
        self.cash_amount += amount

    def withdraw_cash(self, amount):
        if amount > self.cash_amount:
            print("Insufficient funds in wallet.")
            return False
        self.cash_amount -= amount
        return True

    def view_balance(self):
        return self.cash_amount
    

class Portfolio:
    def __init__(self, user):
        self.user = user
        self.stocks = {}

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


class User:
   def __init__(self, full_name, username, email, password):
      self.full_name = full_name
      self.username = username
      self.email = email
      self.password = password
      self.wallet = Wallet(self)
      self.portfolio = portfolio
      self.transaction_history = []

   def buy_stock(self, stock, quantity):
        if stock.price * quantity > self.wallet.view_balance():
            print("Not enough money available to buy this quantity of stock.")
            return
        self.portfolio.add_stock(stock, quantity)
        self.wallet.withdraw_cash(stock.price * quantity)
        self.transaction_history.append(f"Bought {quantity} shares of {stock.company.name} at ${stock.price} per share")

   def sell_stock(self, stock, quantity):
        self.portfolio.remove_stock(stock, quantity)
        self.wallet.deposit_cash(stock.price * quantity)
        self.transaction_history.append(f"Sold {quantity} shares of {stock.company.name} at ${stock.price} per share")

   def deposit_cash(self, amount):
        self.wallet.deposit_cash(amount)
        self.transaction_history.append(f"Deposited ${amount} into cash account")

   def withdraw_cash(self, amount):
        if self.wallet.withdraw_cash(amount):
            self.transaction_history.append(f"Withdrew ${amount} from cash account")

   def view_portfolio(self):
        self.portfolio.view_portfolio()

   def view_cash_account(self):
        print(f"Cash Account Balance: ${self.wallet.view_balance()}")

   def view_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)


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
   return render_template('transaction.html')

@app.route("/faq")
def faq():
   return render_template('faq.html')
