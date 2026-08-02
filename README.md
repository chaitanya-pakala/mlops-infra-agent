# MLOps Infrastructure Agent

An agent-style MLOps project that analyzes an application repository, determines its infrastructure requirements, selects an approved Terraform pattern, generates infrastructure code, validates it, and deploys the application locally using Docker or Kubernetes.

The project is designed to demonstrate how infrastructure automation can be made safer by selecting from reusable Terraform patterns instead of allowing an LLM or automation system to generate arbitrary infrastructure.

## Project Flow

1. **Repo Analyzer**

   * Analyzes a target application repository.
   * Detects application language and important deployment files.
   * Detects Docker usage.
   * Detects database dependencies from `requirements.txt`.
   * Detects Kubernetes manifests recursively.

2. **Requirements Agent**

   * Converts repository findings into deployment requirements.
   * Determines whether the application needs:

     * containerization
     * database infrastructure
     * Kubernetes
     * networking
     * environment configuration

3. **Terraform Pattern Selector**

   * Selects an approved infrastructure pattern based on application requirements.

   Current patterns:

   * `docker_web_app`
   * `docker_web_app_with_db`
   * `kubernetes_web_app`

4. **Terraform Generator**

   * Retrieves the selected Terraform pattern from the approved pattern catalog.
   * Combines the pattern with environment-specific configuration.
   * Generates Terraform under `outputs/terraform`.

5. **Terraform Validation**

   * Runs:

     * `terraform fmt`
     * `terraform init`
     * `terraform validate`
     * `terraform plan`
   * Infrastructure proceeds only when validation succeeds.

6. **GitHub Automation**

   * Supports Git branch, commit, push, and pull-request workflow for generated infrastructure changes.

7. **Local Deployment**

   * Docker applications are built and deployed locally.
   * Kubernetes applications are deployed to a local Kind Kubernetes cluster.
   * Automated health checks confirm that the application is reachable.

8. **Troubleshooting — Future Enhancement**

   * Docker log analysis.
   * Kubernetes pod and deployment diagnostics.
   * Automated remediation suggestions.

## Multi-Environment Support

The agent supports:

* `dev`
* `staging`
* `prod`

Environment-specific values are stored separately from the Terraform patterns.

Example:

```bash
python run_pipeline.py --repo-path ./demo_app --environment dev
```

```bash
python run_pipeline.py --repo-path ./demo_app --environment staging
```

```bash
python run_pipeline.py --repo-path ./demo_app --environment prod
```

This separation allows the same approved infrastructure pattern to be reused with different environment configurations.

## Terraform Pattern Catalog

```text
patterns/
├── docker_web_app/
├── docker_web_app_with_db/
└── kubernetes_web_app/
```

Instead of generating arbitrary Terraform, the agent selects one of these approved patterns.

Example decision flow:

```text
Application Repository
        ↓
Repository Analysis
        ↓
Deployment Requirements
        ↓
Kubernetes required?
        │
       Yes → kubernetes_web_app
        │
        No
        ↓
Database required?
        │
       Yes → docker_web_app_with_db
        │
        No
        ↓
docker_web_app
```

## Local Deployment

### Docker

For standard containerized applications:

```text
Application
    ↓
Docker Image
    ↓
Docker Container
    ↓
Health Check
```

### Kubernetes

For Kubernetes applications:

```text
Application
    ↓
Docker Image
    ↓
Kind Kubernetes Cluster
    ↓
Deployment
    ↓
Pod
    ↓
Service
    ↓
Health Check
```

Kind allows the Kubernetes environment to run entirely on a developer laptop without requiring a paid cloud account.

## Repository Analysis

The pipeline can analyze a separate application repository instead of analyzing itself.

Example:

```bash
python run_pipeline.py \
  --repo-path E:\Projects\customer-api \
  --environment dev
```

This allows the MLOps Infrastructure Agent to act as a reusable infrastructure assistant for different development teams and application repositories.

## Technologies

* Python
* Terraform
* Docker
* Kubernetes
* Kind
* kubectl
* Git
* GitHub

## Example End-to-End Workflow

```text
Developer Application Repo
          ↓
Repo Analyzer
          ↓
Requirements Agent
          ↓
Terraform Pattern Selector
          ↓
Terraform Generator
          ↓
Terraform Validate / Plan
          ↓
GitHub Workflow
          ↓
Local Deployment
      ┌───────┴────────┐
      ↓                ↓
   Docker          Kubernetes
                     (Kind)
```

## Future Improvements

* Automated Docker and Kubernetes troubleshooting.
* Infrastructure security scanning using tools such as Checkov.
* TFLint integration.
* Richer Terraform pattern catalog.
* More advanced pattern-selection policies.
* Cloud deployment options through approved Terraform modules.
* Web UI or MCP interface for developer interaction.
* Automated pull-request review checks.
