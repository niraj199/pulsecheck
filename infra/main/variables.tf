variable "aws_region" {
  description = "AWS region for all PulseCheck resources."
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Prefix for resource names."
  type        = string
  default     = "pulsecheck"
}

variable "target_urls" {
  description = "Websites the checker monitors."
  type        = list(string)
  default     = ["https://example.com", "https://aws.amazon.com"]
}

variable "log_retention_days" {
  description = "How long to keep Lambda logs."
  type        = number
  default     = 14
}
