terraform {
  required_version = ">= 1.5.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

resource "null_resource" "container" {
  triggers = {
    environment = var.environment
  }

  provisioner "local-exec" {
    command = "echo Preparing app container for ${var.environment}"
  }
}

resource "null_resource" "database" {
  triggers = {
    environment = var.environment
  }

  provisioner "local-exec" {
    command = "echo Preparing database for ${var.environment}"
  }
}

resource "null_resource" "networking" {
  triggers = {
    environment = var.environment
  }

  provisioner "local-exec" {
    command = "echo Preparing networking for ${var.environment}"
  }
}