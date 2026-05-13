# VPC Flow Log Analyser

Terraform provisions a VPC with flow logs shipped to CloudWatch Logs.
Python script parses the logs and summarises ACCEPT/REJECT traffic.

## Architecture
- AWS VPC with flow logging enabled
- CloudWatch Log Group (7-day retention)
- IAM role scoped to flow logs service
- boto3 analyser script

## Usage

### Deploy infrastructure
```bash
cd terraform
terraform init && terraform apply
```

### Run analyser
```bash
python analyser.py --log-group /aws/vpc/flow-logs/vpc-flow-log-analyser --hours 1
```

## Requirements
- Python 3.8+
- boto3
- AWS credentials configured