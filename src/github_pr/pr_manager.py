import subprocess


def run_command(args):
    result = subprocess.run(
        args,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }


def create_branch(branch_name):
    return run_command([
        "git",
        "checkout",
        "-b",
        branch_name
    ])


def add_generated_files():
    return run_command([
        "git",
        "add",
        "outputs/terraform"
    ])


def commit_changes(message):
    return run_command([
        "git",
        "commit",
        "-m",
        message
    ])


def push_branch(branch_name):
    return run_command([
        "git",
        "push",
        "-u",
        "origin",
        branch_name
    ])


def create_pull_request(title, body, base_branch="main"):
    return run_command([
        "gh",
        "pr",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--base",
        base_branch
    ])