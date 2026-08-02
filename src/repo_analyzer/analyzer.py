from pathlib import Path


def analyze_repository(repo_path):
    repo = Path(repo_path)

    result = {
        "repository": repo.name,
        "language": None,
        "framework": None,
        "requirements_file": False,
        "dockerfile": False,
        "terraform": False,
    }

    if (repo / "requirements.txt").exists():
        result["language"] = "Python"
        result["requirements_file"] = True

    if (repo / "Dockerfile").exists():
        result["dockerfile"] = True

    terraform_files = list(repo.glob("*.tf"))

    if terraform_files:
        result["terraform"] = True

    return result