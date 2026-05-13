import boto3
import argparse
from collections import Counter
from datetime import datetime, timedelta

def get_log_events(log_group, hours=1):
    client = boto3.client("logs")
    start_time = int((datetime.utcnow() - timedelta(hours=hours)).timestamp() * 1000)

    streams = client.describe_log_streams(
        logGroupName=log_group,
        orderBy="LastEventTime",
        descending=True,
        limit=5
    )["logStreams"]

    events = []
    for stream in streams:
        response = client.get_log_events(
            logGroupName=log_group,
            logStreamName=stream["logStreamName"],
            startTime=start_time,
            limit=1000
        )
        events.extend(response["events"])

    return [e["message"] for e in events]

def parse_flow_log(line):
    fields = line.split()
    if len(fields) < 14 or fields[0] == "version":
        return None
    return {
        "srcaddr":  fields[3],
        "dstaddr":  fields[4],
        "dstport":  fields[6],
        "protocol": fields[7],
        "action":   fields[12],
    }

def analyse(log_group, hours):
    print(f"\nFetching flow logs from: {log_group} (last {hours}h)\n")
    raw = get_log_events(log_group, hours)

    parsed = [parse_flow_log(l) for l in raw]
    parsed = [p for p in parsed if p]

    accepts = [p for p in parsed if p["action"] == "ACCEPT"]
    rejects = [p for p in parsed if p["action"] == "REJECT"]

    print(f"Total records : {len(parsed)}")
    print(f"ACCEPT        : {len(accepts)}")
    print(f"REJECT        : {len(rejects)}\n")

    print("Top 10 rejected destination ports:")
    for port, count in Counter(p["dstport"] for p in rejects).most_common(10):
        print(f"  Port {port:>6}  —  {count} hits")

    print("\nTop 5 rejected source IPs:")
    for ip, count in Counter(p["srcaddr"] for p in rejects).most_common(5):
        print(f"  {ip:<20}  —  {count} hits")

if __name