locals {
  checker_name = "${var.project_name}-checker"
}

# Zip app/checker (checker.py + handler.py) for upload to Lambda.
data "archive_file" "checker" {
  type        = "zip"
  source_dir  = "${path.module}/../../app/checker"
  output_path = "${path.module}/build/checker.zip"
}

# Created up front so retention is set; otherwise Lambda would create
# a log group that keeps logs forever.
resource "aws_cloudwatch_log_group" "checker" {
  name              = "/aws/lambda/${local.checker_name}"
  retention_in_days = var.log_retention_days
}

resource "aws_lambda_function" "checker" {
  function_name    = local.checker_name
  description      = "Checks website availability for PulseCheck"
  role             = aws_iam_role.checker.arn
  runtime          = "python3.14"
  handler          = "handler.lambda_handler"
  architectures    = ["arm64"]
  memory_size      = 128
  timeout          = 60
  filename         = data.archive_file.checker.output_path
  source_code_hash = data.archive_file.checker.output_base64sha256

  environment {
    variables = {
      TARGET_URLS = join(",", var.target_urls)
      LOG_LEVEL   = "INFO"
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.checker,
    aws_iam_role_policy.checker_logs,
  ]
}
