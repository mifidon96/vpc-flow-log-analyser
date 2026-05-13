# VPC Flow Log Analyser

Terraform provisions a VPC with flow logs shipped to CloudWatch Logs.
Python script parses the logs and summarises ACCEPT/REJECT traffic.
CloudWatch alarm fires an SNS email alert when rejected traffic spikes.

## Architecture
- AWS VPC with flow logging enabled
- CloudWatch Log Group (7-day retention)
- IAM role scoped to flow logs service
- CloudWatch Metric Filter — counts REJECT events
- CloudWatch Alarm — triggers when rejects exceed 100 in 5 minutes
- SNS Topic + email subscription for alerting
- boto3 analyser script

## Usage

### Deploy infrastructure
cd terraform
terraform init && terraform apply

### Run analyser
python analyser.py --log-group /aws/vpc/flow-logs/vpc-flow-log-analyser --hours 1

## Requirements
- Python 3.8+
- boto3
- AWS credentials configured