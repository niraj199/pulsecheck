terraform {
  required_version = ">= 1.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }

  # State lives in the bucket created by infra/bootstrap.
  backend "s3" {
    bucket       = "pulsecheck-tfstate-69214bc7"
    key          = "pulsecheck/main.tfstate"
    region       = "us-east-2"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "pulsecheck"
      ManagedBy   = "terraform"
      Environment = "dev"
    }
  }
}
