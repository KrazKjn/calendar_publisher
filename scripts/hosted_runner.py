# hosted_runner.py

import os
import traceback
from scripts.csv2ics import process_csv
from scripts.utils import validate_csv_path, ensure_output_dir

def run_hosted_calendar_generation(input_path, output_dir="calendars", datetime_format=None):
    print(f"\n🌐 Hosted Calendar Generation")
    print(f"📁 Input CSV: {input_path}")
    print(f"📂 Output Directory: {output_dir}")
    if datetime_format:
        print(f"🕒 Manual Format: {datetime_format}")

    try:
        validate_csv_path(input_path)
        ensure_output_dir(output_dir)

        result = process_csv(
            input_path=input_path,
            output_dir=output_dir,
            datetime_format=datetime_format
        )

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
    # Example usage for testing
    run_hosted_calendar_generation("data/sample.csv", output_dir="hosted_output")
