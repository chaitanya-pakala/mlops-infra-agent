from pathlib import Path


DATABASE_KEYWORDS = [
    "sqlalchemy",
    "psycopg2",
    "pymysql",
    "mysql",
    "sqlite",
    "pymongo",
    "redis",
]

KUBERNETES_FILES = [
    "deployment.yaml",
    "deployment.yml",
    "service.yaml",
    "service.yml",
]


def analyze_repository(repo_path):
    repo = Path(repo_path)

    result = {
        "repository": repo.name,
        "language": None,
        "framework": None,
        "requirements_file": False,
        "dockerfile": False,
        "terraform": False,
        "database": False,
        "kubernetes": False,
    }

    requirements_path = repo / "requirements.txt"

    if requirements_path.exists():
        result["language"] = "Python"
        result["requirements_file"] = True

        requirements_text = requirements_path.read_text(
            encoding="utf-8"
        ).lower()

        if any(
            keyword in requirements_text
            for keyword in DATABASE_KEYWORDS
        ):
            result["database"] = True

    if (repo / "Dockerfile").exists():
        result["dockerfile"] = True

    terraform_files = list(repo.glob("*.tf"))

    if terraform_files:
        result["terraform"] = True

    for filename in KUBERNETES_FILES:
        matches = list(repo.rglob(filename))
        if matches:
            result["kubernetes"] = True
            break

    return result