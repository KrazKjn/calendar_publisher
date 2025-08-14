# test_runner.py

import os
import traceback
from scripts.csv2ics import process_csv
from scripts.utils import validate_csv_path, ensure_output_dir
from scripts.teams import load_teams_config, get_team_by_id, get_user_role

def run_hosted_calendar_generation(team_id, user_email, datetime_format=None):
    teams = load_teams_config()
    team = get_team_by_id(team_id, teams)

    if not team:
        print(f"❌ Team '{team_id}' not found.")
        return None

    role = get_user_role(team, user_email)
    print(f"\n🔐 Simulated role: {role} for {user_email}")

    input_path = team.get("csv")
    output_dir = team.get("output", f"calendars/{team_id}")
    team["output"] = output_dir  # Ensure it's set for process_csv()

    print(f"\n🌐 Hosted Calendar Generation")
    print(f"📁 Input CSV: {input_path}")
    print(f"📂 Output Directory: {output_dir}")
    if datetime_format:
        print(f"🕒 Manual Format: {datetime_format}")
        team["datetime_format"] = datetime_format

    try:
        validate_csv_path(input_path)
        ensure_output_dir(output_dir)

        result = process_csv(team)

        print(f"\n✅ Generated {len(result['generated_files'])} ICS file(s):")
        for fname in result["generated_files"]:
            print(f"   - {fname}")
        print(f"\n📄 Download page saved to: {os.path.join(result['output_dir'], 'download_links.md')}")
        print(f"🕒 Datetime format used: {result['datetime_format']}")
        return result

    except Exception as e:
        print(f"\n❌ Hosted generation failed: [{type(e).__name__}] {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    run_hosted_calendar_generation("hhs_volleyball", "coach.hhsvb@gmail.com")
