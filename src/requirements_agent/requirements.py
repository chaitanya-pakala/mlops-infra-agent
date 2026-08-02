def build_requirements(app_profile):
    requirements = {
        "needs_container": False,
        "needs_database": False,
        "needs_kubernetes": False,
        "needs_public_access": False,
        "needs_environment_variables": False,
        "recommended_runtime": None,
    }

    if app_profile.get("language") == "Python":
        requirements["recommended_runtime"] = "python"

    if app_profile.get("kubernetes"):
        requirements["needs_kubernetes"] = True

    if not app_profile.get("dockerfile"):
        requirements["needs_container"] = True

    if app_profile.get("database"):
        requirements["needs_database"] = True

    if app_profile.get("environment_files"):
        requirements["needs_environment_variables"] = True

    return requirements