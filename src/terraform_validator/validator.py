import subprocess
from pathlib import Path


def validate_terraform(terraform_dir="outputs/terraform"):
    terraform_path = Path(terraform_dir)

    result = {
        "fmt": None,
        "init": None,
        "validate": None,
        "plan": None,
        "success": False,
    }

    try:
        fmt = subprocess.run(
            ["terraform", "fmt", "-check"],
            cwd=terraform_path,
            capture_output=True,
            text=True
        )

        result["fmt"] = fmt.returncode == 0

        init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=terraform_path,
            capture_output=True,
            text=True
        )

        result["init"] = init.returncode == 0

        validate = subprocess.run(
            ["terraform", "validate"],
            cwd=terraform_path,
            capture_output=True,
            text=True
        )

        result["validate"] = validate.returncode == 0

        plan = subprocess.run(
            ["terraform", "plan", "-input=false"],
            cwd=terraform_path,
            capture_output=True,
            text=True
        )

        result["plan"] = plan.returncode == 0

        result["success"] = all([
            result["fmt"],
            result["init"],
            result["validate"],
            result["plan"],
        ])

    except FileNotFoundError:
        result["error"] = "Terraform CLI was not found."

    return result