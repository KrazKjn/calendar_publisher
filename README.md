# 📅 calendar_publisher

**CSV to ICS creation with subscription-ready output**

This project streamlines the process of converting CSV-based event data into `.ics` calendar files. While future versions may support direct CSV upload and web-based conversion, the current implementation operates via command-line for fast, reliable generation.

I built this tool to simplify the chaos of managing my children's high school and middle school sports schedules. Most calendars are distributed in Word or PDF format, which makes syncing to mobile devices repetitive, tedious, and error-prone. Mass updates are nearly impossible.

With this project, I can quickly update a CSV spreadsheet, generate `.ics` files, and publish calendars via GitHub hosting. My workflow typically involves copying calendar text, formatting it in Excel, and converting it into structured columns. Once complete, I commit the changes and the calendars are instantly available for subscription.

---

### ✅ Features

- Flexible CSV parsing with smart column detection
- ICS generation for mobile and desktop calendar apps
- Markdown download page for easy sharing
- GitHub-hosted publishing for instant access

---

### 🔧 Usage

```bash
python csv2ics.py --input events.csv --output calendars

This will generate .ics files for each team or group and create a download_links.md file and web page with branded links.

## 📌 Tags
`#automation` `#scripting` `#python`
