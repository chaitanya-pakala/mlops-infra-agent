from src.github_pr.pr_manager import (
    create_branch,
    add_generated_files,
    commit_changes,
    push_branch,
    create_pull_request
)


branch_name = "infra/generated-terraform"

print("Creating branch...")
print(create_branch(branch_name))

print("\nAdding Terraform files...")
print(add_generated_files())

print("\nCreating commit...")
print(commit_changes(
    "Generate Terraform infrastructure"
))

print("\nPushing branch...")
print(push_branch(branch_name))

print("\nCreating pull request...")
print(create_pull_request(
    title="Generate Terraform infrastructure",
    body="Generated and validated Terraform infrastructure from the MLOps infrastructure agent."
))