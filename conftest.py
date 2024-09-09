# conftest.py
import os

from dotenv import load_dotenv

load_dotenv()

COOKIE_FILE = os.getenv("SESSIONID_COOKIE_FILE")


def pytest_sessionstart(session):
    print("Deleting ASP.NET_SessionId cookie file before starting the test session.")
    try:
        if os.path.exists(COOKIE_FILE):
            os.remove(COOKIE_FILE)
            print(
                f"Deleted {COOKIE_FILE} to force a new session for each test suite run."
            )
        else:
            print(f"Cookie file {COOKIE_FILE} does not exist, no need to delete.")
    except Exception as e:
        print(f"Error deleting {COOKIE_FILE}: {e}")
