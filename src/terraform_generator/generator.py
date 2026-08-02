from pathlib import Path


def generate_terraform(infrastructure_pattern, output_dir="outputs/terraform"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    components = infrastructure_pattern.get("components", [])

    main_tf = """terraform {
  required_version = ">= 1.5.0"
}

"""

    if "container" in components:
        main_tf += """
# Container infrastructure placeholder
resource "null_resource" "container" {
  provisioner "local-exec" {
    command = "echo Container infrastructure selected"
  }
}
"""

    if "database" in components:
        main_tf += """
# Database infrastructure placeholder
resource "null_resource" "database" {
  provisioner "local-exec" {
    command = "echo Database infrastructure selected"
  }
}
"""

    if "networking" in components:
        main_tf += """
# Networking infrastructure placeholder
resource "null_resource" "networking" {
  provisioner "local-exec" {
    command = "echo Networking infrastructure selected"
  }
}
"""

    variables_tf = """variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "local"
}
"""

    outputs_tf = """output "selected_pattern" {
  value = "Infrastructure generated successfully"
}
"""

    tfvars = """environment = "local"
"""

    (output_path / "main.tf").write_text(main_tf)
    (output_path / "variables.tf").write_text(variables_tf)
    (output_path / "outputs.tf").write_text(outputs_tf)
    (output_path / "terraform.tfvars").write_text(tfvars)

    return str(output_path)