terraform {
  required_version = ">= 1.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # Every resource this configuration creates gets these tags automatically.
  default_tags {
    tags = {
      Project   = "pulsecheck"
      ManagedBy = "terraform"
      Component = "state-bootstrap"
    }
  }
}
