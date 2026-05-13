import boto3
import argparse
from collections import Counter
from datetime import datetime, timedelta

def get_log_events(log_group, hours=1):
    client = boto3.client("logs")
    start_time = int((datetime.utcnow() - timedelta(hours=hours)).timestamp() * 1000)

    streams = client.describe_log_