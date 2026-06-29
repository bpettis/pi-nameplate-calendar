import os, requests
from dotenv import load_dotenv

load_dotenv()
FILENAME = os.getenv("ICS_FILE", "calendar.ics")
CALENDAR_URL = os.getenv("CALENDAR_URL", None)
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

def main():
    # Backup existing file
    if os.path.exists(FILENAME):
        os.rename(FILENAME, f"{FILENAME}_backup.ics")

    # Enable the wifi:
    os.system("sudo rfkill unblock wifi")

    # Download calendar
    try:
        response = requests.get(CALENDAR_URL)
        response.raise_for_status()

        with open(FILENAME, "w") as f:
            f.write(response.text)

        print(f"Downloaded {FILENAME} from {CALENDAR_URL}")
    except Exception as e:
        print(f"Failed to download {FILENAME}: {e}")

        # Restore backup if it exists
        if os.path.exists(f"{FILENAME}_backup.ics"):
            os.rename(f"{FILENAME}_backup.ics", FILENAME)

            print(f"Restored backup {FILENAME}_backup.ics to {FILENAME}")
        return


    if not DEBUG:
        # Disable the wifi:
        os.system("sudo rfkill block wifi")

    # Cleanup backup
    if os.path.exists(f"{FILENAME}_backup.ics"):
        os.remove(f"{FILENAME}_backup.ics")
        print(f"Removed backup {FILENAME}_backup.ics")

if __name__ == "__main__":
    main()