from src.repo_analyzer.analyzer import analyze_repository
from src.requirements_agent.requirements import build_requirements
from src.terraform_pattern_selector.selector import select_pattern
from src.terraform_generator.generator import generate_terraform
from src.terraform_validator.validator import validate_terraform
from src.github_pr.git_manager import (
    check_git_repository,
    get_current_branch
)


repo_path = "."

app_profile = analyze_repository(repo_path)
deployment_requirements = build_requirements(app_profile)

print("APP PROFILE")
print(app_profile)

deployment_requirements = build_requirements(app_profile)

print("\nDEPLOYMENT REQUIREMENTS")
print(deployment_requirements)

infrastructure_pattern = select_pattern(
    app_profile,
    deployment_requirements
)

print("\nINFRASTRUCTURE PATTERN")
print(infrastructure_pattern)

terraform_output = generate_terraform(infrastructure_pattern)

print("\nTERRAFORM GENERATED")
print(terraform_output)

validation_result = validate_terraform(terraform_output)

print("\nTERRAFORM VALIDATION")
print(validation_result)

git_status = check_git_repository()
current_branch = get_current_branch()

print("\nGIT STATUS")
print(git_status)

print("\nCURRENT BRANCH")
print(current_branch)