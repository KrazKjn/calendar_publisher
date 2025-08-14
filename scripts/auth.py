import json

def validate_user(user, team):
    with open('data/allowed_users.json') as f:
        allowed = json.load(f)
    return user in allowed and team in allowed[user]
