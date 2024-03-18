### USER AUTHENTICATION PSEUDOCODE ###

login_process = get_user_login()
# function to retrieve credentials
# note that get_user_login will retrieve information given from the website
send_rq("authenticate_user", login_process)
# attempt process of user authentication

def authenticate_user(login_process):
    # process of authenticating the user

    if existing_user==True and account_locked(login_process):
        #checks if account exists & is locked
        return "Your account has been locked due to lots of failed auth attempts pls contact support"
    
    if existing_user==True:
    # checks if account exists. If it gets to this point the acc wasn't locked.
        if check_credential_hash(login_process):
        # checks credentials with hash for legitimacy
            reset_attempt_count(login_process)
            # ONLY IF SUCCESSFUL - resets # of login attempts to 0
            return "authentication successful"
        else:
            add_attempt_count(login_process)
            # increments the # of attempts to log into an acc by 1
            if get_failed_attempts(login_process) == 5:
            # retrieves the # of failed attempts so far from DB + locks the account if 5 login attempts have failed
                lock_user_account(login_process)
                return "Your account has been locked due to lots of failed auth attempts pls contact support"
            else:
            #tells the user their credentials were wrong
                return "Invalid credentials"
    else:
        return "Acc doesn't exist. Sign up instead?"
        # link to sign-up page + script
    
def account_locked():
    # checks if acc is locked or not

def check_credential_hash():
    # checks credentials with stored hash

def add_attempt_count():
    # increments the # of attempts to log into account

def get_failed_attempts():
    # gets the # of failed attempts that have been counted in the DB so far

def reset_attempt_count():
    # resets the # of failed attempts once authentication is successful

def lock_user_account():
    # sets the state of the user acc to 'locked' in the DB
