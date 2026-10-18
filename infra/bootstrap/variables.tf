variable "aws_region" {
  description = "AWS region for all PulseCheck resources."
  type        = string
  default     = "us-east-2"
}

variable "noncurrent_version_retention_days" {
  description = "Days to keep old versions of state files before deleting them."
  type        = number
  default     = 90
}
