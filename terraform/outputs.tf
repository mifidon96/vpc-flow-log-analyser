output "vpc_id" {
  value = aws_vpc.main.id
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.flow_logs.name
}