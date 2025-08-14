from flask import Flask, request, jsonify, send_from_directory
from scripts.teams import (
    load_teams_config,
    get_team_by_id,
    is_user_allowed,
    get_user_role
)
from scripts.csv2ics import process_csv
import os, json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
LOG_FOLDER = 'logs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

teams = load_teams_config()
if not teams:
    raise RuntimeError("❌ Teams config not found.")

@app.route('/upload', methods=['POST'])
def upload_csv():
    user = request.form.get('user')
    team_id = request.form.get('team')
    file = request.files.get('file')

    team = get_team_by_id(team_id, teams)
    if not team:
        return jsonify({'error': 'Team config not found'}), 404

    if not is_user_allowed(team, user):
        return jsonify({'error': 'Unauthorized'}), 403

    # Save uploaded CSV
    team_folder = os.path.join(UPLOAD_FOLDER, team_id)
    os.makedirs(team_folder, exist_ok=True)
    filepath = os.path.join(team_folder, file.filename)
    file.save(filepath)

    # Update team config with uploaded CSV path
    team["csv"] = filepath
    team["output"] = f"docs/calendars/{team_id}"

    try:
        result = process_csv(team)
        log_success(user, team_id, file.filename)
        return jsonify({
            'status': 'Success',
            'ics_files': result["generated_files"],
            'download_page': os.path.join(team["output"], "download_links.md")
        })
    except Exception as e:
        log_failure(user, team_id, file.filename, str(e))
        return jsonify({'error': 'Generation failed', 'details': str(e)}), 500

@app.route('/calendar/<team_id>/<filename>')
def serve_calendar(team_id, filename):
    calendar_dir = os.path.join("docs", "calendars", team_id)
    return send_from_directory(calendar_dir, filename)

def log_success(user, team_id, filename):
    log_entry = {
        'user': user,
        'team': team_id,
        'file': filename,
        'status': 'success'
    }
    with open(os.path.join(LOG_FOLDER, 'log.json'), 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def log_failure(user, team_id, filename, error):
    log_entry = {
        'user': user,
        'team': team_id,
        'file': filename,
        'status': 'failure',
        'error': error
    }
    with open(os.path.join(LOG_FOLDER, 'log.json'), 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

if __name__ == '__main__':
    app.run(debug=True)
