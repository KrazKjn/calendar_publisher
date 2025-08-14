import json

def load_teams_config(path="config/teams.json"):
    with open(path, "r") as f:
        return json.load(f)["teams"]

def get_team_by_id(team_id, teams):
    return next((team for team in teams if team["id"] == team_id), None)

def is_user_allowed(team, email):
    return email in team.get("allowed_users", [])

def get_user_role(team, email):
    return team.get("role_map", {}).get(email, "viewer")
