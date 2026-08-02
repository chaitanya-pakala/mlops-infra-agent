import subprocess


def run_git_command(args):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }


def check_git_repository():
    return run_git_command(
        ["rev-parse", "--is-inside-work-tree"]
    )


def get_current_branch():
    return run_git_command(
        ["branch", "--show-current"]
    )