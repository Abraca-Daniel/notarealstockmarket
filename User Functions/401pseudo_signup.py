### SIGNUP PSEUDOCODE ###

def user_signup(signup_credentials):
    while not email_available(signup_credentials['email']):
        # 'as long as the email isn't available for sign up'
        print("Sorry, but an account exists with that email already. Try logging in instead?")
        #direct user to go log into their account.

    while not username_available(signup_credentials['username']):
        # 'as long as the username is taken'
        print("Sorry, but that username's taken. Try a different one.")
        signup_credentials['username'] = input("Enter a username: ")

    while not is_pass_valid(signup_credentials['password']):
        # 'as long as the password isn't complex enough'
        print("Your password doesn't meet our complexity requirements. Try a different one.")
        signup_credentials['password'] = input("Enter a password: ")
    
    create_user(signup_credentials)
    # creates the user account in the DB

    send_confirmation_email(signup_credentials['username'], signup_credentials['email'])
    # sends confirmation email

def email_available():
    # checks if the email is already registered in the database

def username_available():
    # checks if username is free from database
    # probably have requirement for usernames being more than 2 characters

def is_pass_valid():
    # checks if the password meets complexity requirements
    # requirements needed:
    ## (1) minimum 8 char, max 20
    ## (2) any 3 of the following:
    ##  (a) Upper case letters from Latin languages (A to Z)
    ##  (b) Lowercase letters from Latin languages (a to z)
    ##  (c) Digits 0 - 9
    ##  (d) At least 1 non-alphanumeric character like ~!@#$%^&*_-+=`|(){}[]:;"'<>,.?/

def create_user():
    # adds new user to database with accepted credentials

def send_confirmation_email():
    # sends the confirmation email to the email address provided
    print(f"We sent a confirmation email to {'email'} for {'username'}. It'll expire within 30 minutes.")