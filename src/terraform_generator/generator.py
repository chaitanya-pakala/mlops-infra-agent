from pathlib import Path
import shutil


def generate_terraform(
    infrastructure_pattern,
    environment="dev",
    output_dir="outputs/terraform"
):
    pattern_name = infrastructure_pattern.get("pattern_name")

    if not pattern_name:
        raise ValueError("No infrastructure pattern was selected.")

    allowed_environments = [
        "dev",
        "staging",
        "prod"
    ]

    if environment not in allowed_environments:
        raise ValueError(
            f"Invalid environment: {environment}. "
            f"Choose from {allowed_environments}"
        )

    pattern_path = Path("patterns") / pattern_name

    environment_file = (
        Path("environments") / f"{environment}.tfvars"
    )

    output_path = Path(output_dir)

    if not pattern_path.exists():
        raise FileNotFoundError(
            f"Terraform pattern not found: {pattern_path}"
        )

    if not environment_file.exists():
        raise FileNotFoundError(
            f"Environment file not found: {environment_file}"
        )

    if output_path.exists():
        shutil.rmtree(output_path)

    # Copy the approved Terraform pattern
    shutil.copytree(
        pattern_path,
        output_path
    )

    # Copy environment-specific values
    shutil.copy(
        environment_file,
        output_path / "terraform.tfvars"
    )

    return str(output_path)