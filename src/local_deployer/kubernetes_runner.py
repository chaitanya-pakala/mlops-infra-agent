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


def ensure_kind_cluster():
    clusters = run_command(["kind", "get", "clusters"])

    if not clusters["success"]:
        return clusters

    if "mlops-local" in clusters["stdout"]:
        return {
            "success": True,
            "stdout": "Kind cluster already exists."
        }

    return run_command([
        "kind",
        "create",
        "cluster",
        "--name",
        "mlops-local"
    ])


def load_image_into_kind():
    return run_command([
        "kind",
        "load",
        "docker-image",
        "mlops-demo-app",
        "--name",
        "mlops-local"
    ])


def apply_kubernetes_manifests():
    deployment = run_command([
        "kubectl",
        "apply",
        "-f",
        "k8s/deployment.yaml"
    ])

    if not deployment["success"]:
        return deployment

    service = run_command([
        "kubectl",
        "apply",
        "-f",
        "k8s/service.yaml"
    ])

    return service


def wait_for_deployment():
    return run_command([
        "kubectl",
        "rollout",
        "status",
        "deployment/mlops-demo",
        "--timeout=60s"
    ])


def start_port_forward():
    return subprocess.Popen(
        [
            "kubectl",
            "port-forward",
            "service/mlops-demo-service",
            "8080:8000"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def health_check():
    time.sleep(3)

    try:
        response = urllib.request.urlopen(
            "http://localhost:8080",
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


def deploy_local_kubernetes():
    cluster_result = ensure_kind_cluster()

    if not cluster_result["success"]:
        return {
            "success": False,
            "stage": "kind_cluster",
            "details": cluster_result
        }

    image_result = load_image_into_kind()

    if not image_result["success"]:
        return {
            "success": False,
            "stage": "image_load",
            "details": image_result
        }

    apply_result = apply_kubernetes_manifests()

    if not apply_result["success"]:
        return {
            "success": False,
            "stage": "kubectl_apply",
            "details": apply_result
        }

    rollout_result = wait_for_deployment()

    if not rollout_result["success"]:
        return {
            "success": False,
            "stage": "deployment_rollout",
            "details": rollout_result
        }

    port_forward_process = start_port_forward()

    health_result = health_check()

    return {
        "success": health_result["success"],
        "stage": "health_check",
        "details": health_result,
        "port_forward_pid": port_forward_process.pid
    }