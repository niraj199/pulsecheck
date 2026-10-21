output "checker_function_name" {
  value = aws_lambda_function.checker.function_name
}

output "checker_log_group" {
  value = aws_cloudwatch_log_group.checker.name
}
