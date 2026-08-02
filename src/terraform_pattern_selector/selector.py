def select_pattern(app_profile, deployment_requirements):
    pattern = {
        "pattern_name": None,
        "components": []
    }

    if deployment_requirements.get("needs_container"):
        pattern["components"].append("container")

    if deployment_requirements.get("needs_database"):
        pattern["components"].append("database")

    if deployment_requirements.get("needs_public_access"):
        pattern["components"].append("networking")

    if app_profile.get("language") == "Python":
        pattern["pattern_name"] = "python_web_app"

    return pattern