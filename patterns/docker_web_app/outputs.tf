output "selected_environment" {
  description = "Environment selected for deployment"
  value       = var.environment
}

output "deployment_pattern" {
  description = "Approved infrastructure pattern"
  value       = "docker_web_app"
}