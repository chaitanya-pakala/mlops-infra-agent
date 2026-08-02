import argparse

from src.local_deployer.kubernetes_runner import deploy_local_kubernetes
from src.local_deployer.docker_runner import deploy_local_docker
from src.repo_analyzer.analyzer import analyze_repository
from src.requirements_agent.requirements import build_requirements
from src.terraform_pattern_selector.selector import select_pattern
from src.terraform_generator.generator import generate_terraform
from src.terraform_validator.validator import validate_terraform
from src.github_pr.git_manager import (
    check_git_repository,
    get_current_branch
)
from src.github_pr.pr_manager import (
    create_branch,
    add_generated_files,
    commit_changes,
    push_branch
)

parser = argparse.ArgumentParser(
    description="MLOps Infrastructure Agent"
)

parser.add_argument(
    "--environment",
    choices=["dev", "staging", "prod"],
    default="dev",
    help="Deployment environment"
)

parser.add_argument(
    "--repo-path",
    default="./demo_app",
    help="Path to the application repository to analyze"
)

args = parser.parse_args()

environment = args.environment
repo_path = args.repo_path

app_profile = analyze_repository(repo_path)
deployment_requirements = build_requirements(app_profile)

print("APP PROFILE")
print(app_profile)


print("\nDEPLOYMENT REQUIREMENTS")
print(deployment_requirements)



infrastructure_pattern = select_pattern(
    app_profile,
    deployment_requirements
)

print("\nINFRASTRUCTURE PATTERN")
print(infrastructure_pattern)

print("\nDEPLOYMENT ENVIRONMENT")
print(environment)

terraform_output = generate_terraform(infrastructure_pattern, environment)

print("\nTERRAFORM GENERATED")
print(terraform_output)

validation_result = validate_terraform(terraform_output)

print("\nTERRAFORM VALIDATION")
print(validation_result)

if validation_result.get("success"):

    if infrastructure_pattern.get("pattern_name") == "kubernetes_web_app":
        local_deployment = deploy_local_kubernetes()

        print("\nLOCAL KUBERNETES DEPLOYMENT")
        print(local_deployment)

    else:
        local_deployment = deploy_local_docker()

        print("\nLOCAL DOCKER DEPLOYMENT")
        print(local_deployment)

    
git_status = check_git_repository()
current_branch = get_current_branch()

print("\nGIT STATUS")
print(git_status)

print("\nCURRENT BRANCH")
print(current_branch)

print("\nGITHUB AUTOMATION")
print("Git branch/commit/push functions are ready.")