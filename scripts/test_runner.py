# scripts/test_runner.py

import os
import argparse
import traceback
from csv2ics import process_csv
from teams import load_teams_config, get_team_by_id, get_user_role
from utils import validate_csv_path, ensure_output_dir

def run_hosted_calendar_generation(team_id, user_email):
    teams = load_teams_config()
    team = get_team_by_id(team_id, teams)

    if not team:
        print(f"❌ Team '{team_id}' not found.")
        return None

    role = get_user_role(team, user_email)
    print(f"\n🔐 Simulated role: {role} for {user_email}")

    team["csv"] = team.get("csv", f"data/{team_id}.csv")
    team["output"] = team.get("output", f"docs/calendars/{team_id}")

    try:
        validate_csv_path(team["csv"])
        ensure_output_dir(team["output"])

        result = process_csv(team)

        print(f"\n✅ Generated {len(result['generated_files'])} ICS file(s):")
        for fname in result["generated_files"]:
            print(f"   - {fname}")
        print(f"\n📄 Download page saved to: {os.path.join(result['output_dir'], 'download_links.md')}")
        return result

    except Exception as e:
        print(f"\n❌ Hosted generation failed: [{type(e).__name__}] {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ICS for a team")
    parser.add_argument("--team", required=True, help="Team ID (e.g. hhs_baseball)")
    parser.add_argument("--user", required=True, help="User email")

    args = parser.parse_args()
    run_hosted_calendar_generation(args.team, args.user)
