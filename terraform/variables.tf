variable "aws_region" {
  default = "eu-west-2"
}

variable "project_name" {
  default = "vpc-flow-log-analyser"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "log_retention_days" {
  default = 7
}