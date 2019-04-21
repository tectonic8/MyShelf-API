from db import db, User

def get_user_by_netid(netid):
  return User.query.filter(User.netid == netid).first()

def get_user_by_session_token():
  pass

def verify_credentials(email, password):
  pass

def create_user(email, password):
  pass

