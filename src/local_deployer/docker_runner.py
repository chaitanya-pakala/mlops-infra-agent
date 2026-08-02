import subprocess
import time
import urllib.request


def run_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def build_docker_image():
    return run_command([
        "docker",
        "build",
        "-t",
        "mlops-demo-app",
        "./demo_app"
    ])


def remove_old_container():
    subprocess.run(
        ["docker", "rm", "-f", "mlops-demo"],
        capture_output=True,
        text=True
    )


def run_container():
    return run_command([
        "docker",
        "run",
        "-d",
        "--name",
        "mlops-demo",
        "-p",
        "8000:8000",
        "mlops-demo-app"
    ])


def health_check():
    time.sleep(2)

    try:
        response = urllib.request.urlopen(
            "http://localhost:8000",
            timeout=5
        )

        body = response.read().decode()

        return {
            "success": response.status == 200,
            "response": body
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def deploy_local_docker():
    remove_old_container()

    build_result = build_docker_image()

    if not build_result["success"]:
        return {
            "success": False,
            "stage": "docker_build",
            "details": build_result
        }

    run_result = run_container()

    if not run_result["success"]:
        return {
            "success": False,
            "stage": "docker_run",
            "details": run_result
        }

    health_result = health_check()

    return {
        "success": health_result["success"],
        "stage": "health_check",
        "details": health_result
    }