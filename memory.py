import json
import os

PROFILE_FILE = "user_profile.json"
LOG_FILE = "wellness_log.json"


def default_profile():
    return {
        "user_type": "college student",
        "wellness_goals": [],
        "sleep": {
            "goal": "",
            "usual_pattern": "",
            "consistency": 0
        },
        "hydration": {
            "goal": "",
            "consistency": 0
        },
        "physical_activity": {
            "goal": "",
            "consistency": 0
        },
        "nutrition": {
            "goal": "",
            "preferences": []
        },
        "stress_management": {
            "goal": "",
            "preferred_methods": []
        },
        "previous_challenges": [],
        "successful_habits": [],
        "preferred_response_style": "short and practical",
        "overall_wellness_score": 0
    }


def load_profile():
    if not os.path.exists(PROFILE_FILE):
        profile = default_profile()
        save_profile(profile)
        return profile

    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        profile = default_profile()
        save_profile(profile)
        return profile


def save_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profile, file, indent=4)


def load_logs():
    if not os.path.exists(LOG_FILE):
        return {}

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)


def add_checkin(date, data):
    logs = load_logs()
    logs[date] = data
    save_logs(logs)


def calculate_score(data):
    sleep = min(float(data.get("sleep_hours", 0)) / 8 * 100, 100)
    water = min(float(data.get("water", 0)) / 8 * 100, 100)
    activity = min(float(data.get("activity_minutes", 0)) / 30 * 100, 100)

    stress = float(data.get("stress_level", 10))
    stress_score = max(0, 100 - ((stress - 1) * 11.11))

    score = (sleep + water + activity + stress_score) / 4

    return round(score)


def update_profile_from_checkin(data):
    profile = load_profile()

    score = calculate_score(data)

    profile["overall_wellness_score"] = score

    if data.get("sleep_hours", 0) < 7:
        if "irregular sleep" not in profile["previous_challenges"]:
            profile["previous_challenges"].append("irregular sleep")

    if data.get("water", 0) >= 6:
        if "better hydration" not in profile["successful_habits"]:
            profile["successful_habits"].append("better hydration")

    if data.get("activity_minutes", 0) >= 20:
        if "regular activity" not in profile["successful_habits"]:
            profile["successful_habits"].append("regular activity")

    save_profile(profile)

    return profile