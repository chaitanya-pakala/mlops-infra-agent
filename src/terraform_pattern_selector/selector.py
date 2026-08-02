PATTERN_CATALOG = {
    "docker_web_app": {
        "description": "Containerized web application",
        "components": ["container", "networking"],
    },

    "docker_web_app_with_db": {
        "description": "Containerized web application with a database",
        "components": ["container", "database", "networking"],
    },

    "kubernetes_web_app": {
        "description": "Containerized application deployed to Kubernetes",
        "components": ["container", "kubernetes", "networking"],
    },
}


def select_pattern(app_profile, deployment_requirements):
    needs_database = deployment_requirements.get(
        "needs_database", False
    )

    needs_container = deployment_requirements.get(
        "needs_container", False
    )

    needs_kubernetes = deployment_requirements.get(
        "needs_kubernetes", True
    )

    if needs_kubernetes:
        selected_pattern = "kubernetes_web_app"

    elif needs_database:
        selected_pattern = "docker_web_app_with_db"

    elif needs_container:
        selected_pattern = "docker_web_app"

    else:
        selected_pattern = "docker_web_app"

    pattern = PATTERN_CATALOG[selected_pattern].copy()
    pattern["pattern_name"] = selected_pattern

    return pattern