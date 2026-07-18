import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.normpath(os.path.join(HERE, "..", "profile.yaml"))

if not os.path.exists(PROFILE_PATH):
    raise FileNotFoundError(f"Profile configuration not found at: {PROFILE_PATH}")

with open(PROFILE_PATH, "r", encoding="utf-8") as f:
    _data = yaml.safe_load(f) or {}

def get(key, default=None):
    return _data.get(key, default)

# Load profile data with fallback override check for env variable
GITHUB_USERNAME = os.getenv("GH_PROFILE_USER", get("github_username", "MeghPatel-007"))
DISPLAY_NAME = get("display_name", "Megh Patel")
ROLE = get("role", "")
LOCATION = get("location", "")
EDUCATION = get("education", "")
FOCUS = get("focus", "")
PORTFOLIO_URL = get("portfolio_url", "")
SECTIONS = get("sections", {})
