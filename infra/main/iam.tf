# Trust policy: only the Lambda service may assume this role.
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "checker" {
  name               = "${local.checker_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

# Permissions: write to this function's own log group, and nothing else.
data "aws_iam_policy_document" "checker_logs" {
  statement {
    sid       = "WriteOwnLogsOnly"
    effect    = "Allow"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.checker.arn}:*"]
  }
}

resource "aws_iam_role_policy" "checker_logs" {
  name   = "write-own-logs"
  role   = aws_iam_role.checker.id
  policy = data.aws_iam_policy_document.checker_logs.json
}
